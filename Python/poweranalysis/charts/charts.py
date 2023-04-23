# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from bokeh.plotting import figure
from bokeh.io import show, output_file
from bokeh.layouts import gridplot
from bokeh.models import LinearAxis, Range1d
from plots import histogram, output, plot_format, Line

from ..analysis import filter_for_charts, read_top5, read_top31, read_labour_journals
from ..paths import get_save_dir


def study_area_histograms(all_estimate_data: pd.DataFrame, savedir: str):
    ''' Generates histograms of estimates per research area.'''
    
    counts = all_estimate_data.groupby('Filename').count()['Filter'].values

    hist = histogram([counts[counts<=500]], nbins=100, x_axis_label='No. observations')
    output(hist, f'{savedir}/histogram of observations (0-500)', output_html=True)

    hist = histogram([counts], nbins=100, x_axis_label='No. observations')
    output(hist, f'{savedir}/histogram of observations', output_html=True)


def author_count_plots(all_estimate_data: pd.DataFrame, savedir: str):
    ''' Generates plots showing mean number of authors and Power over time '''

    m_econ = all_estimate_data['FoR code'].isin([1401, 1402, 1403, 1499])
    
    data_econ = all_estimate_data[m_econ]
    data_necon = all_estimate_data[~m_econ]

    na1 = (data_econ
           .groupby(['Year published'])['Number of authors']
           .mean())
    
    na2 = (data_necon
           .groupby(['Year published'])['Number of authors']
           .mean())

    output_file(f'{savedir}/authors over time.html')
    
    nplot = figure(x_axis_label='Year published', y_axis_label='Average number of authors',
                   title='All journals', plot_height=500, plot_width=500, x_range=(1960, 2020))

    nplot.line(na1.index, na1.values, line_width=2)
    
    nplot.line(na2.index, na2.values, line_width=2, line_dash='dashed',
               color='red',line_alpha=0.7)

    show(nplot)

    ap_eco = (data_econ
              .groupby(['Year published'])['Power']
              .mean())
    
    ap_all = (data_necon
              .groupby(['Year published'])['Power']
              .mean())

    output_file(f'{savedir}/average power over time.html')

    aplot = figure(x_axis_label='Year published', y_axis_label='Average power',
                   plot_height=500, plot_width=500, x_range=(1960, 2020))

    aplot.line(ap_eco.index, ap_eco.values, line_width=2)
    aplot.line(ap_all.index, ap_all.values, line_width=2, line_dash='dashed',
               color='red', line_alpha=0.7)

    show(aplot)


def running_mean(x, N):
    cumsum = np.nancumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def plot_ranking(all_estimate_data, rankings=['A*'], journals=None,
                 n='effect', top5=None, title=''):
    if rankings is not None:
        filtered_data = all_estimate_data[all_estimate_data['FoR code'].isin([1401, 1402, 1403, 1499])]
        data_astar = filtered_data.loc[filtered_data['Ranking'].isin(rankings)]
    elif journals is not None:
        data_astar = all_estimate_data.loc[all_estimate_data['Journal'].isin(journals)]
    elif top5 is not None:
        data_astar = all_estimate_data.loc[all_estimate_data['Journal'].isin(top5)]
    annual_power = data_astar.groupby('Year published')['Power'].mean()
    years = annual_power.index

    rmean = running_mean(annual_power.values, 5)

    plot = figure(x_axis_label='Year published', y_axis_label='Average power',
                  title=title, plot_height=500, plot_width=600, x_range=(1960, 2020), y_range=(0, 1.05))

    if n == 'effect':
        ns = data_astar.groupby(['Year published']).count()['Study no.']
    else:
        ns = data_astar.groupby(['Year published','Filename'])['Study no.'].nunique().groupby('Year published').sum()

    nyears = ns.index
    if len(ns) > 0 :
    	min_y, max_y = 0, max(ns)
    else:
        min_y, max_y = 0, 10
    plot.extra_y_ranges = {"N": Range1d(start=min_y, end=max_y)}
    plot.add_layout(LinearAxis(y_range_name="N", axis_label="Number of studies"), 'right')
    plot.vbar(nyears, top= ns.values, width=0.5, color='grey', y_range_name="N", fill_alpha=0.65, line_alpha=0)

    plot.circle(years, annual_power, size=5)
    rmean = np.concatenate((np.ones(4)*np.nan, rmean))
    plot.line(years, rmean, line_width=3, line_dash='dashed', color='red')
    plot.line(np.linspace(1906, 2020, len(years)), [0.8]*len(years), line_width=1.5, color='orange')
    plot = plot_format(plot)
    nplot = figure(x_axis_label='Year published', y_axis_label='Sample size',
                   title=title, plot_height=500, plot_width=500, x_range=(1960, 2020))

    nplot.vbar(nyears, top= ns.values, width=0.5, color='grey')

    return plot, nplot


def ranking_plots(all_estimate_data, savedir_charts):
        
    lb_journals = read_labour_journals()
    top31 = read_top31()
    top5 = read_top5()

    output_file(f'{savedir_charts}/time_trends_nestimate.html')
    plot_as, nplot_as = plot_ranking(all_estimate_data, ['A*'], title='A*')
    plot_aas, nplot_aas = plot_ranking(all_estimate_data, ['A*','A'], title='A* & A')
    plot_ar, nplot_ar = plot_ranking(all_estimate_data, None, ['The american economic review'], title='American review')
    plot_t5, nplot_t5 = plot_ranking(all_estimate_data, None, None, 'effect', top5=top5, title='Top 5')
    plot_lb, nplot_lb = plot_ranking(all_estimate_data, None, lb_journals, title='Labour only')
    plot_31, nplot_31 = plot_ranking(all_estimate_data, None, top31, title='top 31')
    plot_a, nplot_a = plot_ranking(all_estimate_data, ['A'], title='A')
    plot_b, nplot_b = plot_ranking(all_estimate_data, ['B'], title='B')
    show(gridplot([[plot_as, plot_ar],  [plot_a, plot_b], [plot_t5, plot_aas], [plot_lb, plot_31]]))


def prop_sig(all_estimate_data, savedir, journ_base, journs, title):
    ''' Generates plots visualising weighted averages over time. '''
    
    data_journal_ann = (all_estimate_data
                        .groupby(['Journal','Year published'])
                        .agg({'significant':'sum', 'Study no.':'count'}))

    data_journal_ann['Proportion significant'] = data_journal_ann['significant'] / data_journal_ann['Study no.']

    data_base = data_journal_ann.loc[journ_base, :]['Proportion significant']

    data_journs = data_journal_ann.loc[journs, :][['Proportion significant', 'significant', 'Study no.']]

    max_year = 2019
    years = list(range(1990-10, max_year))

    chart_data = (data_journs
                  .groupby('Year published')
                  .agg({'significant':'sum',
                        'Study no.':'sum',
                        'Proportion significant':'mean'}))

    chart_data['Proportion significant wa'] = chart_data['significant'] / chart_data['Study no.']

    data_base = data_base.reindex(years).fillna(np.nan)
    
    avg = chart_data['Proportion significant'].reindex(years).fillna(np.nan)
    
    wavg = chart_data['Proportion significant wa'].reindex(years).fillna(np.nan)

    ybase = running_mean(data_base.values, 5)
    ybase = np.concatenate((np.ones(4)*np.nan, ybase))

    ya = running_mean(avg.values.T,5)
    ya = np.concatenate((np.ones(4)*np.nan, ya))

    ywa = running_mean(wavg.values.T,5)
    ywa = np.concatenate((np.ones(4)*np.nan, ywa))

    years = years[10:]
    ya = ya[10:]
    ywa = ywa[10:]
    ybase = ybase[10:]

    plot_sig = Line(x=years,
                    ys=[ya],
                    plot_width=800,
                    y_range=(0, 1),
                    legend_params={'location':'below', 'orientation':'vertical','labels':[title +' average']},
                    y_axis_label='Proportion significant',
                    colors=['#273746'],
                    format_kwargs={'legend_font_size':'16px', 'axis_font_size':'16px'}).p

    plot_sig.line(x=years, y=ywa, legend=title +' weighted average', line_dash='dotted', line_width=3)
    
    plot_sig.line(x=years, y=ybase, legend=journ_base, line_dash='dashed', line_width=3)
    
    plot_sig.line(x=[2006, 2006], y=[0,1], line_width=2, line_color='grey')
    
    plot_sig.legend.location = (200, 0)
    
    output(plot_sig, f'{savedir}/Proportion signficant over time, {title}', output_html=True)


def prop_charts(all_estimate_data, savedir_charts):
    journ_base = 'The american economic review'
    journs_1 = ['The review of economic studies','The quarterly journal of economics']
    journs_2 = ['The review of economic studies',
                'The quarterly journal of economics','The review of economics and statistics',
                'Journal of the european economic association','The economic journal',
                'International economic review','European economic review']

    prop_sig(all_estimate_data, savedir_charts, journ_base, journs_1, 'RES, QJE')
    prop_sig(all_estimate_data, savedir_charts, journ_base, journs_2, 'RES, TRES, JEEA, EJ, IER, EER')



def summary_charts(output_dir, how, suffix, all_estimate_data, reg_results):

    savedir_charts = get_save_dir(output_dir, f'{how}{suffix}/charts/')

    all_estimate_data = filter_for_charts(all_estimate_data)

    study_area_histograms(all_estimate_data, savedir_charts)

    all_estimate_data = all_estimate_data[all_estimate_data['Number of authors'].notnull()]

    all_estimate_data = all_estimate_data[all_estimate_data['Year_pub_invalid'] == False]

    author_count_plots(all_estimate_data, savedir_charts)

    ranking_plots(all_estimate_data, savedir_charts)

    prop_charts(all_estimate_data, savedir_charts)

