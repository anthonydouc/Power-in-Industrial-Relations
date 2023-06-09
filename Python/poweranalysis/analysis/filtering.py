# -*- coding: utf-8 -*-
'''
Module containing filtering steps for various analytical tasks.
'''


def filter_for_estimation(data):

    data = data.copy()
    m_ntout = data['Outlier_tstat'] == False
    m_nout = data['Outlier'] == False
    m_nlev = data['Leverage_point'] == False
    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False

    data = data[m_vest & m_vse & m_nlev & m_nout & m_ntout]

    return data


def filter_for_outliers(data):

    data = data.copy()
    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False

    data = data[m_vest & m_vse]

    return data


def filter_for_network(data):

    data = data.copy()

    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False

    data = data[m_vest & m_vse]

    return data


def filter_for_subsets(data):
    
    data = data.copy()

    m_ntout = data['Outlier_tstat'] == False
    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False

    m_out = data['Outlier'] == False

    m_lev = data['Leverage_point'] == False
    
    m_journ = (~data['Journal'].isnull()) & (data['Journal'] != '')

    data = data[m_vest & m_vse & m_ntout & m_out & m_lev & m_journ]

    return data


def filter_for_journal_stats(data):

    data = data.copy()

    m_ntout = data['Outlier_tstat'] == False
    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False
    
    data = data[m_vest & m_vse & m_ntout]

    return data


def filter_for_charts(data):
    data = data.copy()
    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False

    data = data[m_vest & m_vse]
    return data


def filter_for_file_stats(data):

    data = data.copy()
    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False

    data = data[m_vest & m_vse]

    return data


def filter_for_author_stats(data):

    data = data.copy()
    m_vest = data['Est_invalid'] == False
    m_vse = data['SE_invalid'] == False

    data = data[m_vest & m_vse]

    return data


def filter_for_reporting(data):

    date_cols = ["Acceptance_time",
                 "Submit_to_revision",
                 "Revise_to_accept",
                 "Accept_to_publish",
                 "Submit_to_publish",
                 ]
    
    date_cols_day = [col + "_days"  for col in date_cols]

    date_cols_week = [col + "_weeks" for col in date_cols]
    
    drop_cols = ['Submission date',
                 'Acceptance date',
                 'Revised date',
                 'Month published',
                 'Author share of estimates',
                 'Google scholar citations may 2021',
                 'Data available',
                 'Ranking',
                 'FoR code',
                 'Author group',
                 'No. estimates file',
                 'No. estimates author group',
                 'Author share of estimates',
                 'Net change in unique editors',
                 'Adequate_28',
                 'Inflation',
                 'Bias',
                 'Inflation 1000',
                 'Z',
                 'q',
                 'c',
                 'p_sig',
                 'ex_sig',
                 'significant',
                 'Power_gt_29',
                 'Sig_pow_29',
                 'index',
                 'Doi',
                 'n_citations',
                 'first_page',
                 'last_page',
                 'issue',
                 'Adequate_2',      
                 'Author group share of estimates',
                 'No. lost editors'
                 ]

    editor_cols = [c for c in data.columns if ('Editor_'  in c) or ('Co-editor_' in c)]
    
    drop_cols += editor_cols
    
    drop_cols += date_cols_day
    
    drop_cols += date_cols_week

    drop_cols = [c for c in drop_cols if c in data.columns]
    
    data = data.drop(drop_cols, axis=1)
    return data
