# -*- coding: utf-8 -*-
'''
Module for generating journal level summary files.
'''
import pandas as pd

from ..analysis import (get_impact_factors, read_labour_journals, read_top31,
                        get_journal_attrs, filter_for_journal_stats,
                        read_top31order)

from ..paths import get_save_dir


def get_journal_files(all_data, journals):

    data_journals = all_data[all_data['Journal'].isin(journals)]

    files_sub = data_journals['Filename'].unique()

    return files_sub


def journal_summary(all_data, groups):

    journal_factors = get_impact_factors()

    journal_rankings, journal_forcode = get_journal_attrs()

    data_agg = (all_data
                .groupby(groups)
                .agg({'Adequate_2': ['sum'],
                      'Adequate_28': ['sum'],
                      'Study no.': ['count', 'nunique'],
                      'Filename':'nunique',
                      'Year published':['min','max'],
                      't-stat': ['mean','median'],
                      'significant_196': 'sum',
                      'ex_sig_196':'mean',
                      'tsq': 'mean',
                      'Power_196': ['mean', 'median'],
                      'Inflation': 'median',
                      'Inflation 1000': 'median',
                      'Sig_pow_29_196':'sum'}))

    data_agg.columns = ['No. adequate_2',
                        'No. adequate_28',
                        'No. estimates',
                        'No. study',
                        'No. unique effects',
                        'First year of data',
                        'Last year of data',
                        'Average t-stat',
                        'Median t-stat',
                        'No. significant 196',
                        'Average ESS',
                        'tsq',
                        'Average power',
                        'Median power',
                        'Median Inflation',
                        'Median Inflation (1000)',
                        'Prop_sig_pow29']

    data_agg = data_agg.reset_index()

    data_agg['Proportion adequate_2'] = data_agg['No. adequate_2'] / data_agg['No. estimates']
    data_agg['Proportion adequate_28'] = data_agg['No. adequate_28'] / data_agg['No. estimates']
    #data_agg['Proportion significant'] = data_agg['No. significant'] / data_agg['No. estimates']
    data_agg['Proportion significant 196'] = data_agg['No. significant 196'] / data_agg['No. estimates']
    data_agg['Prop_sig_pow29'] = data_agg['Prop_sig_pow29'] / data_agg['No. estimates']
    data_agg['Prop_sig_pow29_cond'] = data_agg['Prop_sig_pow29'] / data_agg['Proportion significant 196']

    data_agg = data_agg.fillna(0)
    data_agg = data_agg.sort_values(by='Proportion adequate_2', ascending=False).reset_index()

    if 'Journal' in groups:

        data_agg['ABDC_ranking'] = data_agg['Journal'].map(journal_rankings)
        
        data_agg['FOR code'] = data_agg['Journal'].map(journal_forcode)
        
        data_agg['Impact factor'] = data_agg['Journal'].map(journal_factors)

    return data_agg


def gen_file_subset(all_data, all_data_noflt, data_agg_file, journals):

    cols = ['Filename',
            'Filter',
            'No. estimates',
            'Proportion significant 196',
            'Average power',
            'Average ESS',
            'tsq']

    journal_files = get_journal_files(all_data, journals)

    summary = data_agg_file[data_agg_file['Filename'].isin(journal_files)]

    # number of estimates in each file that are only published in the list of journals.
    data_j_flt = (all_data[all_data['Journal'].isin(journals)]
                  .groupby(['Filename','Filter'])
                  .count()['Study no.'])

    # number of estimates in each file.
    data_j_noflt = (all_data_noflt
                    .groupby(['Filename','Filter'])
                    .count()['Study no.'])

    summary = summary[cols].set_index(['Filename','Filter'])

    summary['No. estimates in top31'] = data_j_flt

    summary['No. estimates before filter'] = data_j_noflt

    return summary


def gen_file_summary(all_data, all_data_noflt, savedir):
    ''' Generates aggregated summaries by journal and research area (filename). '''

    lb_journals = read_labour_journals()

    top31_journals = read_top31()

    data_agg_file = journal_summary(all_data, ['Filename','Filter'])

    top31_summary = gen_file_subset(all_data, all_data_noflt, data_agg_file, top31_journals)
    top31_summary.to_excel(f'{savedir}/file_summary_top31_only.xlsx', encoding='latin-1')

    lab_summary = gen_file_subset(all_data, all_data_noflt, data_agg_file, lb_journals)
    lab_summary.to_excel(f'{savedir}/file_summary_labour_only.xlsx', encoding='latin-1')

    
def gen_ann_summary(all_data, savedir):
    ''' Generates aggregated summaries by journal and year of publication. '''
    
    lb_journals = read_labour_journals()

    top31_journals = read_top31()

    cols = ['Journal',
            'No. estimates',
            'No. study',
            'No. unique effects',
            'First year of data',
            'Last year of data',
            'Average power',
            'Median power',
            'Average ESS',
            'Average t-stat',
            'Median t-stat',
            'No. significant 196',
            'Proportion significant 196',
            'No. adequate_2',
            'Proportion adequate_2',
            'Median Inflation',
            'Prop_sig_pow29',
            'Prop_sig_pow29_cond']
    
    data_agg = journal_summary(all_data, ['Journal','Year published'])

    data_agg.to_excel(f'{savedir}/annual_summary_by_journal.xlsx', encoding='latin-1')

    data_agg = data_agg[cols+['Year published']]
    data_agg = data_agg.sort_values(by=['Journal','Year published'])

    labour_summary = data_agg[data_agg['Journal'].isin(lb_journals)]
    labour_summary.to_excel(f'{savedir}/annual_summary_by_journal_labour_only.xlsx', encoding='latin-1')

    top31_summary = data_agg[data_agg['Journal'].isin(top31_journals)]
    top31_summary.to_excel(f'{savedir}/annual_summary_by_journal_top31_only.xlsx', encoding='latin-1')


def gen_summary(all_data, savedir):
    ''' Generates aggregated summaries by journal. '''


    lb_journals = read_labour_journals()

    top31_journals = read_top31()

    cols = ['Journal',
            'No. estimates',
            'No. study',
            'No. unique effects',
            'First year of data',
            'Last year of data',
            'Average power',
            'Median power',
            'Average ESS',
            'Average t-stat',
            'Median t-stat',
            'No. significant 196',
            'Proportion significant 196',
            'No. adequate_2',
            'Proportion adequate_2',
            'Median Inflation',
            'Prop_sig_pow29',
            'Prop_sig_pow29_cond']

    data_agg = journal_summary(all_data, 'Journal')

    data_agg.to_excel(f'{savedir}/SADD.xlsx', index=False, encoding='latin-1')

    njf = (all_data
           .groupby(['Journal','Filename','Filter'])
           .count()['Inflation'])

    nf = (all_data
          .groupby(['Filename','Filter'])
          .count()['Inflation'])

    rjf = njf / nf

    rj_avg = rjf.groupby('Journal').mean()

    rj_med = rjf.groupby('Journal').median()

    # aggregate
    data_agg = data_agg[cols].set_index('Journal')
    data_agg['Average proportion of estimates'] = rj_avg
    data_agg['Median proportion of estimates'] = rj_med
    data_agg = data_agg.reset_index()

    labour_summary = data_agg[data_agg['Journal'].isin(lb_journals)]

    top31_summary = data_agg[data_agg['Journal'].isin(top31_journals)]

    # ensure order matches the spreadsheet.
    top31order = read_top31order()
   
    top31_summary['Order'] = top31_summary['Journal'].map(top31order)

    top31_summary = top31_summary.sort_values(by='Order', ascending=True).drop('Order', axis=1)

    top31_summary.to_excel(f'{savedir}/journal_summary_top31_only.xlsx', encoding='latin-1')

    labour_summary.to_excel(f'{savedir}/journal_summary_labour_only.xlsx', encoding='latin-1')


def journal_summaries(output_dir, how, suffix, all_estimate_data, reg_results):

    all_estimate_data = filter_for_journal_stats(all_estimate_data)

    savedir_journal = get_save_dir(output_dir, f'{how}{suffix}/journal_summaries/')

    savedir_file = get_save_dir(output_dir, f'{how}{suffix}/file_summaries/')

    all_estimate_data['Number of authors'] = all_estimate_data['Number of authors'].astype(float)
    all_estimate_data['Study no.'] = all_estimate_data['Study no.'].astype(str)
    all_estimate_data['Study no.'] += all_estimate_data['Filename']

    def summarise(x, how='Filename'):
        
        year = x.name[1]
        filename = x.name[0]
        mask_file = all_estimate_data[how] == filename
        mask_years = (all_estimate_data['Year published'] >= (year - 5)) & (all_estimate_data['Year published'] < year)
        data_full = all_estimate_data[mask_file & mask_years]

        x[f'ES median 5 {how}'] = data_full.median()['Effect size']
        x[f'SE median 5 {how}'] = data_full.median()['Standard error']
        x[f't-stat median 5 {how}'] = data_full.median()['t-stat']
        x[f'Prop sig 5 {how}'] = data_full['significant_196'].sum() / len(data_full)

        return x

    all_estimate_data_noflt = all_estimate_data.copy()

    m_out = all_estimate_data['Outlier'] == False
    m_lev = all_estimate_data['Leverage_point'] == False
    
    m_journ = (~all_estimate_data['Journal'].isnull()) & (all_estimate_data['Journal'] != '')

    all_estimate_data = all_estimate_data[m_out & m_lev & m_journ]
    
    all_estimate_data = (all_estimate_data
                         .groupby(['Filename', 'Year published'])
                         .apply(summarise, how='Filename'))

    all_estimate_data = (all_estimate_data
                         .groupby(['Journal', 'Year published'])
                         .apply(summarise, how='Journal'))

    gen_summary(all_estimate_data, savedir_journal)

    gen_ann_summary(all_estimate_data, savedir_journal)

    gen_file_summary(all_estimate_data, all_estimate_data_noflt, savedir_file)
    
