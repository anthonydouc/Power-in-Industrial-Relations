# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

from ..paths import get_save_dir
from ..analysis import filter_for_charts 

from bokeh.plotting import figure, output_file, show
from bokeh.layouts import gridplot


def funnel_plot(output_dir: str, how: str, suffix: str,
                all_estimate_data: pd.DataFrame, reg_results: pd.DataFrame):
    '''
    Generates a funnel plot of inidiual effect sizes and standard errors for
    each research area.
    '''
    
    all_estimate_data = filter_for_charts(all_estimate_data)
    
    reg_results = reg_results.reset_index()
    
    savedir = get_save_dir(output_dir, f'{how}{suffix}/charts/')
                
    # output to static HTML file
    all_estimate_data = all_estimate_data[all_estimate_data['Filter'].astype(str) != 'nan']
    
    m_tout = all_estimate_data['Outlier_tstat'] == True
    m_out = all_estimate_data['Outlier'] == True
    m_lev = all_estimate_data['Leverage_point'] == True
        
    data_flt = all_estimate_data[~(m_out | m_lev | m_tout)]
        
    data_flt['Filename_filter'] = (data_flt['Filename']
                                    + '_' 
                                    + data_flt['Filter'].astype(int).astype(str))
    
    reg_results['Filename_filter'] = (reg_results['Filename']
                                      + '_'
                                      + reg_results['Filter'].astype(str))
    
    output_file(f"{savedir}/funnel_plots_all_files.html")
    
    filenames = data_flt['Filename_filter'].unique()
    charts = []
    
    y_line = np.linspace(-1e4, 1e4, 1000)
            
    for filename in filenames:
        
        data = data_flt[data_flt['Filename_filter'] == filename]
        
        reg = reg_results[reg_results['Filename_filter'] == filename]
        
        x = data['Effect size']
        
        y = 1 / data['Standard error']
        
        p = figure(plot_width=400, plot_height=400, toolbar_location=None,
                   title=filename, y_range=(0.98*y.min(), 1.02*y.max()))
        
        p.circle(x, y, size=2.5, color="navy")

        x_line = [reg[f'b1_{how}'].values[0]] * 1000

        p.line(x_line, y_line, color="red",
               line_width=2, line_dash='dashed', line_alpha=0.6)
        
        charts.append(p)
            
    show(gridplot(charts, ncols=4, toolbar_location=None))
    
    