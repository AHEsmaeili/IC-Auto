import pandas as pd

def export(aggDur, aggNum, compDict, anovas, posthocs, halfs, anova_pars):
    
    # Create spreadsheet
    def write2excel(dfDict, sheets, filename):
        with pd.ExcelWriter(filename) as writer:  
            for sheet in sheets:
                dfDict[sheet].to_excel(writer, sheet_name = sheet)
    
    write2excel(dfDict = aggNum, sheets = list(aggNum.keys()), filename = 'Aggregate_Analysis.xlsx')
    write2excel(dfDict = aggDur, sheets = list(aggDur.keys()), filename = 'Aggregate_Analysis_MeanVis.xlsx')
    write2excel(dfDict = compDict, sheets = list(compDict.keys()), filename = 'Method_Comparison.xlsx')

    for half in halfs:
        for par in anova_pars:
            write2excel(dfDict = posthocs[half[1]][par[2]], sheets = list(posthocs[half[1]][par[2]].keys()), filename = 'PPairwise_ttest_'+ half[1] + '-' + par[1] + '-' + par[2] + '-phase.xlsx')
            write2excel(dfDict = anovas[half[1]][par[2]], sheets = list(posthocs[half[1]][par[2]].keys()), filename = 'MixedAnova_'+ half[1] + '-' + par[1] + '-' + par[2] + '-phase.xlsx')
