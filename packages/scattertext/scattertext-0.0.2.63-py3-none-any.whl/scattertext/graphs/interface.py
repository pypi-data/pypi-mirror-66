import pandas as pd

from ..Scalers import dense_rank
from ..features.UseFullDocAsMetadata import UseFullDocAsMetadata
from ..CorpusFromParsedDocuments import CorpusFromParsedDocuments
from ..interface.ProduceScattertextExplorer import produce_scattertext_explorer
from . import SimpleDiGraph, ComponentDiGraphHTMLRenderer, GraphStructure


def produce_scattertext_digraph(
        df,
        text_col,
        source_col,
        dest_col,
        source_name='Source',
        dest_name='Destination',
        graph_width=500,
        graph_height=500,
        metadata_func=None,
        **kwargs,
):
    graph_df = pd.concat([
        df.assign(
            __text=lambda df: df[source_col],
            __alttext=lambda df: df[text_col],
            __category='source'
        ),
        df.assign(
            __text=lambda df: df[dest_col],
            __alttext=lambda df: df[text_col],
            __category='target'
        )
    ])

    corpus = CorpusFromParsedDocuments(
        graph_df,
        category_col='__category',
        parsed_col='__text',
        feats_from_spacy_doc=UseFullDocAsMetadata()
    ).build()

    edges = (corpus.get_df()[[source_col, dest_col]]
             .rename(columns={source_col: 'source', dest_col: 'target'})
             .drop_duplicates())

    component_graph = SimpleDiGraph(edges).make_component_digraph()

    graph_renderer = ComponentDiGraphHTMLRenderer(component_graph,
                                                  height=graph_height, width=graph_width)

    alternative_term_func = '''(function(termDict) {
        document.querySelectorAll(".dotgraph").forEach(svg => svg.style.display = 'none');
        showTermGraph(termDict['term']);
        return true;
    })'''

    scatterplot_structure = produce_scattertext_explorer(
        corpus,
        category='source',
        category_name=source_name,
        not_category_name=dest_name,
        minimum_term_frequency=0,
        pmi_threshold_coefficient=0,
        alternative_text_field='__alttext',
        use_non_text_features=True,
        transform=dense_rank,
        metadata=corpus.get_df().apply(metadata_func, axis=1) if metadata_func else None,
        return_scatterplot_structure=True,
        width_in_pixels=kwargs.get('width_in_pixels', 700),
        max_overlapping=kwargs.get('max_overlapping', 3),
        color_func=kwargs.get('color_func', '(function(x) {return "#5555FF"})'),
        alternative_term_func=alternative_term_func,
        **kwargs
    )

    html = GraphStructure(
        scatterplot_structure,
        graph_renderer=graph_renderer
    ).to_html()

    return html
