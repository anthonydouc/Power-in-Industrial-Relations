# -*- coding: utf-8 -*-
'''
Module for generating research area level summary files.
'''
import pandas as pd
import scipy.stats as stats

from ..analysis import read_top31, filter_for_file_stats
from ..paths import get_info_dir, get_save_dir


def inflation_by_file(all_data: pd.DataFrame) -> pd.DataFrame:
    ''' Summarises inflation by research area. '''

    summary = (all_data
               .groupby(['Filename', 'Filter'])[['Inflation']]
               .agg(['mean', 'median', 'min', 'max']))

    return summary


def sample_size_stats(all_data: pd.DataFrame) -> pd.DataFrame:
    ''' Summarises sample size by research area. '''

    summary = (all_data
               .groupby(['Filename','Filter'])['Sample size']
               .agg(['mean','median','std'])
               .round(0))

    return summary


def effect_stats(all_data: pd.DataFrame) -> pd.DataFrame:
    ''' Summarises effect size by research area. '''

    fns = ['count', stats.iqr, stats.skew, stats.kurtosis]
    summary = (all_data
               .groupby(['Filename','Filter'])['Effect size']
               .agg(fns)
               .round(0))

    return summary


def data_sharing_stats(all_data, infodir):
    '''
    Summarises the proportion of estimates published
    before and after data sharing by research area and journal.
    '''

    data_sharing_journals = pd.read_excel(f'{infodir}/Data sharing journals.xlsx')

    data_sharing_journals['Journal'] = (data_sharing_journals['Journal']
                                        .str.capitalize())

    data_sharing_years = (data_sharing_journals
                          .set_index('Journal')['Year data sharing mandated']
                          .to_dict())

    all_data['First_year_data_sharing'] = all_data['Journal'].map(data_sharing_years)

    all_data['Before_data_sharing'] = (all_data['Year published']
                                       < all_data['First_year_data_sharing'])

    all_data['After_data_sharing'] = (all_data['Year published']
                                      >= all_data['First_year_data_sharing'])

    data_sharing_summary = (all_data
                            .groupby(['Filename','Filter','Journal'])
                            .agg({'Before_data_sharing':'sum', 'After_data_sharing':'sum'}))

    data_sharing_summary['No. estimate'] = (all_data
                                            .groupby(['Filename','Filter'])
                                            .count()['Study id.'])

    data_sharing_summary['Before_data_sharing'] /= data_sharing_summary['No. estimate']
    data_sharing_summary['After_data_sharing'] /= data_sharing_summary['No. estimate']

    data_sharing_summary = data_sharing_summary[['Before_data_sharing', 'After_data_sharing']]

    # journals that have inacted data sharing.
    m_j_ds = (data_sharing_summary
              .index.get_level_values('Journal')
              .isin(data_sharing_journals['Journal'].unique()))

    data_sharing_summary = data_sharing_summary[m_j_ds]

    medians = (data_sharing_summary
               .groupby(['Filename','Filter'])
               .median())

    medians['Journal'] = 'Median'

    medians = (medians
               .reset_index()
               .set_index(['Filename','Filter','Journal']))

    data_sharing_summary = pd.concat([data_sharing_summary, medians])

    data_sharing_summary = (data_sharing_summary
                            .unstack(2)
                            .fillna(0)
                            .reindex(list(data_sharing_journals['Journal'])+['Median'], level=1, axis=1))

    return data_sharing_summary


def first_studies(all_data: pd.DataFrame, reg_results: pd.DataFrame,
                  how:str) -> pd.DataFrame:
    '''
    Generates a comparison of the first three years of data
    for each research area.
    '''

    exclude_journals = ['Working paper',
                        'Thesis',
                        'Conference paper',
                        'Report',
                        '3ie final report',
                        "Ifpri report",
                        "Mnb workingpapers 2005/1. budapest: magyar nemzeti bank."]


    mask_exlcude_journals = all_data['Journal'].isin(exclude_journals)

    average_effects = (all_data
                       .groupby(['Study id.'])['Effect size']
                       .mean())

    data_flt = all_data[~mask_exlcude_journals]

    first_years = (data_flt
                   .drop_duplicates(subset=['Filename','Filter','Year published'])
                   .groupby(['Filename','Filter'])['Year published']
                   .nsmallest(3))

    first_years = (pd.DataFrame(first_years)
                   .reset_index()
                   .set_index(['Filename','Filter','Year published']))

    first_years['Year_number'] = (1 + first_years
                                      .reset_index()
                                      .groupby(['Filename','Filter'])
                                      .cumcount()).values

    idx = first_years.index

    lowest = (all_data
              .set_index(['Filename','Filter', 'Year published'])
              .loc[idx][['Journal', 'Study id.', 'Obs id']])

    lowest['Average study level effect'] = lowest['Study id.'].map(average_effects.to_dict())

    lowest = (lowest
              .reset_index()
              .drop_duplicates(subset=['Filename','Filter','Year published', 'Study id.'])
              .set_index(['Filename','Filter', 'Year published']))

    lowest['Count'] = (lowest
                       .groupby(['Filename','Filter'])
                       .cumcount())

    lowest[f'b1_{how}'] = reg_results[f'b1_{how}']

    lowest = (lowest
              .reset_index()
              .set_index(['Filename','Filter','Count'])
              .unstack(2))

    lowest.columns = lowest.columns.swaplevel(0, 1)

    lowest = lowest.sort_index(level=0, axis=1)

    return lowest


def data_sharing_compar(all_data:pd.DataFrame, infodir: str):
    '''
    Generates a stacked dataset by iteratively removing
    data from individual research areas.
    '''

    top31 = read_top31()

    all_data_31 = all_data[all_data['Journal'].isin(top31)]

    data = []

    sharing_exclusions = pd.read_excel(f'{infodir}/data_sharing_exclusions.xlsx')
    sharing_exclusions.columns = [col.capitalize() for col in sharing_exclusions.columns]
    sharing_exclusions['Journals_excluded'] = sharing_exclusions['Journals_excluded'].str.capitalize()
    sharing_exclusions = sharing_exclusions.set_index('Journals_excluded')

    for col in sharing_exclusions.columns:
        exclude_journals = sharing_exclusions[sharing_exclusions[col] == 1].index
        sharing_data = all_data_31[~all_data_31['Journal'].isin(exclude_journals)].copy()
        sharing_data['Journal adopting sharing'] = col
        data.append(sharing_data)

    all_data = pd.concat(data)
    return all_data


def data_sharing_prop(reg_results: pd.DataFrame,
                      data_sharing_summary: pd.DataFrame) -> pd.DataFrame:

    summary = reg_results.copy()
    summary['Median_share_before_data_sharing'] = data_sharing_summary['Before_data_sharing']['Median']
    summary['Median_share_after_data_sharing'] = data_sharing_summary['After_data_sharing']['Median']
    return summary


def data_sharing_summaries(output_dir, how, suffix, all_data, reg_results):
    '''
    Generates research area (file) summary files relating to data sharing
    only, and saves to disk.
    '''

    all_data = filter_for_file_stats(all_data)

    infodir = get_info_dir()

    savedir = get_save_dir(output_dir, f'{how}{suffix}/file_summaries/')

    save_kwargs = {'encoding':'latin-1'}

    sharing_compar = data_sharing_compar(all_data, infodir)

    (sharing_compar
     .reset_index()
     .to_excel(f'{savedir}/data_sharing_comparison.xlsx', **save_kwargs))


def file_summaries(output_dir, how, suffix, all_data, reg_results):
    ''' Generates research area (file) summary files and saves to disk. '''

    all_data = filter_for_file_stats(all_data)

    infodir = get_info_dir()

    savedir = get_save_dir(output_dir, f'{how}{suffix}/file_summaries/')

    save_kwargs = {'encoding':'latin-1'}

    sample_size_sum = sample_size_stats(all_data)

    (sample_size_sum
     .reset_index()
     .to_excel(f'{savedir}/file_sample_size_stats.xlsx', **save_kwargs))

    est_no_sum = effect_stats(all_data)

    (est_no_sum
     .reset_index()
     .to_excel(f'{savedir}/file_est_no_stats.xlsx', **save_kwargs))

    # data_sharing_summary = data_sharing_stats(all_data, infodir)

    # (data_sharing_summary
    #  .reset_index()
    #  .to_excel(f'{savedir}/file_sharing_stats.xlsx', **save_kwargs))

    # sharing_compar = data_sharing_compar(all_data, infodir)

    # (sharing_compar
    #  .reset_index()
    #  .to_excel(f'{savedir}/data_sharing_comparison.xlsx', **save_kwargs))

    # sharing_props = data_sharing_prop(reg_results, data_sharing_summary)

    # (sharing_props
    #  .reset_index()
    #  .to_excel(f'{savedir}/file_estimates_data_sharing_proportions.xlsx', **save_kwargs))

    year_summaries = first_studies(all_data, reg_results, how)

    (year_summaries
     .reset_index()
     .to_excel(f'{savedir}/studies_first_three_years_wide.xlsx', **save_kwargs))

    inf_summary = inflation_by_file(all_data)

    (inf_summary
     .reset_index()
     .to_excel(f'{savedir}/inflation_by_dataset.xlsx', **save_kwargs))
