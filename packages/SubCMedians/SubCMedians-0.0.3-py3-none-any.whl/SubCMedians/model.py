import numpy as np
import pandas as pd
from SubCMedians.phenotype import Phenotype
from SubCMedians.genotype import Genotype

class Model:
    """
    Model Class

    Examples
    --------
    >>> m = Model(10,100)
    >>> m._candidate_insertion = (0,1,200)
    >>> m.try_insertion()
    >>> m.pheno.to_pandas()
    >>> m.geno.to_pandas()
    >>> m.apply_changes()
    >>> m._candidate_insertion = (1,9,20)
    >>> m.try_insertion()
    >>> m.apply_changes()
    >>> m._candidate_insertion = (1,9,8990)
    >>> m.try_insertion()
    >>> m.pheno.to_pandas()
    >>> m.reverse_changes()
    >>> m.pheno.to_pandas()
    >>> m._candidate_deletion = m.geno.get_gene_candidate()
    >>> m.try_deletion()
    >>> m.apply_changes()
    >>> m.pheno.to_pandas()
    >>> m.geno.to_pandas()
    >>> m._candidate_insertion = (0,1,20)
    >>> m.try_insertion()
    >>> m.apply_changes()
    >>> m.pheno.to_pandas()
    >>> m.geno.to_pandas()
    >>> m._candidate_deletion = m.geno.get_gene_candidate()
    >>> m._candidate_insertion = m._candidate_deletion[:2]+(666,)
    >>> m.try_deletion()
    >>> m.try_insertion()
    >>> m.apply_changes()
    >>> m.pheno.to_pandas()
    >>> m._candidate_insertion = (3,2,666,)
    >>> m.try_insertion()
    >>> m.apply_changes()
    >>> m.pheno.to_pandas()
    >>> m.geno.to_pandas()
    >>> m._candidate_deletion = m.geno.get_gene_candidate()
    >>> m.try_deletion()
    >>> m.pheno.to_pandas()
    >>> m.geno.to_pandas()
    >>> m._candidate_insertion = m._candidate_deletion[:2]+(999,)
    >>> m.try_insertion()
    >>> m.pheno.to_pandas()
    >>> m.geno.to_pandas()
    >>> m._candidate_deletion = (3, 2, 5)
    >>> m.try_deletion()
    >>> m.pheno.to_pandas()
    >>> m.geno.to_pandas()
    >>> m._candidate_insertion = m._candidate_deletion[:1]+(4,999,)
    >>> m.try_insertion()
    >>> m.apply_changes()

    """
    def __init__(self, D, capacity):
        self.pheno = Phenotype(D,capacity)
        self.geno = Genotype()
        self._candidate_deletion = None
        self._candidate_insertion = None

    def try_deletion(self):
        if self._candidate_deletion is not None:
            c,d,_ = self._candidate_deletion
            if self.geno.genes_counter[c][d] == 1:
                self.pheno.replace(c,d,0)
            if self.geno.center_counter[c] == 1:
                self.pheno.delete_center(c)

    def try_insertion(self):
        if self._candidate_insertion is not None:
            c,d,x = self._candidate_insertion
            self.pheno.replace(c,d,x)
            if c not in self.pheno._used_centers:
                self.pheno.add_center(c)

    def reverse_changes(self):
        self.pheno.reverse_changes()
        self._candidate_deletion = None
        self._candidate_insertion = None

    def apply_changes(self):
        self.pheno.apply_changes()
        if self._candidate_deletion is not None:
            self.geno.deletion(self._candidate_deletion)
        if self._candidate_insertion is not None:
            self.geno.insertion(self._candidate_insertion)
        self._candidate_deletion = None
        self._candidate_insertion = None

    def get_cluster_centers(self):
        cluster_centers_ = self.pheno.to_pandas()
        cluster_centers_.index = range(cluster_centers_.shape[0])
        return(cluster_centers_)

    def get_cluster_subspaces(self):
        subspaces_ = self.pheno.to_pandas() * 0
        subspaces_ += self.geno.to_pandas()
        subspaces_.index = range(subspaces_.shape[0])
        subspaces_ = subspaces_>0
        return(subspaces_)
