import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import seaborn as sb
import typing as tp

Size = tp.Tuple[tp.Optional[float], tp.Optional[float]]


class PlotManager:
    '''
    Convinient interface to divide DataFrame into buckets
    and plot it bucket by bucket

    :param data: initial data frame to plot
    :param bucket_sizes: sizes of all buckets from start to the end of data frame, their sum must be <= len(data)
    :param names: name for each bucket
    :param y_name: title for y axis

    '''

    def __init__(self, data: pd.DataFrame, bucket_sizes: tp.Iterable[int], names: tp.Optional[tp.List[str]] = None, y_name: tp.Optional[str] = None):
        self._data = data
        self._sizes = list(bucket_sizes)
        self._names = names
        self._yname = y_name

    def plot_all_buckets(self, title: str, plot_all_data=False, ylim: tp.Optional[Size] = None):
        '''
        Function to plot all data by groups of specified buckets

        :param title: title for plot
        :param plot_all_data: if true, then also plot all data frame combined
        :param ylim: top limit on y-axis
        '''

        def plot_box(data, axes, i):
            boxplot = sb.boxplot(data, ax=axes[i])
            if self._names is not None:
                boxplot.axes.set_title(self._names[i])
            else: boxplot.axes.set_title(f'{i + 1} Bucket')
            if ylim is not None:
                boxplot.set_ylim(ylim)

        fig, axes = plt.subplots(
            1, len(self._sizes) + 1 if plot_all_data else 0, figsize=(14, 8), sharey=True)
        prev_pos = 0
        for i, size in enumerate(self._sizes):
            bucket = self._data.iloc[prev_pos:prev_pos + size]
            prev_pos += size
            if self._yname is not None:
                axes[0].set_ylabel(self._yname)
            plot_box(bucket, axes, i)

        if plot_all_data:
            i = len(self._sizes)
            boxplot = sb.boxplot(self._data, ax=axes[i])
            boxplot.set_title('All')
            if ylim is not None:
                boxplot.set_ylim(ylim)

        if title is not None: fig.suptitle(title)
        fig.tight_layout()
        plt.show()

    @staticmethod
    def scatter(data: pd.DataFrame, x: str, y: str, basedOn: str, xlim: Size = (0, 1.2)):
        plt.figure(figsize=(9, 6))
        s = sb.scatterplot(data, x=x, y=y, hue=basedOn, style=basedOn)
        s.axes.yaxis.set_major_formatter(PercentFormatter(1))
        s.axes.xaxis.set_major_formatter(PercentFormatter(1))
        # s.axes.flat[0].yaxis.set_major_formatter(PercentFormatter(data.loc[0, y]))  # type: ignore
        # s.axes.flat[0].xaxis.set_major_formatter(PercentFormatter(data.loc[0, x]))  # type: ignore
        plt.title('Path length against number of steps')
        plt.xlabel('Steps count ratio')
        plt.ylabel('Path length ratio')
        plt.xlim(*xlim)
        plt.legend(fontsize=10)
        plt.show()

    def plot_lines(self, title: tp.Optional[str] = None, link: tp.Optional['PlotManager'] = None):
        '''
        Plots test number against given characteristic in the data frame.
        Each heuristic is colored uniqely.

        :param title: title for plot
        :param link: potentially anotehr PlotManager which data can be used 
            to create plot with shared x-axis
        '''

        def build_plots(data, ax, legend=False):
           for col in self._data.columns:
                p = sb.lineplot(data[col], label=col if legend else None, ax=ax)
                p.axes.yaxis.set_major_formatter(PercentFormatter(1))
            

        if link is not None:
            fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
            build_plots(self._data, axes[0])
            build_plots(link._data, axes[1], legend=True)
            axes[1].set_xlabel('Difficulty')
            axes[0].set_alpha(0.8)
            axes[1].set_alpha(0.8)
            if self._yname is not None: axes[0].set_ylabel(self._yname) 
            if link._yname is not None: axes[1].set_ylabel(link._yname) 
            if title is not None: fig.suptitle(title)
            # plt.legend(fontsize=10)
            # fig.legend(fontsize=10, loc=3)
            fig.tight_layout()
        else:
            axes = plt.axes()
            build_plots(self._data, axes, legend=True)
            plt.xlabel('Difficulty')
            if self._yname is not None: plt.ylabel(self._yname)
            if title is not None: plt.title(title)
            plt.grid(ls=':')
            plt.legend(loc=2)

        plt.show()


