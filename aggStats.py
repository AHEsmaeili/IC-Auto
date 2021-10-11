import numpy as np
import pandas as pd
import pingouin as pg


def getstats(aggDur, aggNum):
    
    animals = list(aggNum['0NP']['sub_id'])
    cols = list(aggNum['0NP'].columns.values)
    phaseCols = cols[3:19] # Getting phase names

    sequences = ['0NP', '1NP', '(0,1,~) D', '(0,-1,~)']
    
    # Loading results of manual analysis
    mxl = pd.read_excel('Impulsivity strategies.xlsx', sheet_name=sequences, index_col=0, nrows=25,
                        usecols=np.arange(0, 19), keep_default_na=False)

    # Auto. vs Man. correlation
    corrDict = {}
    meanCorrs = {} # Just the mean

    for key in sequences:
        corrDict[key] = {}
        meanCorrs[key] = 0
        df = aggNum[key].set_index('sub_id')
        for animal in animals:
            corRes = pg.corr(mxl[key].loc[animal, '1L':'8D'].astype('float64'),
                             df.loc[animal, '1L':'8D'].astype('float64'), method='pearson')
            corrDict[key][animal] = corRes.loc['pearson']
            meanCorrs[key] += corRes.loc['pearson']['r'] / len(animals)

    # For export
    compDict = {}
    for key in sequences:
        compDict[key] = pd.DataFrame.from_dict(corrDict[key]).T


    anova_pars = [('treat', 'control', 'phen'), ('phen', 'epi', 'treat')]
    sequences.append('Other')
    days = [phase for phase in phaseCols if 'L' in phase]
    nights = [phase for phase in phaseCols if 'D' in phase]
    halfs = ((cols[:3]+days, 'Days', days), (cols[:3]+nights, 'Nights', nights))
    
    # Running between subjects mixed-Anovas and pairwise t-tests for light/dark phases separately     
    anovas = {}    
    posthocs = {}
    
    for half in halfs:
        aovs = {'treat':{}, 'phen':{}}
        posts = {'treat':{}, 'phen':{}}
        
        for par in anova_pars:
            for key in sequences:
                seq = aggNum[key]
                df = seq[seq[par[0]] == par[1]].loc[:, half[0]].melt(id_vars = ['sub_id', 'treat', 'phen'], value_vars = half[2], var_name = 'phase', value_name = 'dv')
                df['dv'] = pd.to_numeric(df['dv'])
                aovs[par[2]][key] = pg.mixed_anova(data=df, subject = 'sub_id', dv='dv', within = 'phase', between = par[2])

                posts[par[2]][key] = pg.pairwise_ttests(data = df, subject = 'sub_id', dv = 'dv', within = 'phase',
                                           between = [par[2]], return_desc = True).round(6)
        
        posthocs[half[1]] = posts
        anovas[half[1]] = aovs


    return corrDict, meanCorrs, compDict, anovas, posthocs, halfs, anova_pars
