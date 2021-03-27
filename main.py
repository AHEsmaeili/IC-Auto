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
    aniDicts = nameLists.copy()
    
    
    print('Analyzing files:\n')

    for zipind, zipname in enumerate(zipNames):
        
        print(zipname + '\n')
        nameLists[zipind], filePhases[zipind], aniDicts[zipind] = analysisIC.analyze(zipname, myDir)
    
    print('Aggregating files\n')
    aggDict, phaseDict = aggAnalyze.aggregate(aniDicts, filePhases, nameLists)
    
    print('Running statistical tests\n')
    corrDict, meanCorrs, compDict, betDict, phenotype, cStats = aggStats.getstats(aggDict)
    
    print('Creating Graphs\n')
    aggPlot.visualize(aggDict, betDict, meanCorrs, cStats)
    
    print('Exporting results to Excel\n')
    aggExport.export(aggDict, compDict, betDict, phenotype)
    
    print('Finished!\n\nExiting...')
    time.sleep(3)
