# -*- coding: utf-8 -*-
import shutil

from pathlib import Path

from .analysis import (get_all_data,
                       estimate_all,
                       filter_for_reporting,
                       filter_for_outliers,
                       get_study_type)

from .charts import funnel_plot#, summary_charts

from .summaries import (data_sharing_summaries,
                        author_summaries,
                        file_summaries,
                        journal_summaries,
                        generate_subsets)

from .paths import get_outputs_dir


def save_outputs(all_data, reg_results, method, suffix, critical_values):
        
    outputdir = get_outputs_dir()
    
    Path(f'{outputdir}/{method}{suffix}/').mkdir(parents=True, exist_ok=True)

    crit_cols = []
    
    for critical_value in critical_values:
        critname = f'{critical_value*100:.0f}'

        crit_cols += [f'Power_{critname}', f'ex_sig_{critname}']

    cols = ['Filename',
            'Journal',
            'Year published',
            'yearsubmitted', 
            'Author share of estimates',
            'Google scholar citations may 2021',
            'Sample size',
            'Number of authors',
            'Effect size',
            'Study no.',
            'Standard error',
            'Ranking',
            'FoR code',
            f'b1_{method}',
            f'b2_{method}',
            'Filter',
            'Outlier', 
            'Student residual',
            'dfbeta',
            'Leverage_point',
            'tsq',
            'q',
            'c',
            't-stat',
            'First year',
            'Last year',
            'Time span',
            'Four years prior',
            'Same year',
            'Three years after',
            'Four years prior top 5',
            'Same year top 5',
            'Three years after top 5']
    
    cols += crit_cols
    
    save_data = all_data[cols]
    
    save_data['Filecode'] = (save_data
                             .groupby(['Filename','Filter'])
                             .ngroup())
    
    save_data = save_data.sort_values(by=['Filecode', 'Journal'])
    
    effects, types = get_study_type()
        
    save_data['Effect type'] = save_data['Filename'].map(effects)
    
    save_data['Micro or Macro'] = save_data['Filename'].map(types)
    
    print(f'{outputdir}/{method}{suffix}/all_datasets_combined.xlsx')
    
    save_data.to_excel(f'{outputdir}/{method}{suffix}/all_datasets_combined.xlsx', encoding='latin-1', index=False)
    all_data.reset_index(drop=True).to_excel(f'{outputdir}/{method}{suffix}/estimate_data.xlsx', encoding='latin-1', index=False)
    reg_results.reset_index().to_excel(f'{outputdir}/{method}{suffix}/estimates_by_file.xlsx', encoding='latin-1', index=False)


def run_local(method: str, drop_outliers=True, keep_journals=None,
              suffix: str=''):

    if not drop_outliers: suffix += '_keep_outliers'
    if keep_journals is not None: suffix += '_top31_journals'

    print(f'Running with method={method}')

    all_data = get_all_data(keep_journals=keep_journals)

    all_data, reg_results = estimate_all(all_data, method, drop_outliers, suffix)

    all_data = filter_for_reporting(all_data)

    output_dir = get_outputs_dir()

    if (method == 'wls') and ((keep_journals is None) and (drop_outliers)):
        data_sharing_summaries(output_dir, method, suffix, all_data, reg_results)

    generate_subsets(output_dir, method, suffix, all_data)

