import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph._traversal import connected_components

from scattertext.graphs.SimpleDiGraph import SimpleDiGraph


class SimpleDiGraphBase(object):
    def get_connected_subgraph_df(self):
        return pd.DataFrame({'component': self.get_connected_components(),
                             'nodes': self.node_df['index'].values,
                             'values': self.node_df.index}
                            ).groupby('component').agg(list).assign(
            size=lambda df: df.nodes.apply(len)
        ).sort_values(by='size', ascending=False).reset_index(drop=True)

    def get_connected_components(self):
        return connected_components(self.get_sparse_graph(), True)[1]

    def get_sparse_graph(self):
        return csr_matrix(
            (np.ones(len(self.edge_df)),
             (self.edge_df.source_id.values, self.edge_df.target_id.values)),
            shape=(len(self.node_df), len(self.node_df))
        )

    def limit_nodes(self, nodes):
        return SimpleDiGraph(self.edge_df[
                                 self.edge_df.target_id.isin(nodes) | self.edge_df.source_id.isin(nodes)
                                 ][['source', 'target']])