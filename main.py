import os
import analysisIC
import aggAnalyze
import aggStats
import aggPlot
import aggExport
import warnings
import time


warnings.filterwarnings("ignore")

# Input the address to the location of IC .zip files
# Please make sure the IC archives are the only .zip files in that folder
myDir = ''
zipNames = [x for x in os.listdir(myDir) if x.endswith(".zip")]


if __name__ == '__main__':
    
    nameLists = [None] * len(zipNames)
    filePhases = nameLists.copy()
    visDurs = nameLists.copy()
    visNums = nameLists.copy()

    
    print('Analyzing files:\n')

    for zipind, zipname in enumerate(zipNames):
        
        print(zipname + '\n')
        nameLists[zipind], filePhases[zipind], visDurs[zipind], visNums[zipind] = analysisIC.analyze(zipname, myDir)
    
    print('Aggregating files\n')
    aggNum, phaseDict = aggAnalyze.aggregate(visNums, filePhases, nameLists)
    aggDur, _ = aggAnalyze.aggregate(visDurs, filePhases, nameLists)

    print('Running statistical tests\n')
    corrDict, meanCorrs, compDict, anovas, posthocs, halfs, anova_pars = aggStats.getstats(aggDur, aggNum)
    
    print('Creating Graphs\n')
    aggPlot.visualize(aggDur, aggNum, meanCorrs, posthocs, halfs, anova_pars)
    
    print('Exporting results to Excel\n')
    aggExport.export(aggDur, aggNum, compDict, anovas, posthocs, halfs, anova_pars)
    
    print('Finished!\n\nExiting...')
    time.sleep(3)
