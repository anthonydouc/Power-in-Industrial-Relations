 # -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy

from .filtering import filter_for_outliers, filter_for_estimation
from .regressions import (calc_estimates, calc_outliers_tstat, calc_outliers,
                          calc_leverage)


def estimate(all_data: pd.DataFrame, how: str, critical_values=[1.96]):
    ''' Run estimation for all files based on specified method. '''
    
    if how != 'rfe':
        est_how = how
    else:
        est_how = 'wls'
        
    # filter data for estimation
    data_filtered = filter_for_estimation(all_data)

    # calculate estimates for each file and filter
    reg_results = (data_filtered
                   .groupby(['Filename','Filter'])
                   .apply(calc_estimates, how=est_how)
                   .unstack(2)
                   .reset_index(level=2)
                   .rename(columns={'level_2':'Year'}))
    
    # merge results for all years back onto data
    reg_results_all = reg_results.loc[reg_results['Year'] == 'All', [f'b1_{est_how}',f'b2_{est_how}']]
    
    data_filtered = pd.merge(data_filtered,
                             reg_results_all,
                             how='left',
                             on=['Filename','Filter'])

    # merge results for window specific years back onto data
    reg_results_window = reg_results.loc[reg_results['Year'] != 'All', [f'b1_{est_how}',f'b2_{est_how}', 'Year']]

    reg_results_window = reg_results_window.rename(columns= {f'b1_{est_how}': f'b1_{est_how}_subyr_window',
                                                             f'b2_{est_how}': f'b2_{est_how}_subyr_window',
                                                             'Year': 'yearsubmitted'})

    data_filtered = pd.merge(data_filtered,
                             reg_results_window,
                             how='left',
                             on=['Filename','Filter', 'yearsubmitted'])

    data_ad = (data_filtered
               .groupby(['Filename','Filter'])
               .apply(calc_stats, how=est_how, critical_values=critical_values))

    all_data = pd.merge(all_data,
                        data_ad,
                        on=['Filename','Filter','Obs id'],
                        how='left')

    all_data = pd.merge(all_data,
                        reg_results_all,
                        how='left',
                        on=['Filename','Filter'])

    all_data = pd.merge(all_data,
                        reg_results_window,
                        how='left',
                        on=['Filename','Filter', 'yearsubmitted'])

    if how == 'fpp':
        
        # add in the individual fatpetp & fatpet results 
        data_filtered = filter_for_estimation(all_data)

        reg_res_fatpet = (data_filtered
                          .groupby(['Filename','Filter'])
                          .apply(calc_estimates, how='fatpet')
                          .unstack(2)
                          .reset_index(level=2)
                          .rename(columns={'level_2':'Year'}))
     
        reg_res_fatpetp = (data_filtered
                           .groupby(['Filename','Filter'])
                           .apply(calc_estimates, how='fatpetp')
                           .unstack(2)
                           .reset_index(level=2)
                           .rename(columns={'level_2':'Year'}))

        reg_results = reg_results.merge(reg_res_fatpet,
                                        how='left',
                                        on=['Filename','Filter', 'Year'])
        
        reg_results = reg_results.merge(reg_res_fatpetp,
                                        how='left',
                                        on=['Filename','Filter', 'Year'])
        
    if how == 'rfe':
        data_filtered = filter_for_estimation(all_data)
        
        reg_results = (data_filtered
                       .groupby(['Filename','Filter'])
                       .apply(calc_estimates, how='rfe'))
        
        all_data = pd.merge(all_data,
                            reg_results[['b1_rfe','b2_rfe']],
                            how='left',
                            on=['Filename','Filter'])
        
        # recalculate various stats and overwrite the existing (which)
        # were based on wls
        
        all_data = all_data[[col for col in all_data.columns 
                             if col not in data_ad.columns or col == "Obs id"]]
        
        data_filtered = filter_for_estimation(all_data)

        
        data_ad = (data_filtered
                   .groupby(['Filename','Filter'])
                   .apply(calc_stats, how='rfe', critical_values=critical_values))
    
        all_data = pd.merge(all_data,
                            data_ad,
                            on=['Filename','Filter','Obs id'],
                            how='left')
        
    return all_data, reg_results


def outliers(data: pd.DataFrame, drop_outliers=True) -> pd.DataFrame:
    '''
    Determine outlier and leverage points for all files, and append the results
    to the input DataFrame.
    '''

    data_filtered = filter_for_outliers(data)

    out_results = (data_filtered
                   .groupby(['Filename','Filter'])
                   .apply(calc_outliers))
    
    lev_results = (data_filtered
                   .groupby(['Filename','Filter'])
                   .apply(calc_leverage))

    if drop_outliers:
        
        data = pd.merge(data, lev_results[['Leverage_point']],
                        how='left', left_index=True, right_index=True)
        
        data = pd.merge(data, out_results[['Outlier']],
                        how='left', left_index=True, right_index=True)
    
        data['Outlier'] = data['Outlier'].fillna(False)
        
        data['Leverage_point'] = data['Leverage_point'].fillna(False)
        
        data = calc_outliers_tstat(data)
        
    else:
        data['Outlier'] = False
        data['Leverage_point'] = False
        data['Outlier_tstat'] = False
        
    data = pd.merge(data, lev_results[['dfbeta']],
                    how='left', left_index=True, right_index=True)
    
    data = pd.merge(data, out_results[['Student residual']],
                    how='left', left_index=True, right_index=True)
    
    return data


def cumnorm(z):
    return 0.5 * (1 + scipy.special.erf(z / (2 ** 0.5)))


def calc_tau_sq(data: pd.DataFrame) -> pd.Series:
    ''' Calculates tau squared. '''
    
    w = (1 / data['Standard error']) ** 2
    
    t = data['Effect size']
    
    c = w.sum() - (w ** 2).sum() / w.sum()
    
    q = (w * t ** 2).sum() - (w * t).sum() ** 2 / w.sum()
    
    if q > len(data) - 1:
        tsq = (q - (len(data) - 1)) / c
    else:
        tsq = 0
        
    return tsq, c, q


def calc_stats(data, how, critical_values=[1.96]):
    '''
    Calculates various statistical metrics from observation level data,
    and regression estimates.
    '''
    data = data.copy()
    
    if len(data) == 0:
        
        fields = ['Filename', 'Filter', 'Obs id', 'Adequate_2', 'Adequate_28',
                  'Inflation', 'Bias', 'Inflation 1000',
                  'Z', 'tsq', 'Power', 'q', 'c', 'p_sig',
                  'ex_sig', 'ex_sigcrit', 'significant',
                  'significant_crit', 'Power_gt_29', 'Sig_pow_29']
        
        return pd.DataFrame({f: np.nan for f in fields})

    b1_estimate = data[f'b1_{how}'].values[0]

    # determine whether observations are adequate based on
    # two different sized thresholds.
    threshold_2 = abs(b1_estimate) / 2
    
    threshold_28 = abs(b1_estimate) / 2.8

    data['Adequate_2'] = 0
    
    data['Adequate_28'] = 0

    mask_adequate2 = data['Standard error'] <= threshold_2
    
    mask_adequate28 = data['Standard error'] <= threshold_28
    
    data.loc[mask_adequate2, 'Adequate_2'] = 1
    
    data.loc[mask_adequate28, 'Adequate_28'] = 1
    
    # determine extent of research inflation
    data['Bias'] = data['Effect size'] - b1_estimate
    
    mask_1 = data['Effect size'] / b1_estimate < 0


    if b1_estimate == 0:
        data['Inflation'] = np.nan
    else:
        data['Inflation'] = data['Bias'] / b1_estimate

    data['Inflation 1000'] = data['Inflation']

    data.loc[mask_1, 'Inflation 1000'] = 10 ** 3
    
    fields = {}

    # calculate tau squared statistic, and excessess statistical significance.
    tsq, c, q = calc_tau_sq(data)
        
    for critical_value in critical_values:
        
        critname = f'{critical_value*100:.0f}'
        
        # determine whether observations are significant,
        # first based on the effect size versus the regression estimate,
        # secondly based additionally on the observation t-statistic value.
        #data['significant'] =  0
        
        data['significant'] = 0
    
        mask_tstat = data['t-stat'] >= critical_value
        
        mask_sign = data['Effect size'] / b1_estimate > 0
        
        data.loc[mask_tstat, 'significant'] = 1
    
        #data.loc[mask_tstat & mask_sign, 'significant'] = 1
        
        # determine statistical power
        data['Z'] = critical_value - abs(b1_estimate) / data['Standard error']
        
        data['Power'] = 1 - cumnorm(data['Z'])
        
        data['Power_gt_29'] = 0
        mask_p29 = data['Power'] > 29.43 / 100
        data.loc[mask_p29, 'Power_gt_29'] = 1
        
        data['Sig_pow_29'] = 0
        mask_sig_pow_29 = (data['significant'] == 1) & (data['Power_gt_29'] == 1)
        data.loc[mask_sig_pow_29, 'Sig_pow_29'] = 1

        prs = ((critical_value * data['Standard error'] - abs(b1_estimate))
               / np.sqrt( data['Standard error'] ** 2 + tsq))

        p_sig = 1 - cumnorm(prs)

        #ex_sig = data['significant'] - p_sig

        ex_sig = data['significant'] - p_sig

        fields_crit = {f'Z_{critname}':data['Z'],
                       f'Power_{critname}':data['Power'],
                       f'p_sig_{critname}': p_sig,
            #           f'ex_sig_{critname}': ex_sig,
                       f'ex_sig_{critname}': ex_sig,
                       f'significant_{critname}': data['significant'],
                       f'Power_gt_29_{critname}': data['Power_gt_29'],
                       f'Sig_pow_29_{critname}': data['Sig_pow_29']}
        
        fields = {**fields, **fields_crit}

    return pd.DataFrame({'Filename': data['Filename'],
                         'Filter': data['Filter'], 
                         'Obs id':data['Obs id'],
                         'Adequate_2':data['Adequate_2'],
                         'Adequate_28':data['Adequate_28'],
                         'Inflation':data['Inflation'],
                         'Bias':data['Bias'],
                         'Inflation 1000':data['Inflation 1000'],
                         'Z':data['Z'],
                         'tsq': tsq,
                         'q':q,
                         'c':c,
                         **fields})


def estimate_all(all_data, how='wls', drop_outliers=True, suffix='',
                 critical_values=[1.96]):

    # map outliers and leverage points
    all_data = outliers(all_data, drop_outliers)
    
    # estimate coefficents based on specified method
    all_data, reg_results = estimate(all_data, how, critical_values=critical_values)
        
    return all_data, reg_results
