import numpy as np
import plotnine as p9

# https://stackoverflow.com/questions/52556305/how-to-print-quantiles-using-plotnine-in-python


def fancy_plot(
    df, plot_type="violin", figure_size=None, save_path="fancy_violinplot.png"
):
    """
    Cleaned up plots using plotnine
    TODO: Needs more documentation
    """
    if figure_size is None:
        height = len(df["variable"].unique()) / 2
        width = height / 1.2
        figure_size = (width, height)
    bp = p9.ggplot(df, p9.aes(x="variable", y="value", fill="variable"))
    if plot_type == "violin":
        bp += p9.geom_violin()
    if plot_type == "box":
        bp += p9.geom_boxplot()
    bp = (
        bp
        + p9.coord_flip()
        + p9.geom_jitter(alpha=0.2, width=0.1, height=0.1)
        + p9.labs(
            title="Violinplot of avg inter-class distance",
            x="Label (class name)",
            y="Avg distance",
            color="Label (class name)",
        )
        + p9.geom_text(
            p9.aes(
                x="variable",
                y="value",
                label=round(df.groupby("variable").median().reset_index().value, 2),
            ),
            color="black",
            data=df.groupby("variable").median().reset_index(),
            position=p9.position_dodge(width=0.8),
            nudge_x=0.2,
        )
        + p9.geom_text(
            p9.aes(
                x="variable",
                y="value",
                label=round(df.groupby("variable").min().reset_index().value, 2),
            ),
            color="black",
            size=8,
            data=df.groupby("variable").min().reset_index(),
            position=p9.position_dodge(width=0.2),
            nudge_x=0.2,
        )
        + p9.geom_text(
            p9.aes(
                x="variable",
                y="value",
                label=round(df.groupby("variable").max().reset_index().value, 2),
            ),
            color="black",
            size=8,
            data=df.groupby("variable").max().reset_index(),
            position=p9.position_dodge(width=0.2),
            nudge_x=0.2,
        )
    )
    bp = bp + p9.theme(figure_size=figure_size, legend_position="none")
    bp.save(save_path, dpi=300, limitsize=False)
    return bp
