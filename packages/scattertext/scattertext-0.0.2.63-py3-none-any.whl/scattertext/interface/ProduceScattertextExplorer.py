import warnings

from scattertext import DEFAULT_MINIMUM_TERM_FREQUENCY, DEFAULT_PMI_THRESHOLD_COEFFICIENT, percentile_alphabetical, \
    termranking, get_category_names, get_term_scorer_scores, ScatterChartExplorer, get_semiotic_square_html, \
    ScatterplotStructure, VizDataAdapter, BasicHTMLFromScatterplotStructure


def produce_scattertext_explorer(corpus,
                                 category,
                                 category_name=None,
                                 not_category_name=None,
                                 protocol='https',
                                 pmi_threshold_coefficient=DEFAULT_MINIMUM_TERM_FREQUENCY,
                                 minimum_term_frequency=DEFAULT_PMI_THRESHOLD_COEFFICIENT,
                                 minimum_not_category_term_frequency=0,
                                 max_terms=None,
                                 filter_unigrams=False,
                                 height_in_pixels=None,
                                 width_in_pixels=None,
                                 max_snippets=None,
                                 max_docs_per_category=None,
                                 metadata=None,
                                 scores=None,
                                 x_coords=None,
                                 y_coords=None,
                                 original_x=None,
                                 original_y=None,
                                 rescale_x=None,
                                 rescale_y=None,
                                 singleScoreMode=False,
                                 sort_by_dist=False,
                                 reverse_sort_scores_for_not_category=True,
                                 use_full_doc=False,
                                 transform=percentile_alphabetical,
                                 jitter=0,
                                 gray_zero_scores=False,
                                 term_ranker=None,
                                 asian_mode=False,
                                 match_full_line=False,
                                 use_non_text_features=False,
                                 show_top_terms=True,
                                 show_characteristic=True,
                                 word_vec_use_p_vals=False,
                                 max_p_val=0.1,
                                 p_value_colors=False,
                                 term_significance=None,
                                 save_svg_button=False,
                                 x_label=None,
                                 y_label=None,
                                 d3_url=None,
                                 d3_scale_chromatic_url=None,
                                 pmi_filter_thresold=None,
                                 alternative_text_field=None,
                                 terms_to_include=None,
                                 semiotic_square=None,
                                 num_terms_semiotic_square=None,
                                 not_categories=None,
                                 neutral_categories=[],
                                 extra_categories=[],
                                 show_neutral=False,
                                 neutral_category_name=None,
                                 get_tooltip_content=None,
                                 x_axis_values=None,
                                 y_axis_values=None,
                                 x_axis_values_format=None,
                                 y_axis_values_format=None,
                                 color_func=None,
                                 term_scorer=None,
                                 show_axes=True,
                                 show_axes_and_cross_hairs=False,
                                 horizontal_line_y_position=None,
                                 vertical_line_x_position=None,
                                 show_cross_axes=True,
                                 show_extra=False,
                                 extra_category_name=None,
                                 censor_points=True,
                                 center_label_over_points=False,
                                 x_axis_labels=None,
                                 y_axis_labels=None,
                                 topic_model_term_lists=None,
                                 topic_model_preview_size=10,
                                 metadata_descriptions=None,
                                 vertical_lines=None,
                                 characteristic_scorer=None,
                                 term_colors=None,
                                 unified_context=False,
                                 show_category_headings=True,
                                 include_term_category_counts=False,
                                 div_name=None,
                                 alternative_term_func=None,
                                 term_metadata=None,
                                 max_overlapping=-1,
                                 include_all_contexts=False,
                                 return_data=False,
                                 return_scatterplot_structure=False):
    '''Returns html code of visualization.

    Parameters
    ----------
    corpus : Corpus
        Corpus to use.
    category : str
        Name of category column as it appears in original data frame.
    category_name : str
        Name of category to use.  E.g., "5-star reviews."
        Optional, defaults to category name.
    not_category_name : str
        Name of everything that isn't in category.  E.g., "Below 5-star reviews".
        Optional defaults to "N(n)ot " + category_name, with the case of the 'n' dependent
        on the case of the first letter in category_name.
    protocol : str, optional
        Protocol to use.  Either http or https.  Default is https.
    pmi_threshold_coefficient : int, optional
        Filter out bigrams with a PMI of < 2 * pmi_threshold_coefficient. Default is 6
    minimum_term_frequency : int, optional
        Minimum number of times word needs to appear to make it into visualization.
    minimum_not_category_term_frequency : int, optional
      If an n-gram does not occur in the category, minimum times it
       must been seen to be included. Default is 0.
    max_terms : int, optional
        Maximum number of terms to include in visualization.
    filter_unigrams : bool, optional
        Default False, do we filter out unigrams that only occur in one bigram
    width_in_pixels : int, optional
        Width of viz in pixels, if None, default to JS's choice
    height_in_pixels : int, optional
        Height of viz in pixels, if None, default to JS's choice
    max_snippets : int, optional
        Maximum number of snippets to show when term is clicked.  If None, all are shown.
    max_docs_per_category: int, optional
        Maximum number of documents to store per category.  If None, by default, all are stored.
    metadata : list, optional
        list of meta data strings that will be included for each document
    scores : np.array, optional
        Array of term scores or None.
    x_coords : np.array, optional
        Array of term x-axis positions or None.  Must be in [0,1].
        If present, y_coords must also be present.
    y_coords : np.array, optional
        Array of term y-axis positions or None.  Must be in [0,1].
        If present, x_coords must also be present.
    original_x : array-like
        Original, unscaled x-values.  Defaults to x_coords
    original_y : array-like
        Original, unscaled y-values.  Defaults to y_coords
    rescale_x : lambda list[0,1]: list[0,1], optional
        Array of term x-axis positions or None.  Must be in [0,1].
        Rescales x-axis after filtering
    rescale_y : lambda list[0,1]: list[0,1], optional
        Array of term y-axis positions or None.  Must be in [0,1].
        Rescales y-axis after filtering
    singleScoreMode : bool, optional
        Label terms based on score vs distance from corner.  Good for topic scores. Show only one color.
    sort_by_dist: bool, optional
        Label terms based distance from corner. True by default.  Negated by singleScoreMode.
    reverse_sort_scores_for_not_category: bool, optional
        If using a custom score, score the not-category class by
        lowest-score-as-most-predictive. Turn this off for word vector
        or topic similarity. Default True.
    use_full_doc : bool, optional
        Use the full document in snippets.  False by default.
    transform : function, optional
        not recommended for editing.  change the way terms are ranked.  default is st.Scalers.percentile_ordinal
    jitter : float, optional
        percentage of axis to jitter each point.  default is 0.
    gray_zero_scores : bool, optional
        If True, color points with zero-scores a light shade of grey.  False by default.
    term_ranker : TermRanker, optional
        TermRanker class for determining term frequency ranks.
    asian_mode : bool, optional
        Use a special Javascript regular expression that's specific to chinese or japanese
    match_full_line : bool, optional
        Has the javascript regex match the full line instead of part of it
    use_non_text_features : bool, optional
        Show non-bag-of-words features (e.g., Empath) instead of text.  False by default.
    show_top_terms : bool, default True
        Show top terms on the left-hand side of the visualization
    show_characteristic: bool, default True
        Show characteristic terms on the far left-hand side of the visualization
    word_vec_use_p_vals: bool, default False
        Sort by harmonic mean of score and distance.
    max_p_val : float, default 0.1
        If word_vec_use_p_vals, the minimum p val to use.
    p_value_colors : bool, default False
      Color points differently if p val is above 1-max_p_val, below max_p_val, or
       in between.
    term_significance : TermSignificance instance or None
        Way of getting signfiance scores.  If None, p values will not be added.
    save_svg_button : bool, default False
        Add a save as SVG button to the page.
    x_label : str, default None
        Custom x-axis label
    y_label : str, default None
        Custom y-axis label
    d3_url, str, None by default.  The url (or path) of d3.
        URL of d3, to be inserted into <script src="..."/>.  Overrides `protocol`.
      By default, this is `DEFAULT_D3_URL` declared in `ScatterplotStructure`.
    d3_scale_chromatic_url, str, None by default.  Overrides `protocol`.
      URL of d3 scale chromatic, to be inserted into <script src="..."/>
      By default, this is `DEFAULT_D3_SCALE_CHROMATIC` declared in `ScatterplotStructure`.
    pmi_filter_thresold : (DEPRECATED) int, None by default
      DEPRECATED.  Use pmi_threshold_coefficient instead.
    alternative_text_field : str or None, optional
        Field in from dataframe used to make corpus to display in place of parsed text. Only
        can be used if corpus is a ParsedCorpus instance.
    terms_to_include : list or None, optional
        Whitelist of terms to include in visualization.
    semiotic_square : SemioticSquareBase
        None by default.  SemioticSquare based on corpus.  Includes square above visualization.
    num_terms_semiotic_square : int
        10 by default. Number of terms to show in semiotic square.
        Only active if semiotic square is present.
    not_categories : list
        All categories other than category by default.  Documents labeled
        with remaining category.
    neutral_categories : list
        [] by default.  Documents labeled neutral.
    extra_categories : list
        [] by default.  Documents labeled extra.
    show_neutral : bool
        False by default.  Show a third column listing contexts in the
        neutral categories.
    neutral_category_name : str
        "Neutral" by default. Only active if show_neutral is True.  Name of the neutral
        column.
    get_tooltip_content : str
        Javascript function to control content of tooltip.  Function takes a parameter
        which is a dictionary entry produced by `ScatterChartExplorer.to_dict` and
        returns a string.
    x_axis_values : list, default None
        Value-labels to show on x-axis. Low, medium, high are defaults.
    y_axis_values : list, default None
        Value-labels to show on y-axis. Low, medium, high are defaults.
    x_axis_values_format : str, default None
        d3 format of x-axis values
    y_axis_values_format : str, default None
        d3 format of y-axis values
    color_func : str, default None
        Javascript function to control color of a point.  Function takes a parameter
        which is a dictionary entry produced by `ScatterChartExplorer.to_dict` and
        returns a string.
    term_scorer : Object, default None
        In lieu of scores, object with a get_scores(a,b) function that returns a set of scores,
        where a and b are term counts.  Scorer optionally has a get_term_freqs function. Also could be a
        CorpusBasedTermScorer instance.
    show_axes : bool, default True
        Show the ticked axes on the plot.  If false, show inner axes as a crosshair.
    show_axes_and_cross_hairs : bool, default False
        Show both peripheral axis labels and cross axes.
    vertical_line_x_position : float, default None
    horizontal_line_y_position : float, default None
    show_cross_axes : bool, default True
        If show_axes is False, do we show cross-axes?
    show_extra : bool
        False by default.  Show a fourth column listing contexts in the
        extra categories.
    extra_category_name : str, default None
        "Extra" by default. Only active if show_neutral is True and show_extra is True.  Name
        of the extra column.
    censor_points : bool, default True
        Don't label over points.
    center_label_over_points : bool, default False
        Center a label over points, or try to find a position near a point that
        doesn't overlap anything else.
    x_axis_labels: list, default None
        List of string value-labels to show at evenly spaced intervals on the x-axis.
        Low, medium, high are defaults.
    y_axis_labels : list, default None
        List of string value-labels to show at evenly spaced intervals on the y-axis.
        Low, medium, high are defaults.
    topic_model_term_lists : dict default None
        Dict of metadata name (str) -> List of string terms in metadata. These will be bolded
        in query in context results.
    topic_model_preview_size : int default 10
        Number of terms in topic model to show as a preview.
    metadata_descriptions : dict default None
        Dict of metadata name (str) -> str of metadata description. These will be shown when a meta data term is
        clicked.
    vertical_lines : list default None
        List of floats corresponding to points on the x-axis to draw vertical lines
    characteristic_scorer : CharacteristicScorer default None
        Used for bg scores
    term_colors : dict, default None
        Dictionary mapping term to color
    unified_context : bool, default False
        Boolean displays contexts in a single pane as opposed to separate columns.
    show_category_headings : bool, default True
        Show category headings if unified_context is True.
    include_term_category_counts : bool, default False
        Include the termCounts object in the plot definition.
    div_name : str, None by default
        Give the scatterplot div name a non-default value
    alternative_term_func: str, default None
        Javascript function which take a term JSON object and returns a bool.  If the return value is true,
        execute standard term click pipeline. Ex.: `'(function(termDict) {return true;})'`.
    term_metadata : dict, None by default
        Dict mapping terms to dictionaries containing additional information which can be used in the color_func
        or the get_tooltip_content function. These will appear in termDict.etc
    include_all_contexts: bool, default False
        Include all contexts, even non-matching ones, in interface
    max_overlapping: int, default -1
        Number of overlapping terms to dislay. If -1, display all. (default)
    return_data : bool default False
        Return a dict containing the output of `ScatterChartExplorer.to_dict` instead of
        an html.
    return_scatterplot_structure : bool, default False
        return ScatterplotStructure instead of html
    Returns
    -------
    str
    html of visualization

    '''
    color = None
    if singleScoreMode or word_vec_use_p_vals:
        color = 'd3.interpolatePurples'
    if singleScoreMode or not sort_by_dist:
        sort_by_dist = False
    else:
        sort_by_dist = True
    if term_ranker is None:
        term_ranker = termranking.AbsoluteFrequencyRanker

    category_name, not_category_name = get_category_names(category, category_name, not_categories, not_category_name)

    if not_categories is None:
        not_categories = [c for c in corpus.get_categories() if c != category]

    if term_scorer:
        scores = get_term_scorer_scores(category, corpus, neutral_categories, not_categories, show_neutral, term_ranker,
                                        term_scorer, use_non_text_features)

    if pmi_filter_thresold is not None:
        pmi_threshold_coefficient = pmi_filter_thresold
        warnings.warn(
            "The argument name 'pmi_filter_thresold' has been deprecated. Use 'pmi_threshold_coefficient' in its place",
            DeprecationWarning)

    if use_non_text_features:
        pmi_threshold_coefficient = 0

    scatter_chart_explorer = ScatterChartExplorer(corpus,
                                                  minimum_term_frequency=minimum_term_frequency,
                                                  minimum_not_category_term_frequency=minimum_not_category_term_frequency,
                                                  pmi_threshold_coefficient=pmi_threshold_coefficient,
                                                  filter_unigrams=filter_unigrams,
                                                  jitter=jitter,
                                                  max_terms=max_terms,
                                                  term_ranker=term_ranker,
                                                  use_non_text_features=use_non_text_features,
                                                  term_significance=term_significance,
                                                  terms_to_include=terms_to_include, )
    if ((x_coords is None and y_coords is not None)
            or (y_coords is None and x_coords is not None)):
        raise Exception("Both x_coords and y_coords need to be passed or both left blank")
    if x_coords is not None:
        scatter_chart_explorer.inject_coordinates(x_coords,
                                                  y_coords,
                                                  rescale_x=rescale_x,
                                                  rescale_y=rescale_y,
                                                  original_x=original_x,
                                                  original_y=original_y)
    if topic_model_term_lists is not None:
        scatter_chart_explorer.inject_metadata_term_lists(topic_model_term_lists)
    if metadata_descriptions is not None:
        scatter_chart_explorer.inject_metadata_descriptions(metadata_descriptions)
    if term_colors is not None:
        scatter_chart_explorer.inject_term_colors(term_colors)
    if term_metadata is not None:
        scatter_chart_explorer.inject_term_metadata(term_metadata)
    html_base = None
    if semiotic_square:
        html_base = get_semiotic_square_html(num_terms_semiotic_square,
                                             semiotic_square)
    scatter_chart_data = scatter_chart_explorer.to_dict(
        category=category,
        category_name=category_name,
        not_category_name=not_category_name,
        not_categories=not_categories,
        transform=transform,
        scores=scores,
        max_docs_per_category=max_docs_per_category,
        metadata=metadata,
        alternative_text_field=alternative_text_field,
        neutral_category_name=neutral_category_name,
        extra_category_name=extra_category_name,
        neutral_categories=neutral_categories,
        extra_categories=extra_categories,
        background_scorer=characteristic_scorer,
        include_term_category_counts=include_term_category_counts
    )

    if return_data:
        return scatter_chart_data

    scatterplot_structure = ScatterplotStructure(
        VizDataAdapter(scatter_chart_data),
        width_in_pixels=width_in_pixels,
        height_in_pixels=height_in_pixels,
        max_snippets=max_snippets,
        color=color,
        grey_zero_scores=gray_zero_scores,
        sort_by_dist=sort_by_dist,
        reverse_sort_scores_for_not_category=reverse_sort_scores_for_not_category,
        use_full_doc=use_full_doc,
        asian_mode=asian_mode,
        match_full_line=match_full_line,
        use_non_text_features=use_non_text_features,
        show_characteristic=show_characteristic,
        word_vec_use_p_vals=word_vec_use_p_vals,
        max_p_val=max_p_val, save_svg_button=save_svg_button,
        p_value_colors=p_value_colors,
        x_label=x_label,
        y_label=y_label,
        show_top_terms=show_top_terms,
        show_neutral=show_neutral,
        get_tooltip_content=get_tooltip_content,
        x_axis_values=x_axis_values,
        y_axis_values=y_axis_values,
        x_axis_values_format=x_axis_values_format,
        y_axis_values_format=y_axis_values_format,
        color_func=color_func,
        show_axes=show_axes,
        horizontal_line_y_position=horizontal_line_y_position,
        vertical_line_x_position=vertical_line_x_position,
        show_extra=show_extra,
        do_censor_points=censor_points,
        center_label_over_points=center_label_over_points,
        x_axis_labels=x_axis_labels,
        y_axis_labels=y_axis_labels,
        topic_model_preview_size=topic_model_preview_size,
        vertical_lines=vertical_lines,
        unified_context=unified_context,
        show_category_headings=show_category_headings,
        show_cross_axes=show_cross_axes, div_name=div_name,
        alternative_term_func=alternative_term_func,
        include_all_contexts=include_all_contexts,
        show_axes_and_cross_hairs=show_axes_and_cross_hairs,
        max_overlapping=max_overlapping
    )

    if return_scatterplot_structure:
        return scatterplot_structure

    return (BasicHTMLFromScatterplotStructure(scatterplot_structure)
            .to_html(protocol=protocol,
                     d3_url=d3_url,
                     d3_scale_chromatic_url=d3_scale_chromatic_url,
                     html_base=html_base))