import numpy as np
import pandas as pd
import pingouin as pg
from scipy import stats



def getstats(aggDict):
    
    animals = list(aggDict['0NP']['sub_id'])
    cols = list(aggDict['0NP'].columns.values)
    phaseCols = cols[3:19] # Getting phase names

    sequences = ['0NP', '1NP', '(0,1,~) D', '(0,-1,~)']
    
    # Loading results of manual analysis
    mxl = pd.read_excel('Impulsivity strategies.xlsx', sheet_name=sequences, index_col=0, nrows=25,
                        usecols=np.arange(0, 19), keep_default_na=False)

    # Auto. vs Man. correlation
    corrDict = {}
    meanCorrs = {} # Just the mean

    for kind, kval in enumerate(sequences):
        corrDict[kval] = {}
        meanCorrs[kval] = 0
        df = aggDict[kval].set_index('sub_id')
        for animal in animals:
            corRes = pg.corr(mxl[kval].loc[animal, '1L':'8D'].astype('float64'),
                             df.loc[animal, '1L':'8D'].astype('float64'), method='pearson')
            corrDict[kval][animal] = corRes.loc['pearson']
            meanCorrs[kval] += corRes.loc['pearson']['r'] / len(animals)

    # For export
    compDict = {}
    for ind, sheetname in enumerate(sequences):
        compDict[sheetname] = pd.DataFrame.from_dict(corrDict[sheetname]).T

    # Between subjects pairwise t-tests
    betDict = {'treat': {}, 'phen': {}}
    for bet in betDict.keys():
        for key in sequences:
            
            # Converting to long format
            df = aggDict[key].loc[:, :'8D'].melt(id_vars=['sub_id', 'treat', 'phen'], value_vars=phaseCols,
                                                 var_name='phase', value_name='dv')
            df['dv'] = pd.to_numeric(df['dv'])
            df = pg.pairwise_ttests(data=df, subject='sub_id', dv='dv', within='phase',
                                    between=[bet], return_desc=True).round(6)
            betDict[bet][key] = df
            
    # Wilcoxon for impulsive sequence, for phases 6D:7L
    df = aggDict['(0,-1,~)'].loc[:, :'8D']
    phenotype = {'epi': df[df.phen == 'epi'], 'non': df[df.phen == 'non']}
    for phenkey, phenval in phenotype.items():
        w, p = stats.wilcoxon(phenval.loc[:, '6D'], phenval.loc[:, '7L'], mode='approx')
        phenotype[phenkey] = pd.DataFrame.from_dict({'w': [w], 'p': [p]})

    # Descriptive stats for self-control
    cDrink = aggDict['(0,1,~) D'].loc[:, :'8D']
    cStats = [(cDrink.mean(axis=0), cDrink.sem(axis=0))]

    return corrDict, meanCorrs, compDict, betDict, phenotype, cStats
