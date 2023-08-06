import numpy as np
import pandas as pd

class Genotype:
    """
    Genotype class

    Examples
    --------
    >>> np.random.seed(0)
    >>> g = Genotype()
    >>> g.insertion((3,4,9))
    >>> g.insertion((3,4,99))
    >>> g.nb_centers
    1
    >>> g.insertion((3,40,7))
    >>> g.insertion((1,40,90))
    >>> g.genes
    {(1, 40, 3), (3, 4, 0), (3, 4, 1), (3, 40, 2)}
    >>> g.to_pandas()
        4    40
    3  2.0  1.0
    1  NaN  1.0
    >>> g.nb_centers
    2
    >>> g.G
    4
    >>> candidate = g.get_gene_candidate()
    >>> candidate
    (3, 40, 2)
    >>> g.deletion(candidate)
    >>> g.G
    3
    >>> g.genes
    {(1, 40, 3), (3, 4, 0), (3, 4, 1)}
    >>> g.to_pandas()
        4    40
    3  2.0  NaN
    1  NaN  1.0
    >>> g.deletion(g.get_gene_candidate())
    >>> g.deletion(g.get_gene_candidate())
    >>> g.deletion(g.get_gene_candidate())
    Empty DataFrame
    Columns: []
    Index: []
    """
    def __init__(self):
        self.genes = set()
        self.candidate_del = None
        self._t = 0
        self.genes_counter = {}
        self.center_counter = {}
        self.G = 0
        self.nb_centers = 0

    def deletion(self, gene):
        """
        Delete a gene from the genome

        Parameters
        ----------
        gene : tuple
            Tuple containing 3 elements: the cluster id, the feature id and an id
        """
        c,d,_ = gene
        self.genes.remove(gene)
        self.genes_counter[c][d] -= 1
        self.center_counter[c] -= 1
        self.G -= 1
        if not self.genes_counter[c][d]:
            self.genes_counter[c].pop(d)
        if not self.center_counter[c]:
            self.nb_centers -= 1
            self.center_counter.pop(c)
            self.genes_counter.pop(c)

    def insertion(self,gene):
        """
        Insert a new gene into the genome

        Parameters
        ----------
        gene : tuple
            Tuple containing 3 elements: the cluster id, the feature id and a
            coordinate
        """
        c,d,_ = gene
        self.genes.add((c,d,self._t,))
        if c not in self.center_counter:
            self.center_counter[c] = 0
            self.genes_counter[c] = {}
            self.nb_centers += 1
        if d not in self.genes_counter[c]:
            self.genes_counter[c][d] = 0
        self.center_counter[c] += 1
        self.genes_counter[c][d] += 1
        self.G += 1
        self._t += 1

    def get_gene_candidate(self):
        """
        Return a random gene from the genome
        """
        candidate = self.genes.pop()
        self.genes.add(candidate)
        return(candidate)

    def get_non_empty_dims(self,c):
        if c in self.genes_counter:
            return(self.genes_counter[c].keys())

    def search_gene(self,c,d):
        for g in self.genes:
            if g[0] == c and g[1] == d:
                return(g)

    def to_pandas(self,index=None,columns=None):
        """
        Convert the genome in a pandas data frame

        Parameters
        ----------
        index : numpy.ndarray or list, default=None
            list containing the index name
        columns : numpy.ndarray or list, default=None
            list containing the columns name

        Returns
        -------
        pandas.DataFrame
            Data Frame containing the genome information: index represent
            centers, while columns denote features
        """
        return pd.DataFrame(self.genes_counter,index,columns).T
