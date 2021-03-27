import pandas as pd

def export(aggDict, compDict, betDict, phenotype):
    
    # Create spreadsheet
    def write2excel(dfDict, sheets, filename):
        with pd.ExcelWriter(filename) as writer:  
            for sheet in sheets:
                dfDict[sheet].to_excel(writer, sheet_name = sheet)
    
    write2excel(dfDict = aggDict, sheets = list(aggDict.keys()), filename = 'Aggregate_Analysis.xlsx')
    write2excel(dfDict = compDict, sheets = list(compDict.keys()), filename = 'methodCompare.xlsx')
    for bet in betDict.keys():
        write2excel(dfDict = betDict[bet], sheets = betDict[bet], filename = 'pairwise_ttest_' + bet + '-phase.xlsx')
    write2excel(dfDict = phenotype, sheets = list(phenotype.keys()), filename = 'wilcoxon-phase.xlsx')