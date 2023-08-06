from multiprocessing.pool import Pool

import numpy as np
from scipy import sparse
from sklearn.base import TransformerMixin
from sklearn.pipeline import FeatureUnion, _fit_one, _fit_transform_one, _transform_one, _name_estimators
from sklearn.utils.metaestimators import _BaseComposition
from wordbatch.pipelines import Apply

def fit_one(args):
	X, y, transformer, fit_params = args
	return transformer.fit(X, y, **fit_params)

def transform_one(args):
	X, transformer= args
	return transformer.transform(X)

def fit_transform_one(args):
	X, y, transformer, fit_params = args
	return transformer.fit_transform(X, y, **fit_params), transformer

class FeatureUnion(_BaseComposition, TransformerMixin):
	"""Concatenates results of multiple transformer objects.

	This estimator applies a list of transformer objects in parallel to the
	input data, then concatenates the results. This is useful to combine
	several feature extraction mechanisms into a single transformer.

	Parameters of the transformers may be set using its name and the parameter
	name separated by a '__'. A transformer may be replaced entirely by
	setting the parameter with its name to another transformer,
	or removed by setting to 'drop' or ``None``.

	Read more in the :ref:`User Guide <feature_union>`.

	Parameters
	----------
	transformer_list : list of (string, transformer) tuples
	    List of transformer objects to be applied to the data. The first
	    half of each tuple is the name of the transformer.

	n_jobs : int or None, optional (default=None)
	    Number of jobs to run in parallel.
	    ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.
	    ``-1`` means using all processors. See :term:`Glossary <n_jobs>`
	    for more details.

	transformer_weights : dict, optional
	    Multiplicative weights for features per transformer.
	    Keys are transformer names, values the weights.

	verbose : boolean, optional(default=False)
	    If True, the time elapsed while fitting each transformer will be
	    printed as it is completed.

	See also
	--------
	sklearn.pipeline.make_union : convenience function for simplified
	    feature union construction.

	Examples
	--------
	>>> from sklearn.pipeline import FeatureUnion
	>>> from sklearn.decomposition import PCA, TruncatedSVD
	>>> union = FeatureUnion([("pca", PCA(n_components=1)),
	...                       ("svd", TruncatedSVD(n_components=2))])
	>>> X = [[0., 1., 3], [2., 2., 5]]
	>>> union.fit_transform(X)
	array([[ 1.5       ,  3.0...,  0.8...],
	       [-1.5       ,  5.7..., -0.4...]])
	"""
	_required_parameters = ["transformer_list"]

	def __init__(self, transformer_list, transformer_weights=None, batcher=None, concatenate=True):
		self.transformer_list = transformer_list
		self.transformer_weights = transformer_weights
		self._validate_transformers()
		self.batcher = batcher
		self.concatenate= concatenate

	def get_params(self, deep=True):
		"""Get parameters for this estimator.

		Parameters
		----------
		deep : boolean, optional
			If True, will return the parameters for this estimator and
			contained subobjects that are estimators.

		Returns
		-------
		params : mapping of string to any
			Parameter names mapped to their values.
		"""
		return self._get_params('transformer_list', deep=deep)

	def set_params(self, **kwargs):
		"""Set the parameters of this estimator.

		Valid parameter keys can be listed with ``get_params()``.

		Returns
		-------
		self
		"""
		self._set_params('transformer_list', **kwargs)
		return self

	def _validate_transformers(self):
		names, transformers = zip(*self.transformer_list)

		# validate names
		self._validate_names(names)

		# validate estimators
		for t in transformers:
			if t is None or t == 'drop':
				continue
			if (not (hasattr(t, "fit") or hasattr(t, "fit_transform")) or not
			hasattr(t, "transform")):
				raise TypeError("All estimators should implement fit and "
								"transform. '%s' (type %s) doesn't" %
								(t, type(t)))

	def _iter(self):
		"""
		Generate (name, trans, weight) tuples excluding None and
		'drop' transformers.
		"""
		get_weight = (self.transformer_weights or {}).get
		return ((name, trans, get_weight(name))
				for name, trans in self.transformer_list
		        if trans is not None and trans != 'drop')

	def get_feature_names(self):
		"""Get feature names from all transformers.

		Returns
		-------
		feature_names : list of strings
			Names of the features produced by transform.
		"""
		feature_names = []
		for name, trans, weight in self._iter():
			if not hasattr(trans, 'get_feature_names'):
				raise AttributeError("Transformer %s (type %s) does not "
									 "provide get_feature_names."
									 % (str(name), type(trans).__name__))
			feature_names.extend([name + "__" + f for f in
								  trans.get_feature_names()])
		return feature_names

	def fit(self, X, y=None, **fit_params):
		"""Fit all transformers using X.

		Parameters
		----------
		X : iterable or array-like, depending on transformers
			Input data, used to fit transformers.

		y : array-like, shape (n_samples, ...), optional
			Targets for supervised learning.

		Returns
		-------
		self : FeatureUnion
			This estimator
		"""
		self.transformer_list = list(self.transformer_list)
		self._validate_transformers()
		paral_params = [[X[t['col_pick']] if hasattr(t, 'col_pick') else X, y, t, fit_params]
		                for _, t, _ in self._iter()]
		transformers= Apply(fit_one, self.batcher).transform(paral_params)
		# with Pool(self.n_jobs) as pool:
		# 	transformers = pool.starmap(_fit_one,
		# 				((trans, X[trans['col_pick']] if hasattr(trans, 'col_pick') else X, y) for _, trans, _ in self._iter()))
		self._update_transformer_list(transformers)
		return self

	def fit_transform(self, X, y=None, **fit_params):
		"""Fit all transformers, transform the data and concatenate results.

		Parameters
		----------
		X : iterable or array-like, depending on transformers
			Input data to be transformed.

		y : array-like, shape (n_samples, ...), optional
			Targets for supervised learning.

		Returns
		-------
		X_t : array-like or sparse matrix, shape (n_samples, sum_n_components)
			hstack of results of transformers. sum_n_components is the
			sum of n_components (output dimension) over transformers.
		"""
		self._validate_transformers()
		paral_params = [[X[t['col_pick']] if hasattr(t, 'col_pick') else X, y, t, fit_params]
		                for _, t, _ in self._iter()]
		result = Apply(fit_transform_one, self.batcher).transform(paral_params)
		if not result:
			# All transformers are None
			return np.zeros((X.shape[0], 0))
		Xs, transformers = zip(*result)
		self._update_transformer_list(transformers)
		if self.concatenate:
			if any(sparse.issparse(f) for f in Xs):
				Xs = sparse.hstack(Xs).tocsr()
			else:
				Xs = np.hstack(Xs)
		return Xs

	def transform(self, X):
		"""Transform X separately by each transformer, concatenate results.

		Parameters
		----------
		X : iterable or array-like, depending on transformers
			Input data to be transformed.

		Returns
		-------
		X_t : array-like or sparse matrix, shape (n_samples, sum_n_components)
			hstack of results of transformers. sum_n_components is the
			sum of n_components (output dimension) over transformers.
		"""
		paral_params = [[X[t['col_pick']] if hasattr(t, 'col_pick') else X, t] for _, t, _ in self._iter()]
		Xs = Apply(transform_one, self.batcher).transform(paral_params)
		if not Xs:
			# All transformers are None
			return np.zeros((X.shape[0], 0))
		if self.concatenate:
			if any(sparse.issparse(f) for f in Xs):
				Xs = sparse.hstack(Xs).tocsr()
			else:
				Xs = np.hstack(Xs)
		return Xs

	def _update_transformer_list(self, transformers):
		transformers = iter(transformers)
		self.transformer_list[:] = [(name, None if old is None or old == 'drop' else next(transformers))
		                            for name, old in self.transformer_list
		]


def make_union(*transformers, **kwargs):
	"""Construct a FeatureUnion from the given transformers.

	This is a shorthand for the FeatureUnion constructor; it does not require,
	and does not permit, naming the transformers. Instead, they will be given
	names automatically based on their types. It also does not allow weighting.

	Parameters
	----------
	*transformers : list of estimators

	n_jobs : int, optional
		Number of jobs to run in parallel (default 1).

	Returns
	-------
	f : FeatureUnion

	Examples
	--------
	>>> from sklearn.decomposition import PCA, TruncatedSVD
	>>> from sklearn.pipeline import make_union
	>>> make_union(PCA(), TruncatedSVD())    # doctest: +NORMALIZE_WHITESPACE
	FeatureUnion(n_jobs=1,
		   transformer_list=[('pca',
							  PCA(copy=True, iterated_power='auto',
								  n_components=None, random_state=None,
								  svd_solver='auto', tol=0.0, whiten=False)),
							 ('truncatedsvd',
							  TruncatedSVD(algorithm='randomized',
							  n_components=2, n_iter=5,
							  random_state=None, tol=0.0))],
		   transformer_weights=None)
	"""
	n_jobs = kwargs.pop('n_jobs', 1)
	concatenate = kwargs.pop('concatenate', True)
	if kwargs:
	   # We do not currently support `transformer_weights` as we may want to
	   # change its type spec in make_union
	   raise TypeError('Unknown keyword arguments: "{}"'
					   .format(list(kwargs.keys())[0]))
	return FeatureUnion(_name_estimators(transformers), n_jobs= n_jobs, concatenate= concatenate)
