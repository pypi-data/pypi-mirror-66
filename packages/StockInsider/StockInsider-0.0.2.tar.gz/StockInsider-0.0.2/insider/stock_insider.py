from typing import Callable, List, Optional

import plotly.graph_objects as go
import pandas as pd

from insider.mixins import BaseMixin, MovingIndicatorMixin
from insider.stock import Stock
from insider.constants import MA_N, MD_N, EXPMA_N


class StockInsider(Stock, BaseMixin, MovingIndicatorMixin):
    """Plot daily trading indicators."""

    def __init__(self, code):
        """
        code: Full stock code，(e.g. 'sz002156')，股票完整代码
        """
        super().__init__(code)

    @staticmethod
    def _plot_line(df: pd.DataFrame, head: int, line_name: str):
        if head:
            df = df.tail(head)
        plot_data = go.Scatter(x=df["day"], y=df["close"], name=line_name)
        return plot_data

    def _plot_moving_lines(
        self,
        func: Callable,
        name: str,
        head: int = 90,
        ns: Optional[List] = None,
        verbose: bool = False,
    ):

        plot_data = []
        for n in ns:
            df = func(n=n)
            line_name = name + str(n)
            plot_data.append(self._plot_line(df, head, line_name))

        if verbose:
            df = self._df.copy()
            stock_data = self._plot_stock_data(df, head)
            plot_data.append(stock_data)

        layout = self._set_layout()
        fig = go.Figure(data=plot_data, layout=layout)
        if verbose:
            fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_layout(title_text=f"{name.upper()} Chart ({self.stock_code})")
        fig.show()

    def plot_ma(
        self, head: int = 90, ns: Optional[List[int]] = None, verbose: bool = False
    ):
        """Plot Moving Average Indicator. 绘出MA曲线

        Parameters:
            head: The recent number of trading days to plot, default is 90, 最近交易日的天数，
            默认90，将会绘出最近90个交易日的曲线。
            ns: Select which trading lines to plot, default is to plot 5, 10, 20, 60-day lines
            选择曲线的种类，e.g. [5, 10], 默认会绘出5, 10, 20, 60日曲线
            verbose: If to include stock price or not, default is False.
            选择是否将股票价格曲线一起绘出，默认是False，将会只绘出指标曲线。
        """
        if ns is None:
            ns = MA_N

        func = self.ma
        self._plot_moving_lines(func=func, name="ma", head=head, ns=ns, verbose=verbose)

    def plot_md(
        self, head: int = 90, ns: Optional[List[int]] = None, verbose: bool = False
    ):
        """Plot Moving Deviation Indicator. 绘出MD曲线

        Parameters:
            head: The recent number of trading days to plot, default is 90, 最近交易日的天数，
            默认90，将会绘出最近90个交易日的曲线。
            ns: Select which trading lines to plot, default is to plot 5, 10, 20-day lines
            选择曲线的种类，e.g. [5, 10], 默认会绘出5, 10, 20日曲线
            verbose: If to include stock price or not, default is False.
            选择是否将股票价格曲线一起绘出，默认是False，将会只绘出指标曲线。
        """
        if ns is None:
            ns = MD_N

        func = self.md
        self._plot_moving_lines(func=func, name="md", head=head, ns=ns, verbose=verbose)

    def plot_ema(
        self, head: int = 90, ns: Optional[List[int]] = None, verbose: bool = False
    ):
        """Plot Exponential Moving Average Indicator. 绘出EMA曲线

        Parameters:
            head: The recent number of trading days to plot, default is 90, 最近交易日的天数，
            默认90，将会绘出最近90个交易日的曲线。
            ns: Select which trading lines to plot, default is to plot 5, 10, 20, 60-day lines
            选择曲线的种类，e.g. [5, 10, 20, 60], 默认会绘出5, 10, 20, 60日曲线
            verbose: If to include stock price or not, default is False.
            选择是否将股票价格曲线一起绘出，默认是False，将会只绘出指标曲线。
        """
        if ns is None:
            ns = EXPMA_N

        func = self.ema
        self._plot_moving_lines(
            func=func, name="ema", head=head, ns=ns, verbose=verbose
        )

    def plot_macd(self, head: int = 90):
        """Plot MACD Indicator. 绘出MACD曲线

        Parameters:
            head: The recent number of trading days to plot, default is 90, 最近交易日的天数，
            默认90，将会绘出最近90个交易日的曲线。

        A mixed chart will be plotted, including a bar chart to visualize MACD, and line charts
        to visualize DIFF and DEA.
        将会绘出差值柱形图来表示MACD, 以及表示差离值和讯号线的线性图。
        """
        df_macd = self.macd()
        if head:
            df_macd = df_macd.tail(head)

        df_macd.loc[:, "color"] = df_macd["macd"].apply(
            lambda x: "red" if x >= 0 else "green"
        )

        layout = self._set_layout()
        fig = go.Figure(layout=layout)

        fig.add_trace(
            go.Bar(
                x=df_macd["day"],
                y=df_macd["macd"],
                base=0,
                marker_color=df_macd["color"],
                name="MACD",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_macd["day"], y=df_macd["dea"], marker_color="orange", name="DEA"
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df_macd["day"], y=df_macd["diff"], marker_color="black", name="DIFF"
            )
        )
        fig.update_layout(title_text=f"MACD Chart ({self.stock_code})")
        fig.show()
