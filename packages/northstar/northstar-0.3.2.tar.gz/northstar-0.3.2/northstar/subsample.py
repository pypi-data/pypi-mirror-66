# vim: fdm=indent
# author:     Fabio Zanini
# date:       5/08/19
# content:    Atlas subsampling
__all__ = ['Subsample']

import warnings
import numpy as np
import pandas as pd
import leidenalg
from .fetch_atlas import AtlasFetcher

try:
    from anndata import AnnData
except ImportError:
    AnnData = None


class Subsample(object):
    '''Annotate new cell types using an even subsample of an atlas'''

    def __init__(
            self,
            atlas,
            n_features_per_cell_type=30,
            n_features_overdispersed=500,
            features_additional=None,
            n_pcs=20,
            n_neighbors=10,
            distance_metric='correlation',
            threshold_neighborhood=0.8,
            clustering_metric='cpm',
            resolution_parameter=0.001,
            normalize_counts=True,
            join='keep_first',
            ):
        '''Prepare the model for cell annotation

        Args:
            atlas (str, list of str, or dict): cell atlas to use. If a str,
             the corresponding cell atlas from:

             https://github.com/iosonofabio/atlas_averages/blob/master/table.tsv

             is fetched (check the first column for atlas names). If a list of
             str, multiple atlases will be fetched and combined. Only features
             that are in all atlases will be kept. If you use this feature, be
             careful to not mix atlases from different species. If a list of
             dict, it merges atlases as above but you can specify what cell
             types to fetch from each atlas. Each element of the list must be a
             dict with two key-value pairs: 'atlas_name' is the atlas name, and
             'cell_types' must be a list of cell types to retain. Example:
             atlas=[{'atlas_name': 'Enge_2017', 'cell_tpes': ['alpha']}] would
             load the atlas Enge_2017 and only retain alpha cells. If a dict,
             it can refer to two options. The first is a single atlas with a
             specification to retain only certain cell types. The format is as
             above, e.g. to select only alpha cells from Enge_2017 you can use:
             atlas={'atlas_name': 'Enge_2017', 'cell_tpes': ['alpha']}.
             The second option describes a custom cell atlas. In this case, the
             dict must have two entries, 'cell_types' and 'counts'.
             'cell_types' is a pandas Series with the cell names as
             index and the cell types to use for each cell as values.
             'counts' is a pandas.DataFrame or an anndata.AnnData structure.
             If a DataFrame, it must have features as rows and cell names as
             columns; if an AnnData, it is reversed (AnnData uses a
             different convention) and it must have the cell types as rows
             (obs_names) and the features as columns (var_names). If an AnnData,
             it will be converted into a DataFrame.

            n_features_per_cell_type (int): number of features marking each
             fixed column (atlas cell type).

            n_features_overdispersed (int): number of unbiased, overdispersed
             features from the last N - n_fixed columns.

            features_additional (list of str or None): additional features to
             keep on top of automatic selection. The argument 'features' takes
             priority over this one.

            n_pcs (int): number of principal components to keep in the PCA

            n_neighbors (int): number of neighbors in the similarity graph

            distance_metric (str): metric to use as distance. It should be a
             metric accepted by scipy.spatial.distance.cdist.

            threshold_neighborhood (float): do not consider distances larger
             than this as neighbors

            clustering_metric (str): 'cpm' (default, Cell Potts Model) or
             'modularity'. Sets the type of partition used in the clustering
             step.

            resolution_parameter (float): number between 0 and 1 that sets
             how easy it is for the clustering algorithm to make new clusters

            normalize_counts (bool): whether to renormalize the counts at the
             merging stage to make sure atlas and new data follow the same
             normalization. Be careful if you turn this off.

            join (str): must be 'keep_first', 'union', or 'intersection'. This
             argument is used when sourcing multiple atlases and decides what
             to do with features that are not present in all atlases.
             'keep_first' keeps the features in the first atlas and pads the
             other atlases with zeros, 'union' pads every atlas that is missing
             a feature and 'intersection' only keep features that are in all
             atlases.
        '''

        self.atlas = atlas
        self.n_features_per_cell_type = n_features_per_cell_type
        self.n_features_overdispersed = n_features_overdispersed
        self.features_additional = features_additional
        self.n_pcs = n_pcs
        self.n_neighbors = n_neighbors
        self.distance_metric = distance_metric
        self.threshold_neighborhood = threshold_neighborhood
        self.clustering_metric = clustering_metric
        self.resolution_parameter = resolution_parameter
        self.normalize_counts = normalize_counts
        self.join = join

    def fit(self, new_data):
        '''Run with subsamples of the atlas

        Args:
            new_data (pandas.DataFrame or anndata.AnnData): the new data to be
             clustered. If a dataframe, t must have features as rows and
             cell names as columns (as in loom files). anndata uses the opposite
             convention, so it must have cell names as rows (obs_names) and
             features as columns (var_names) and this class will transpose it.

        Returns:
            None, but this instance of Subsample acquired the property
            `membership` containing the cluster memberships (cell types) of the
            columns except the first n_fixed. The first n_fixed columns are
            assumes to have distinct memberships in the range [0, n_fixed - 1].
        '''
        self.new_data = new_data

        self._check_init_arguments()
        self.fetch_atlas_if_needed()
        self.compute_feature_intersection()
        self._check_feature_intersection()
        self.prepare_feature_selection()
        self.select_features()
        self._check_feature_selection()
        self.merge_atlas_newdata()
        self.compute_pca()
        self.compute_similarity_graph()
        self.cluster_graph()

    def fit_transform(self, new_data):
        '''Run with subsamples of the atlas and return the cell types

        Args:
            new_data (pandas.DataFrame or anndata.AnnData): the new data to be
             clustered. If a dataframe, t must have features as rows and
             cell names as columns (as in loom files). anndata uses the opposite
             convention, so it must have cell names as rows (obs_names) and
             features as columns (var_names) and this class will transpose it.

        Returns:
            the cluster memberships (cell types) of the
            columns except the first n_fixed. The first n_fixed columns are
            assumes to have distinct memberships in the range [0, n_fixed - 1].
        '''
        self.fit(new_data)
        return self.membership

    def _check_init_arguments(self):
        # Custom atlas
        at = self.atlas

        if isinstance(at, str):
            pass
        elif isinstance(at, list) or isinstance(at, tuple):
            for elem in at:
                if isinstance(elem, str):
                    pass
                elif isinstance(elem, dict):
                    if 'atlas_name' not in elem:
                        raise ValueError('List of atlases: format incorrect')
                    if 'cell_types' not in elem:
                        raise ValueError('List of atlases: format incorrect')
                else:
                    raise ValueError('List of atlases: format incorrect')

        elif isinstance(at, dict) and ('atlas_name' in at) and \
                ('cell_types' in at):
            pass

        # Custom atlas
        elif isinstance(at, dict):
            if not isinstance(at, dict):
                raise ValueError('atlas must be a dict')
            if 'counts' not in at:
                raise ValueError('atlas must have a "counts" key')
            if 'cell_types' not in at:
                raise ValueError('atlas must have a "cell_types" key')

            # The counts can be pandas.DataFrame or anndata.AnnData
            if not isinstance(at['counts'], pd.DataFrame):
                if AnnData is None:
                    raise ValueError('atlas["counts"] must be a DataFrame')
                elif not isinstance(at['counts'], AnnData):
                    raise ValueError('atlas["counts"] must be a DataFrame'
                                     ' or AnnData object')

                # AnnData uses features as columns, to transpose and convert
                at['counts'] = at['counts'].T.to_df()

            # even within AnnData, metadata colunms are pandas.DataFrame
            if not isinstance(at['cell_types'], pd.Series):
                raise ValueError('atlas["cell_types"] must be a pd.Series')
            if at['counts'].shape[1] != at['cell_types'].shape[0]:
                raise ValueError(
                    'atlas counts and cell_types must have the same cells')
            if (at['counts'].columns != at['cell_types'].index).any():
                raise ValueError(
                    'atlas counts and cell_types must have the same cells')

        # Make sure new data is a dataframe
        nd = self.new_data
        if not isinstance(nd, pd.DataFrame):
            if AnnData is None:
                raise ValueError('new data must be a DataFrame')
            elif not isinstance(nd, AnnData):
                raise ValueError('new_data must be a DataFrame'
                                 ' or AnnData object')

            # AnnData uses features as columns, to transpose and convert
            self.new_data = nd = nd.T.to_df()

        # New data could be too small to to PCA
        n_newgenes, n_newcells = self.new_data.shape
        if n_newgenes < self.n_pcs:
            warnings.warn('The number of features in the new data is on the small end, northstar might give inaccurate results')

        if n_newcells < self.n_pcs:
            warnings.warn('The number of cells in the new data is on the small end, northstar might give inaccurate results')

        if min(n_newgenes, n_newcells) < self.n_pcs:
            self.n_pcs = min(n_newgenes, n_newcells)

        # New data could be too small for knn
        if n_newcells < self.n_neighbors + 1:
            warnings.warn('The number of cells in the new data is on the small end, reducing the number of graph neighbors')
            self.n_neighbors = max(1, n_newcells - 1)

        nf1 = self.n_features_per_cell_type
        nf2 = self.n_features_overdispersed
        nf3 = self.features_additional
        if not isinstance(nf1, int):
            raise ValueError('n_features_per_cell_type must be an int >= 0')
        if not isinstance(nf1, int):
            raise ValueError('n_features_overdispersed must be an int >= 0')
        if (nf1 < 1) and (nf2 < 1) and (nf3 < 1):
            raise ValueError('No features selected')

    def _check_feature_intersection(self):
        L = len(self.features_ovl)
        if L == 0:
            raise ValueError(
                'No overlapping features in atlas and new data, are gene names correct for this species?')
        if L < 50:
            warnings.warn(
                'Only {:} overlapping features found in atlas and new data'.format(L))

    def _check_feature_selection(self):
        L = len(self.features)
        if L == 0:
            raise ValueError(
                'No features selected, check nortstar parameters')
        if L < self.n_pcs:
            warnings.warn(
                'Only {:} features selected, reducing PCA to those number of components'.format(L))
            self.n_pcs = L

    def fetch_atlas_if_needed(self):
        '''Fetch atlas(es) if needed'''
        at = self.atlas

        if isinstance(at, str):
            self.atlas = AtlasFetcher().fetch_atlas(
                    at,
                    kind='subsample',
                    )

        elif isinstance(at, list) or isinstance(self.atlas, tuple):
            self.atlas = AtlasFetcher().fetch_multiple_atlases(
                    at,
                    kind='subsample',
                    join=self.join,
                    )

        elif isinstance(at, dict) and ('atlas_name' in at) and \
                ('cell_types' in at):
            self.atlas = AtlasFetcher().fetch_atlas(
                    at['atlas_name'],
                    kind='subsample',
                    cell_types=at['cell_types'],
                    )

    def compute_feature_intersection(self):
        '''Calculate the intersection of features between atlas and new data'''
        # Intersect features
        self.features_atlas = self.atlas['counts'].index.values
        self.features_newdata = self.new_data.index.values
        self.features_ovl = np.intersect1d(
                self.features_atlas,
                self.features_newdata,
                )

    def prepare_feature_selection(self):
        # Cell names and types
        self.cell_types_atlas = self.atlas['cell_types'].values
        self.cell_names_atlas = self.atlas['counts'].columns.values
        self.cell_names_newdata = self.new_data.columns.copy()

        # Numbers
        self.n_atlas = self.atlas['counts'].shape[1]
        self.n_newdata = self.new_data.shape[1]
        self.n_total = self.n_atlas + self.n_newdata

    def select_features(self):
        '''Select features that define heterogeneity of the atlas and new data

        Returns:
            ndarray of feature names.
        '''
        features_atlas = self.features_atlas
        features_newdata = self.features_newdata
        features_ovl = list(self.features_ovl)
        features_add = self.features_additional

        nf1 = self.n_features_per_cell_type
        nf2 = self.n_features_overdispersed

        cell_types = self.cell_types_atlas
        cell_typesu = list(np.unique(cell_types))

        features = set()

        # Atlas markers
        if len(cell_typesu) > 1:
            matrix = self.atlas['counts'].values
            for au in cell_typesu:
                icol1 = (cell_types == au).nonzero()[0]
                icol2 = (cell_types != au).nonzero()[0]
                ge1 = matrix[:, icol1].mean(axis=1)
                ge2 = matrix[:, icol2].mean(axis=1)
                fold_change = np.log2(ge1 + 0.1) - np.log2(ge2 + 0.1)
                tmp = np.argsort(fold_change)[::-1]
                ind_markers_atlas = []
                for i in tmp:
                    if features_atlas[i] in features_ovl:
                        ind_markers_atlas.append(i)
                    if len(ind_markers_atlas) == nf1:
                        break
                # Add atlas markers
                features |= set(features_atlas[ind_markers_atlas])

        # Unbiased on new data
        if nf2 > 0:
            if nf2 >= len(features_ovl):
                features |= set(features_ovl)
            else:
                matrix = self.new_data.values
                nd_mean = matrix.mean(axis=1)
                nd_var = matrix.var(axis=1)
                fano = (nd_var + 1e-10) / (nd_mean + 1e-10)
                tmp = np.argsort(fano)[::-1]
                ind_ovd_newdata = []
                for i in tmp:
                    if features_newdata[i] in features_ovl:
                        ind_ovd_newdata.append(i)
                    if len(ind_ovd_newdata) == nf2:
                        break
                # Add overdispersed features
                features |= set(features_newdata[ind_ovd_newdata])

        # Additional features
        if features_add is not None:
            features |= (set(features_add) & set(features_ovl))

        self.features = np.array(list(features))

    def merge_atlas_newdata(self):
        '''Merge atlas data and the new data after feature selection

        NOTE: is self.normalize is True, the merged count matrix is normalized
        by 1 million total counts.
        '''

        features = self.features
        L = len(features)
        N = self.n_total
        N1 = self.n_atlas
        matrix = np.empty((L, N), dtype=np.float32)

        # Find the feature indices for atlas
        ind_features_atlas = pd.Series(
            np.arange(len(self.features_atlas)),
            index=self.features_atlas,
            ).loc[features].values
        matrix[:, :N1] = self.atlas['counts'].values[ind_features_atlas]

        # Find the feature indices for new data
        ind_features_newdata = pd.Series(
            np.arange(len(self.features_newdata)),
            index=self.features_newdata,
            ).loc[features].values
        matrix[:, N1:] = self.new_data.values[ind_features_newdata]

        # The normalization function also sets pseudocounts
        if self.normalize_counts:
            matrix *= 1e6 / (matrix.sum(axis=0) + 0.1)

        self.matrix = matrix

    def compute_pca(self):
        '''Compute k nearest neighbors from a matrix with fixed nodes

        Returns:
            list of lists with the first k or less indices of the neighbors for
            each free column. The length is N - n_fixed. For each now, there are
            less than k entries if no other column within the distance threshold
            were found, or if N < k.


        The algorithm proceeds as follows:
        1. whiten the matrix, i.e. subtract the mean along
        the observation axis (N) and divide by the standard dev along the same axis
        2. calculate the weighted covariance matrix
        3. calculate normal PCA on that matrix
        '''
        from sklearn.decomposition import PCA

        matrix = self.matrix
        n_fixed = self.n_atlas
        n_pcs = self.n_pcs

        # Test input arguments
        L, N = matrix.shape
        if n_fixed >= N:
            raise ValueError('n_fixed larger or equal matrix number of columns')
        if n_pcs > min(L, N):
            raise ValueError('n_pcs greater than smaller matrix dimension, those eigenvalues are zero')

        # 0. take log
        matrix = np.log10(matrix + 0.1)

        # 1. whiten
        Xnorm = ((matrix.T - matrix.mean(axis=1)) / matrix.std(axis=1, ddof=0)).T

        # take care of non-varying components
        Xnorm[np.isnan(Xnorm)] = 0

        # 2. PCA
        pca = PCA(n_components=n_pcs)
        # rvects columns are the right singular vectors
        rvects = pca.fit_transform(Xnorm.T)

        self.pca_data = {
            'pcs': rvects,
            'cell_type': np.array(list(self.cell_types_atlas) + [''] * (N - n_fixed)),
            'n_atlas': n_fixed,
            }

    def compute_similarity_graph(self):
        '''Compute similarity graph from the extended PC space

        1. calculate the distance matrix
        2. calculate neighborhoods
        3. construct similarity graph from neighborhood lists
        '''
        from scipy.spatial.distance import pdist, squareform
        import igraph as ig

        matrix = self.matrix
        k = self.n_neighbors
        metric = self.distance_metric
        threshold = self.threshold_neighborhood
        rvects = self.pca_data['pcs']
        L, N = matrix.shape

        # 1. calculate distance matrix
        # rvects is N x n_pcs. Let us calculate the end that includes only the free
        # observations and then call cdist which kills the columns. The resulting
        # matrix has dimensions N1 x N
        dmat = squareform(pdist(rvects, metric=metric))
        dmax = dmat.max()

        # 2. calculate neighbors
        neighbors = [[] for n1 in range(N)]
        for i, drow in enumerate(dmat):
            nbi = neighbors[i]
            # set distance to self as a high number, to avoid self
            drow[i] = dmax + 1

            # Find largest k negative distances (k neighbors)
            ind = np.argpartition(-drow, -k)[-k:]

            # Discard the ones beyond threshold
            ind = ind[drow[ind] <= threshold]

            # Indices are not sorted within ind, we sort them to help
            # debugging even though it is not needed
            ind = ind[np.argsort(drow[ind])]

            nbi.extend(list(ind))

        self.neighbors = neighbors

        # Construct graph from the lists of neighbors
        edges_d = set()
        for i, neis in enumerate(neighbors):
            for n in neis:
                edges_d.add(frozenset((i, n)))

        edges = [tuple(e) for e in edges_d]
        self.graph = ig.Graph(n=N, edges=edges, directed=False)

    def cluster_graph(self):
        '''Compute communities from a matrix with fixed nodes

        Returns:
            None, but Subsample.membership is set as an array of int with
            size N - n_fixed with the community/cluster membership of all
            columns except the first n_fixed ones.
        '''
        opt = leidenalg.Optimiser()

        matrix = self.matrix
        aa = self.cell_types_atlas
        aau = list(np.unique(aa))
        n_fixed = self.n_atlas
        clustering_metric = self.clustering_metric
        resolution_parameter = self.resolution_parameter
        g = self.graph

        L, N = matrix.shape

        # NOTE: initial membership is singletons except for atlas nodes, which
        # get the membership they have.
        aaun = len(aau)
        initial_membership = []
        for j in range(N):
            if j < self.n_atlas:
                mb = aau.index(aa[j])
            else:
                mb = aaun + (j - n_fixed)
            initial_membership.append(mb)

        # Compute communities with semi-supervised Leiden
        if clustering_metric == 'cpm':
            partition = leidenalg.CPMVertexPartition(
                    g,
                    resolution_parameter=resolution_parameter,
                    initial_membership=initial_membership,
                    )
        elif clustering_metric == 'modularity':
            partition = leidenalg.ModularityVertexPartition(
                    g,
                    resolution_parameter=resolution_parameter,
                    initial_membership=initial_membership,
                    )
        else:
            raise ValueError(
                'clustering_metric not understood: {:}'.format(clustering_metric))

        fixed_nodes = [int(i < n_fixed) for i in range(N)]
        opt.optimise_partition(partition, fixed_nodes=fixed_nodes)
        membership = partition.membership[n_fixed:]

        # Convert the known cell types
        lstring = len(max(self.cell_types_atlas, key=len))
        self.membership = np.array(
                [str(x) for x in membership],
                dtype='U{:}'.format(lstring))
        for i, ct in enumerate(aau):
            self.membership[self.membership == str(i)] = ct

    def estimate_closest_atlas_cell_type(self):
        '''Estimate atlas cell type closest to each new cluster'''
        from scipy.spatial.distance import cdist

        matrix = self.matrix
        n_fixed = self.n_atlas
        metric = self.distance_metric
        cell_types = self.cell_types_atlas

        # Calculate averages for the new clusters
        ct_new = list(set(self.membership) - set(cell_types))
        N = len(ct_new)
        L = matrix.shape[0]
        avg_new = np.empty((L, N), np.float32)
        for i, ct in enumerate(ct_new):
            avg_new[i] = self.matrix[:, self.membership == ct].mean(axis=1)

        avg_atl = np.empty((L, len(cell_types)), np.float32)
        for i, ct in enumerate(cell_types):
            avg_atl[i] = self.matrix[:, self.membership[:n_fixed] == ct].mean(axis=1)

        # Calculate distance matrix between new and old in the high-dimensional
        # feature-selected space
        dmat = cdist(avg_new, avg_atl, metric=metric)

        # Pick the closest
        closest = np.argmin(dmat, axis=1)

        # Give it actual names
        closest = pd.Series(cell_types[closest], index=ct_new)

        return closest

    def embed(self, method='tsne', **kwargs):
        X = self.pca_data['pcs']
        index = list(self.cell_names_atlas) + list(self.cell_names_newdata)

        if method == 'pca':
            emb = X[:, :2]
        elif method == 'tsne':
            from sklearn.manifold import TSNE
            kwargs['perplexity'] = kwargs.get('perplexity', 30)
            model = TSNE(
                n_components=2,
                **kwargs,
                )
            emb = model.fit_transform(X)
        elif method == 'umap':
            from umap import UMAP
            model = UMAP(
                n_components=2,
                **kwargs,
                )
            emb = model.fit_transform(X)

        res = pd.DataFrame(
            emb,
            index=index,
            columns=['Dimension 1', 'Dimension 2'],
            )
        return res
