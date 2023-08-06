import numpy as np
import pandas as pd
from sklearn.datasets import make_blobs

def make_subspace_blobs(p_dim=0.7,**blobs_params):
    """
    Parameters
    ----------
    p_dim : float, default=0.7
        Proportion of noise dimensions in clusters
    **blobs_params : named parameters
        Parameters from the sklearn.datasets.blobs_params function

    Returns
    -------
    np.ndarray
        Dataset generated
    np.ndarray
        cluster memberships
    np.ndarray
        True cluster subspaces

    Examples:
    ---------
        >>> import seaborn as sns
        >>> import matplotlib.pyplot as plt
        >>> import pandas as pd
        >>> X,y_true,subspaces = make_subspace_blobs()
        >>> X_df = pd.DataFrame(X)
        >>> X_df["cluster"] = y_true
        >>> sns.scatterplot(x=0, y=1, hue="cluster", marker=".", data=X_df)
        >>> plt.show()
        >>> sns.heatmap(subspaces)
        >>> plt.show()
    """
    default_blobs_params = {"n_samples":1000,
                            "n_features":10,
                            "centers":5,
                            "cluster_std":1.0,
                            "center_box":(-10.0, 10.0),
                            "shuffle":True,
                            "random_state":None,}
    default_blobs_params.update(blobs_params)
    X,y_true = make_blobs(**default_blobs_params)
    subspaces = np.random.binomial(size=(default_blobs_params["centers"],
                                         default_blobs_params["n_features"]),
                                   p=1 - p_dim,
                                   n=1)
    uniform_coordinates = np.random.uniform(low=default_blobs_params["center_box"][0],
                                            high=default_blobs_params["center_box"][1],
                                            size=X.shape)
    X_rand_subspaces =  subspaces[y_true,:]
    X *= np.logical_not(X_rand_subspaces)
    X += uniform_coordinates*X_rand_subspaces
    ss = pd.DataFrame(np.logical_not(subspaces))
    return(X,y_true,ss)
