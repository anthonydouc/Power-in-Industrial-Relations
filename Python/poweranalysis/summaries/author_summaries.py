# -*- coding: utf-8 -*-
'''
Module for generating author level summary files.
'''
import pandas as pd

from ..analysis import filter_for_author_stats
from ..paths import get_save_dir


def no_estimate_by_author(all_data: pd.DataFrame) -> pd.DataFrame:
    '''Determines the number estimates and unique research areas per author.'''

    all_data = all_data[~all_data['Author group'].isnull()]
    
    author_cols = [f'Author {x}' for x in range(1,10)]

    data = pd.melt(all_data, id_vars=['Filename', 'Author group'],
                   value_vars=author_cols, value_name='Author')

    n_files = (data
               .groupby('Author').nunique()[['Filename']]
               .rename(columns={'Filename':'No. research areas'}))

    n_estimates = (data
                   .groupby('Author').count()[['Filename']]
                   .rename(columns={'Filename':'No. estimates'}))

    summary = pd.concat([n_files, n_estimates], axis=1)

    return summary


def author_summaries(output_dir, how, suffix, all_data, reg_results):
    ''' Generates author summary files and saves to disk. '''
    
    all_data_flt = filter_for_author_stats(all_data)

    savedir = get_save_dir(output_dir, f'{how}{suffix}/author_summaries/')
        
    save_kwargs = {'encoding':'latin-1'}

    author_est = no_estimate_by_author(all_data_flt)
    author_est.to_excel(f'{savedir}/author_summary_stats.xlsx', **save_kwargs)
