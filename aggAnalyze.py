import pandas as pd

# A method for combining all analysis results together
def aggregate(aniDicts, filePhases, nameLists):

    # List of sequences
    sheetNames = list(aniDicts[0][list(aniDicts[0].keys())[0]].keys())
    
    
    # Determining the longest phase
    maxlen = 0
    for indfp, fp in enumerate(filePhases):
        if len(fp) > maxlen:
            maxlen = len(fp)
            maxind = indfp

    phaseDict = filePhases[maxind]
    
    # Converting results to wide format
    aggDict = {}
    for sheetname in sheetNames:
        aggDict[sheetname] = {}
        tind = 0
        for anidictind, anidict in enumerate(aniDicts):
            for animal in nameLists[anidictind]:
                if animal == 'B6K6':
                    continue
                aggDict[sheetname][tind] = anidict[animal][sheetname] 
                tind += 1
        df = pd.DataFrame({k: pd.Series(l) for k, l in aggDict[sheetname].items()})
        aggDict[sheetname] = df.rename(index = phaseDict, inplace = False).T

    return aggDict, phaseDict