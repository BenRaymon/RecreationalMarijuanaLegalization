import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib import cm
from scipy import stats
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
import math
import geopandas
import mapclassify as mc
from pingouin import ancova, read_dataset
from pywaffle import Waffle
import re
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import iplot, init_notebook_mode
from plotly.subplots import make_subplots
import plotly.express as px
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)


def create_fig(df):
    fig = make_subplots(rows=2, cols=3, 
                    specs=[[{"colspan":3}, None, None],
                   [{}, {}, {}]],
                subplot_titles=("","Recreational Confidence Intervals", "Medical Confidence Intervals", "Illegal Confidence Intervals"))

    #top plot with all 3 lines
    i = -1
    colors = ['#E45756', '#00CC96', '#1C8356']
    for col in df.columns:
        i += 1
        fig.add_trace(go.Scatter(x=df.index, y=df[col].values,
                                 name = col,
                                 mode = 'markers+lines',
                                 line=dict(shape='linear', color=colors[i]),
                                 connectgaps=True
                                 )
                     )
    return fig


def calc_CI(data, question, start_year):
    data_Years = []
    for i in range(start_year, 2020):
        year = data[data['Survey Year'] == i]
        data_Years.append(year)
    upper = []
    lower = []
    for year in data_Years:
        ci = (stats.t.interval(alpha=0.95, df=len(year[question])-1,
                     loc=np.mean(year[question]),
                     scale=stats.sem(year[question])))
        lower.append(ci[0])
        upper.append(ci[1])
    return upper, lower

def add_plot(data, row, col, color, fig, upper, lower, ci_color, question):
    fig.add_trace(
        go.Scatter(
            x=data['Survey Year'],
            y=data[question],
            line=dict(color=color),
            showlegend=False,
            name='',
            mode='lines'
        ), row=row, col=col
    )
    fig.add_trace(
        go.Scatter(
            x=data['Survey Year'].to_list()+data['Survey Year'].to_list()[::-1], # x, then x reversed
            y=upper+lower[::-1], # upper, then lower reversed
            fill='toself',
            fillcolor=ci_color,
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False
        ), row=row, col=col
    )