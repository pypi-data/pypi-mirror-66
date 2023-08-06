def PCA(feature_array, n_components=None, whiten=True, svd_solver='auto', tol=0.0, random_state=None):
    """ Performs Principal Component Analysis on a feature set to deduce axis that have the highest variance.
        Each component is guarenteed orthogonal in the original feature space (boon and bane).

    Args:
        feature_array: 2D array (#Sample x #Feature), should be float64
        n_components : How many components are desired, None = all (# input features)
        whiten       : Only set to False if you have already whitened the data
        tol          : Tolerance on update at each iteration
        svd_solver   : Which solver to use, 'auto' intelligently selects
        random_state : Random seed to fix output
    Output:
        components   : PCA components (#features, #components)
        weights      : Sample weights (#samples , #components)

    >>> import numpy as N
    >>> N.random.seed(0)
    >>> feature_array = N.random.random((1000,10))

    >>> components, weights = PCA(feature_array, n_components = 3)

    >>> components.shape
    (10, 3)

    >>> weights.shape
    (1000, 3)


    """

    from sklearn.decomposition import PCA as skPCA

    _PCA = skPCA(n_components=n_components,
                 whiten=whiten, svd_solver=svd_solver,
                 tol=tol, copy=True,
                 random_state=random_state)

    weights = _PCA.fit(feature_array).transform(feature_array)

    components = _PCA.components_.T

    return components, weights


def ICA(feature_array, n_components=None, algorithm='parallel', whiten=True, fun='logcosh', fun_args=None, max_iter=200,
        tol=0.0001, w_init=None, random_state=None):
    """ Performs Independent Component Analysis on a feature set to deduce axis that are "least Gaussian"
        of all possible orientations. Like PCA, but does not require orthogonality in the original feature space.

    Args:
        feature_array: 2D array (#Sample x #Feature), should be float64
        n_components : How many components are desired, None = all (# input features)
        algorithm    : 'parallel' or 'deflation', 'parallel' default
        whiten       : Only set to False if you have already whitened the data
        fun          : The functional form of the G function. logcosh, exp, or cube available. May also provide own.
        fun_args     : dictionary of arguments for function
        max_iter     : Maximum number of iterations during fit
        tol          : Tolerance on update at each iteration
        w_init       : Mixing matrix to be used to initialize algorithm
        random_state : Random seed to fix output
    Output:
        components   : The ICA components     (#features, #ICA_components)
        weights      : The weights per sample (#samples, #ICA_components)

    >>> import numpy as N
    >>> N.random.seed(0)
    >>> feature_array = N.random.random((1000,10))

    >>> components, weights = ICA(feature_array, n_components = 2)

    components are (#orig_features, #ICA_components)
    >>> components.shape
    (10, 2)

    weights are (#samples, #ICA_components)
    >>> weights.shape
    (1000, 2)


    """

    from sklearn.decomposition import FastICA

    ICA = FastICA(n_components=n_components, algorithm=algorithm,
                  whiten=whiten, fun=fun, fun_args=fun_args, max_iter=max_iter, tol=tol,
                  w_init=w_init, random_state=random_state)

    # Generates the "weights" for each sample vs. the requested ICA components (numsamples, numcomponents)
    weights = ICA.fit(feature_array).transform(feature_array)

    # Shows the ICA components themselves (numfeat x numcomponents)
    components = ICA.mixing_

    return components, weights


def TSNE(feature_array, pca_dim=None, output_dim=2, perplexity=30, theta=0.5):
    """ Performs TSNE on the incoming features. Forms a manifold encoding that preserves nearest neighbor
        relationships rather than pursuing a simple distance-metric density cluster analysis.

    Args:
        feature_array: 2D array (#Sample x #Feature), must be float64
        pca_dim      : PCA is used to reduce incoming dimensionality to pca_dim (None means don't do)
        output_dim   : The dimension of the TSNE output, default is 2 (other settings are unstable)
        perplexity   : The rough number of neighbors to preserve, default 30
        theta        : A value that permits approximate matching, required for datasets > 5000 samples, default 0.5
    Returns:
        x, y         : 2 1-D arrays for the x and y coordinates in TSNE space

    >>> import numpy as N
    >>> N.random.seed(0)
    >>> feature_array = N.random.random((1000,10))

    >>> x, y = TSNE(feature_array)

    Expected values are changed as tsne.bh_tse() function is replaced by
    the sklearn.manifold.TSNE().
    TODO: the TSNE performance needs to be rigorously checked out.
    >>> print(round(N.min(x), 4), round(N.max(x), 4), round(N.median(x), 4))
    -33.5334 37.4999 0.1886

    >>> print(round(N.min(y), 4), round(N.max(y), 4), round(N.median(y), 4))
    -40.3367 39.2321 0.1085

    """

    from sklearn.manifold import TSNE as skl_tsne

    # Previous implementation:
    # from tsne import bh_sne
    # new_coordinates = bh_sne(feature_array, d=output_dim, pca_d=pca_dim, perplexity=perplexity, theta=theta)

    # TODO: might need to pass "init" input argument set to "pca" (default value: “random”) if "pca_dim" is enabled.
    new_coordinates = skl_tsne(method='barnes_hut', n_components=output_dim, perplexity=perplexity, angle=theta).fit_transform(feature_array)

    return new_coordinates[:, 0], new_coordinates[:, 1]


# --------------------------------
# --------------------------------
# --------------------------------

if __name__ == "__main__":
    import doctest
    import numpy as N

    doctest.testmod()
