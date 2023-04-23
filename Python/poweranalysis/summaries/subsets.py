#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd

from ..analysis import (read_labour_journals, read_top31, filter_for_subsets)

from ..paths import get_save_dir


def generate_subset(all_data: pd.DataFrame, journals: list) -> pd.DataFrame:
    '''
    Generates substets of the data file where estimates are published in
    the list of specified journals.
    '''

    data_sub = all_data[all_data['Journal'].isin(journals)]

    return data_sub


def get_journal_files(all_data, journals):

    data_journals = all_data[all_data['Journal'].isin(journals)]

    files_sub = data_journals['Filename'].unique()

    return files_sub


def generate_subset_files(all_data: pd.DataFrame, journals: list) -> pd.DataFrame:
    '''
    Generates substets of the data file where files are ....
    '''

    files_sub = get_journal_files(all_data, journals)

    data_sub = all_data[all_data['Filename'].isin(files_sub)]

    return data_sub


def journal_data_subsets(output_dir: list, save_dir: str, suffix: str,
                         all_data: pd.DataFrame):
    '''
    Generates substets of the data file for labour and top31 journals,
    and saves to disk.
    '''


    save_kwargs = {'encoding':'latin-1'}

    lb_journals = read_labour_journals()

    # labour journals
    data_lab = generate_subset(all_data, lb_journals)

    data_lab.to_excel(f'{save_dir}/estimate_data_labour_journals_only_{suffix}.xlsx', **save_kwargs)

    data_lab_files = generate_subset_files(all_data, lb_journals)

    data_lab_files.to_excel(f'{save_dir}/estimate_data_inclab_{suffix}.xlsx', encoding='latin-1')

    return data_lab


def generate_subsets(output_dir: list, how: str, suffix: str,
                     all_data: pd.DataFrame):
    
    save_dir = get_save_dir(output_dir, f'{how}{suffix}/')
    
    journal_data_subsets(output_dir, save_dir,'unfiltered', all_data)

    data_flt = filter_for_subsets(all_data)

    journal_data_subsets(output_dir, save_dir, 'filtered', data_flt)
