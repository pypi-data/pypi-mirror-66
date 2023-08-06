import numpy as np
import plotnine as p9


def plot_distribution(df, plot_type="violin", figure_size=None, save_path="fancy_violinplot.png"):
    """
    Cleaned up plots using plotnine
    # https://stackoverflow.com/questions/52556305/how-to-print-quantiles-using-plotnine-in-python
    TODO: Needs more documentation
    """
    if figure_size is None:
        height = len(df["variable"].unique()) / 2
        width = height / 1.2
        figure_size = (width, height)
    bp = p9.ggplot(df, p9.aes(x="variable", y="value", fill="variable"))
    if plot_type == "violin":
        bp += p9.geom_violin()
    elif plot_type == "box":
        bp += p9.geom_boxplot()
    else:
        raise ValueError(f"Expected `violin` or `box`, value provided: {plot_type}")
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
            p9.aes(x="variable", y="value", label=round(df.groupby("variable").median().reset_index().value, 2),),
            color="black",
            data=df.groupby("variable").median().reset_index(),
            position=p9.position_dodge(width=0.8),
            nudge_x=0.2,
        )
        + p9.geom_text(
            p9.aes(x="variable", y="value", label=round(df.groupby("variable").min().reset_index().value, 2),),
            color="black",
            size=8,
            data=df.groupby("variable").min().reset_index(),
            position=p9.position_dodge(width=0.2),
            nudge_x=0.2,
        )
        + p9.geom_text(
            p9.aes(x="variable", y="value", label=round(df.groupby("variable").max().reset_index().value, 2),),
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


def plot_violin(df, plot_type="violin", figure_size=None, save_path="violinplot.png"):
    return plot_distribution(df=df, plot_type=plot_type, figure_size=figure_size, save_path=save_path)


def plot_box(df, plot_type="box", figure_size=None, save_path="boxplot.png"):
    return plot_distribution(df=df, plot_type=plot_type, figure_size=figure_size, save_path=save_path)


def plot_bar(df, save_path="barplot.png"):
    bp = (
        p9.ggplot(df)
        + p9.geom_col(p9.aes(x="label", y="count"))
        + p9.geom_text(
            p9.aes(x="label", y="count", label="count"), color="blue", stat="identity", nudge_y=0.5, va="bottom"
        )
        + p9.coord_flip()
        + p9.labs(title="No of images per class", x="Label (class name)", y="No of Images", color="Label (class name)")
        + p9.theme_xkcd()
    )
    bp.save(save_path, dpi=300, limitsize=False)
    return bp
