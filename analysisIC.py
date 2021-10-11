import os
import numpy as np
import pymice as pm
import genTimeline


# Clearing logs
os.system('cls||clear')

# Desired behavioral sequences/ratios
# ['Checking', 'Exploring', 'Self-control', 'Impulsive', 'Misc']
stratKeys = ['0NP', '1NP', '(0,1,~) D', '(0,-1,~)', 'Other', 'visRatio', 'Vis']

# Assigning respective traits to each subject
traitDict = {'B10K2': ('trimmed', 'epi'),
             'B10K4': ('trimmed', 'epi'),
             'B10K7': ('trimmed', 'epi'),
             'B1K1': ('trimmed', 'epi'),
             'B1K2': ('trimmed', 'epi'),
             'B2K2': ('trimmed', 'non'),
             'B2K4': ('trimmed', 'non'),
             'B3K4': ('control', 'non'),
             'B4K1': ('control', 'epi'),
             'B4K2': ('control', 'epi'),
             'B4K3': ('control', 'epi'),
             'B4K4': ('control', 'epi'),
             'B4K5': ('control', 'epi'),
             'B4K6': ('control', 'epi'),
             'B6K4': ('control', 'epi'),
             'B6K7': ('control', 'non'),
             'B6K6': ('control', 'non'),
             'B7K1': ('trimmed', 'epi'),
             'B7K2': ('trimmed', 'epi'),
             'B7K4': ('trimmed', 'epi'),
             'B7K6': ('trimmed', 'epi'),
             'B7K9': ('trimmed', 'epi'),
             'B8K4': ('control', 'epi'),
             'B9K3': ('control', 'epi'),
             'B9K6': ('control', 'non'),
             'B9K9': ('control', 'non')}


def analyze(filename, filedir):
    
    # Loading IC data
    data = pm.Loader(filedir + filename)
    
    # Loading IC archives introduces a bottleneck, so generate timelines
    # during each analysis
    if filename[:-4]+'.ini' not in os.listdir(filedir):
        print('\t\tTimeline not found, generating...\n')
        genTimeline.gtimeline(data, filename, filedir)
    else:
        pass

    onlyname = filename[:filename.rfind('.')]
    timeline = pm.Timeline(filedir + onlyname + '.ini')
    PHASES = timeline.sections() # Creating phases from timeline file
    
    
    Animals = list(data.getAnimal())

    visDurs = {} # Dictionary for percentage of mean duration of visits for each animal and sequence
    visNums = {} # Dictionary for percentage of number of visits for each animal and sequence
    
    for animal in Animals:
        if animal == 'B6K6':
            continue
        
        meanDict = {}
        numDict = {}

        traitList = [animal, traitDict[animal][0], traitDict[animal][1]]

        for key in stratKeys:
            meanDict[key] = np.zeros((len(PHASES),))
            numDict[key] = np.zeros((len(PHASES),))
            
        for ind, phase in enumerate(PHASES):

            start, end = timeline.getTimeBounds(phase)
            phasevisits = data.getVisits(mice = animal, start = start, end = end)
            numDict['Vis'][ind] = len(phasevisits)

            # Identifying sequences based on the side condition of nosepokes
            for visit in phasevisits:
                
                visDur = visit.Duration.total_seconds()
                meanDict['Vis'][ind] += visDur

                if len(visit.Nosepokes) == 0:
                    meanDict['0NP'][ind] += visDur
                    numDict['0NP'][ind] += 1

                elif len(visit.Nosepokes) == 1:
                    
                    if visit.Nosepokes[0].SideCondition == -1:
                        meanDict['Other'][ind] += visDur
                        numDict['Other'][ind] += 1
                    else:
                        meanDict['1NP'][ind] += visDur
                        numDict['1NP'][ind] += 1

                elif len(visit.Nosepokes) == 2:

                    if visit.Nosepokes[0].SideCondition == 0:

                        if visit.Nosepokes[1].SideCondition == 0:
                            
                                meanDict['Other'][ind] += visDur
                                numDict['Other'][ind] += 1

                        elif visit.Nosepokes[1].SideCondition == 1:

                            if visit.LickNumber != 0:
                                meanDict['(0,1,~) D'][ind] += visDur
                                numDict['(0,1,~) D'][ind] += 1

                            else:
                                meanDict['Other'][ind] += visDur
                                numDict['Other'][ind] += 1

                        elif visit.Nosepokes[1].SideCondition == -1:
                                meanDict['(0,-1,~)'][ind] += visDur
                                numDict['(0,-1,~)'][ind] += 1

                        else:
                            pass

                    else:
                        meanDict['Other'][ind] += visDur
                        numDict['Other'][ind] += 1

                elif len(visit.Nosepokes) >= 3:

                    if visit.Nosepokes[0].SideCondition == 0:

                        if visit.Nosepokes[1].SideCondition == 0:

                            if visit.Nosepokes[2].SideCondition == 1:

                                if visit.LickNumber != 0:
                                    meanDict['Other'][ind] += visDur
                                    numDict['Other'][ind] += 1

                                else:
                                    meanDict['Other'][ind] += visDur
                                    numDict['Other'][ind] += 1

                            elif visit.Nosepokes[2].SideCondition == -1:
                                meanDict['Other'][ind] += visDur
                                numDict['Other'][ind] += 1

                            elif visit.Nosepokes[2].SideCondition == 0:
                                meanDict['Other'][ind] += visDur 
                                numDict['Other'][ind] += 1

                            else:
                                pass

                        elif visit.Nosepokes[1].SideCondition == -1:
                            meanDict['(0,-1,~)'][ind] += visDur 
                            numDict['(0,-1,~)'][ind] += 1

                        elif visit.Nosepokes[1].SideCondition == 1:
                            if visit.LickNumber != 0:
                                meanDict['(0,1,~) D'][ind] += visDur
                                numDict['(0,1,~) D'][ind] += 1

                            else:
                                meanDict['Other'][ind] += visDur
                                numDict['Other'][ind] += 1
                    else:
                        meanDict['Other'][ind] += visDur
                        numDict['Other'][ind] += 1
                else:
                    pass

        # Calculating percentages for mean durations and numbers of visits
        for key in meanDict:
            if key not in ['visRatio', 'Vis', 'TotalDuration', 'SumMeans']:
                meanDict[key] = np.divide(meanDict[key], numDict[key],
                                           out=np.zeros_like(meanDict[key]), where=numDict[key]!=0)
                meanDict['visRatio'] += meanDict[key]
                meanDict[key] = traitList + list(meanDict[key])            
                numDict[key] /= numDict['Vis']*0.01
                numDict['visRatio'] += numDict[key] 
                numDict[key] = traitList + list(numDict[key])

        meanDict['TotalDuration'] = traitList + list(meanDict['Vis'])
        meanDict['SumMeans'] = traitList + list(meanDict['visRatio'])
        numDict['Vis'] = traitList + list(numDict['Vis'])
        numDict['visRatio'] = traitList + list(numDict['visRatio'])
        meanDict.pop('Vis')
        meanDict.pop('visRatio')
        visDurs[animal] =  meanDict
        visNums[animal] = numDict
    
    # Dictionary of phases for generating dataframes and spreadsheets
    phasedict = {}
    PHASES =  ['sub_id', 'treat', 'phen'] + PHASES
    for ind,val in enumerate(PHASES):
        phasedict[ind]= PHASES[ind]

    return Animals, phasedict, visDurs, visNums