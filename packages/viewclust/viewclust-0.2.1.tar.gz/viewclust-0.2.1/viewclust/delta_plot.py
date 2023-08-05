import plotly.graph_objects as go

def delta_plot(account_list, dist_list, fig_out=''):
    """Takes a list of distance from target frames and generates the delta plot.

    Parameters
    -------
    account_list: array_like of DataFrame
        Strided to match dist_list for labels in the legend.
    dist_list: array_like of DataFrame
        Taken to be a list of distance from target series generated by the jobUse function.
    fig_out: str, optional
        Writes the generated figure to file as the given name.
        If empty, skips writing. Defaults to empty.

    See Also
    -------
    jobUse: Generates the input frame for this function.
    """

    fig = go.Figure()
    for i, frame in enumerate(dist_list):
        fig.add_trace(go.Scatter(x=frame.index, y=frame.divide(len(frame)),
                                 mode='lines',
                                 name=account_list[i],
                                 fillcolor='rgba(200, 128, 128, 1.0)'))
    if fig_out != '':
        fig.write_html(fig_out)
