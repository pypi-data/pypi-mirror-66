import plotly.graph_objs as graph_objects

from capblood_seq import config

from ..data import diurnality


def get_gene_AM_PM_box_plot(gene):

    AM_PM_data = diurnality.get_gene_AM_PM_values(gene)

    AM_box_trace = graph_objects.Box(
        x=AM_PM_data["AM_mean_groups"],
        y=AM_PM_data["AM_means"],
        line={
            "color": config.AM_COLOR
        },
        name="AM"
    )

    AM_scatter_trace = graph_objects.Scatter(
        x=AM_PM_data["AM_mean_groups_jittered"],
        y=AM_PM_data["AM_means"],
        marker_color=AM_PM_data["AM_colors"],
        mode="markers",
        showlegend=False,
        name="AM"
    )

    PM_box_trace = graph_objects.Box(
        x=AM_PM_data["PM_mean_groups"],
        y=AM_PM_data["PM_means"],
        line={
            "color": config.PM_COLOR
        },
        name="PM"
    )

    PM_scatter_trace = graph_objects.Scatter(
        x=AM_PM_data["PM_mean_groups_jittered"],
        y=AM_PM_data["PM_means"],
        marker_color=AM_PM_data["PM_colors"],
        mode="markers",
        showlegend=False,
        name="PM"
    )

    title = "Mean expression"

    y_min = 0
    y_max = max(max(AM_PM_data["PM_means"]), max(AM_PM_data["AM_means"]))*1.1

    layout = graph_objects.Layout(
        {
            "yaxis": {
                "range": [y_min, y_max],
                "title": title,
                "exponentformat": "e"
            },
            "plot_bgcolor": "rgba(0, 0, 0, 0)",
            "title": {
                "text": "%s Time-of-Day Expression" % gene,
                "xanchor": "center",
                "xref": "container",
                "x": 0.5
            },
            "boxmode": "group",
            "xaxis": {
                "tickvals": list(range(
                    len(AM_PM_data["cell_type_label_list"]))),
                "ticktext": AM_PM_data["cell_type_label_list"]
            }
        }
    )

    figure = graph_objects.Figure(
        data=[AM_box_trace, AM_scatter_trace, PM_box_trace, PM_scatter_trace],
        layout=layout)

    for cell_type_index, cell_type_label in \
            enumerate(AM_PM_data["cell_type_label_list"]):
        significance_line = graph_objects.layout.Shape(
            type="line",
            x0=cell_type_index - 0.175,
            x1=cell_type_index + 0.175,
            y0=y_max,
            y1=y_max,
            line=dict(
                color="Black",
                width=5
            )
        )

        significance_bracket_left = graph_objects.layout.Shape(
            type="line",
            x0=cell_type_index - 0.175,
            x1=cell_type_index - 0.175,
            y0=y_max,
            y1=y_max * 0.95,
            line=dict(
                color="Black",
                width=4
            )
        )

        significance_bracket_right = graph_objects.layout.Shape(
            type="line",
            x0=cell_type_index + 0.175,
            x1=cell_type_index + 0.175,
            y0=y_max,
            y1=y_max * 0.95,
            line=dict(
                color="Black",
                width=4
            )
        )

        figure.add_shape(significance_line)
        figure.add_shape(significance_bracket_left)
        figure.add_shape(significance_bracket_right)

        figure.add_annotation(
            graph_objects.layout.Annotation(
                text="p=%.1e" % AM_PM_data["p_values"][cell_type_index],
                showarrow=False,
                yanchor="bottom",
                yref="y",
                y=y_max,
                x=cell_type_index,
                xref="x",
                xanchor="center"
            )
        )

    return figure


def get_diurnality_figure(threshold=None):

    diurnality_df = diurnality.get_gene_diurnality()

    colors = [config.CELL_TYPE_COLORS[cell_type] for
              cell_type in diurnality_df["Max Cell Type"]]

    scatter = graph_objects.Scatter(
        x=diurnality_df["Population Wide Z Score"],
        y=diurnality_df["By Cell Type Z Score"],
        mode="markers",
        marker={
            "size": 2+diurnality_df["Percent Cells Expressing"]*7,
            "color": colors
        },
        text=diurnality_df.index.values
    )

    figure = graph_objects.Figure(
        data=[scatter],
        layout=graph_objects.Layout(
            title="Gene Diurnality",
            plot_bgcolor="rgba(255, 255, 255, 0)",
            paper_bgcolor="rgba(255, 255, 255, 0)",
            yaxis={
                "title": "Cell Type Z-score"
            },
            xaxis={
                "title": "Population Z-score"
            }
        )
    )

    return figure
