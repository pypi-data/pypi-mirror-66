import numpy as np
import pandas as pd
from sklearn.metrics import pairwise_distances
from tqdm.autonotebook import tqdm
from SubCMedians.model import Model

class subcmedians_v3:
    def __init__(self, D, Gmax=300, H=200, nb_iter=10000,random_state=None):
        """SubCMedians subspace clustering.
        Parameters
        ----------
        Gmax : int, default=300
            Maximal model size, i.e., maximal number of coordinates that can
            be included in the model
        nb_iter : int, default=10000
            Number of iterations of the SubCMedians algorithm
        random_state : int, RandomState instance, default=None
            Determines random number generation for centroid initialization. Use
            an int to make the randomness deterministic.
            See :term:`Glossary <random_state>`.
        Attributes
        ----------
        cluster_centers_ : ndarray of shape (n_clusters, n_features)
            Coordinates of cluster centers.
        subspaces_  : ndarray of shape (n_clusters, n_features)
            Subspace of cluster centers.
        labels_ : ndarray of shape (n_samples,)
            Labels of each point
        sae_ : float
            Sum of Absolute Errors between data instances and their closest center

        Examples
        --------
        >>> from SubCMedians.subcmedians import subcmedians
        >>> from SubCMedians.data_generator import make_subspace_blobs
        >>> D = 20
        >>> dataset_params={"p_dim": 0.7,
                            "n_samples":5000,
                            "n_features":D,
                            "centers":12}
        >>> X,y_true,ss = make_subspace_blobs(**dataset_params)
        >>> X = (X - X.mean(axis=0))/ X.std(axis=0)
        >>> scm = subcmedians(D, Gmax=300, H=200, nb_iter=10000)
        >>> scm.fit(X)
        >>> y_pred = scm.predict(X)
        """
        self.model = Model(D=D,capacity=Gmax)
        self.Gmax = Gmax
        self.H = H
        self.D = D
        self.nb_iter = nb_iter
        self.S = {}
        self.random_state = random_state

    def predict(self, X):
        """
        Compute the cluster membership of the data instance from $X$

        Parameters
        ----------
        X : numpy.array
            Data set to be clustered, rows represent instances (points) and
            columns represent features (dimensions)

        Returns
        -------
        numpy.array
            cluster memberships

        """
        X = np.asarray(X)
        if len(X.shape) == 1:
            X = X.reshape(1,-1)
        distances = pairwise_distances(X,
                                       self.model.pheno.L(),
                                       metric="l1",
                                       n_jobs=None)
        self.labels_ = np.argmin(distances,axis=1)
        self.sae_ = distances[range(distances.shape[0]),self.labels_]
        return(self.labels_)

    def sae_score(self, X):
        """
        Compute the Sum of Absolute Errors (SAE) of dataset $X$ with respect to
        the current clustering model, a low SAE means a better quality

        Parameters
        ----------
        X : numpy.array
            Data set to be clustered, rows represent instances (points) and
            columns represent features (dimensions)

        Returns
        -------
        float
            Sum of Absolute Errors

        """
        X = np.asarray(X)
        if len(X.shape) == 1:
            X = X.reshape(1,-1)
        distances = pairwise_distances(X,
                                       self.model.pheno.L(),
                                       metric="l1",
                                       n_jobs=None)
        sae = distances.min(axis=1).sum()
        return(sae)

    def _predict_point_center(self, point):
        distances = pairwise_distances(point.reshape(1,-1),
                                       self.model.pheno.L(),
                                       metric="l1",
                                       n_jobs=None)
        distances = distances.flatten()
        y_index = np.argmin(distances)
        ae = distances[y_index]
        id_c = self.model.pheno._used_centers[y_index]
        center = self.model.pheno._possible_centers[id_c,:]
        distances_dimensions = np.abs(center - point)
        return(id_c, ae, distances_dimensions)

    def _choose_insertion(self, point):
        if np.random.random() > self.model.geno.G/(self.model.geno.G+1):
            c = self.model.pheno.empty_center_candidate()
            distances_dimensions = np.abs(point)
        else:
            c, ae, distances_dimensions = self._predict_point_center(point)
        # Choose insertion dim
        sum_distances = distances_dimensions.sum()
        if sum_distances:
            d = np.random.choice(self.D,p=distances_dimensions/sum_distances)
        else:
            d = np.random.randint(self.D)
        #d = np.random.randint(self.D)
        x = point[d]
        return(c,d,x)

    def _choose_deletion(self, point):
        candidate = self.model.geno.get_gene_candidate()
        return(candidate)

    def _insertion(self,point):
        self.model._candidate_insertion = self._choose_insertion(point)
        self.model.try_insertion()

    def _deletion(self,point):
        self.model._candidate_deletion = self._choose_deletion(point)
        self.model.try_deletion()

    def _model_candidate(self, point):
            if self.model.geno.G > self.Gmax:
                self._deletion(point)
            self._insertion(point)


    def fit(self, X, lazy=False, collector=False):
        """
        Build the SubCMedians model associated to dataset $X$

        Parameters
        ----------
        X : numpy.ndarray
            Data set to be clustered, rows represent instances (points) and
            columns represent features (dimensions)
        lazy: bool, default=False
            If true only tries to update the model iif the SAE increased when
            the datasample was updated, otherwise the optimization iteration is
            permormed at each sample update
        collector: bool, default=False
            If true all the models, and conserved modifications are kept.

        Returns
        -------
        subcmedians
            Fitted subcmedians instance

        """
        X = np.asarray(X)
        if self.random_state is not None:
            np.random.seed(self.random_state)
        industrius = (not lazy)
        if X.shape[0] < self.H:
            self.H = X.shape[0]-1
        self.S = X[:self.H,:].copy()
        self._sae_history = []
        self._nb_centers_history = []
        self._genome_size_history = []
        if collector:
            self.subspaces_history = []
            self.cluster_centers_history = []
            self.changes_accepted_history = []
            self.changes_history = []
            self.gain_sae_history = []
        i = self.H
        h = 0
        self._model_candidate(self.S[h])
        sae = self.sae_score(self.S)
        for t in tqdm(range(self.nb_iter)):
            # update dataset and SAE
            ae_old_point = self.sae_score(self.S[h,:])
            point = X[i,:]
            self.S[h,:] = point
            ae_new_point = self.sae_score(self.S[h,:])
            sae = sae - ae_old_point + ae_new_point
            # generate candidate
            if industrius or ae_old_point < ae_new_point:
                self._model_candidate(point)
            if collector:
                self.changes_history.append([self.model._candidate_deletion,
                                     self.model._candidate_insertion])
            sae_ = self.sae_score(self.S)
            gain = sae - sae_
            if gain >= 0:
                sae = sae_
                self.model.apply_changes()
                if collector:
                    self.changes_accepted_history.append(1)
            else:
                self.model.reverse_changes()
                if collector:
                    self.changes_accepted_history.append(0)
            self._sae_history.append(sae)
            self._nb_centers_history.append(self.model.geno.nb_centers)
            self._genome_size_history.append(self.model.geno.G)
            if collector:
                self.subspaces_history.append(self.model.geno.to_pandas())
                self.cluster_centers_history.append(self.model.pheno.to_pandas())
                self.gain_sae_history.append(gain)
            h = (h+1)%self.H
            i = (i+1)%X.shape[0]
        self.cluster_centers_ = self.model.get_cluster_centers()
        self.subspaces_ = self.model.get_cluster_subspaces()
        self.sae_ = sae
        return(self)
