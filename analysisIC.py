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
    if filename[:-4]+'.ini' not in os.listdir(os.getcwd()):
        print('\t\tTimeline not found, generating...\n')
        genTimeline.gtimeline(data, filename, filedir)
    else:
        pass

    onlyname = filename[:filename.rfind('.')]
    timeline = pm.Timeline(filedir + onlyname + '.ini')
    PHASES = timeline.sections() # Creating phases from timeline file
    
    
    Animals = list(data.getAnimal())

    aniDict = {}
    
    
    for animal in Animals:
        
        if animal == 'B6K6': # Subject B6K6 is omitted from the analysis
            continue
        
        stratDict = {}  # Results dict.
        traitList = [animal, traitDict[animal][0], traitDict[animal][1]] # A list of trait strings

        for key in stratKeys:
            stratDict[key] = np.zeros((len(PHASES),)) # Initializing sequences
            
        for ind, phase in enumerate(PHASES):

            start, end = timeline.getTimeBounds(phase)
            phasevisits = data.getVisits(mice = animal, start = start, end = end)
            stratDict['Vis'][ind] = len(phasevisits)

            # Assignign to each sequence based on NP number and SideCondition
            for visit in phasevisits:

                if len(visit.Nosepokes) == 0:
                    stratDict['0NP'][ind] += 1

                elif len(visit.Nosepokes) == 1:
                    
                    if visit.Nosepokes[0].SideCondition == -1:
                        stratDict['Other'][ind] += 1
                    else:
                        stratDict['1NP'][ind] += 1

                elif len(visit.Nosepokes) == 2:

                    if visit.Nosepokes[0].SideCondition == 0:

                        if visit.Nosepokes[1].SideCondition == 0:

                            stratDict['Other'][ind] += 1

                        elif visit.Nosepokes[1].SideCondition == 1:

                            if visit.LickNumber != 0:
                                stratDict['(0,1,~) D'][ind] += 1
                            else:
                                stratDict['Other'][ind] += 1

                        elif visit.Nosepokes[1].SideCondition == -1:
                            stratDict['(0,-1,~)'][ind] += 1
                        else:
                            pass

                    else:
                        stratDict['Other'][ind] += 1

                elif len(visit.Nosepokes) >= 3:

                    if visit.Nosepokes[0].SideCondition == 0:

                        if visit.Nosepokes[1].SideCondition == 0:

                            if visit.Nosepokes[2].SideCondition == 1:

                                if visit.LickNumber != 0:
                                    stratDict['Other'][ind] += 1
                                else:
                                    stratDict['Other'][ind] += 1

                            elif visit.Nosepokes[2].SideCondition == -1:
                                stratDict['Other'][ind] += 1

                            elif visit.Nosepokes[2].SideCondition == 0:
                                stratDict['Other'][ind] += 1 
                            else:
                                pass

                        elif visit.Nosepokes[1].SideCondition == -1:
                            stratDict['(0,-1,~)'][ind] += 1 

                        elif visit.Nosepokes[1].SideCondition == 1:
                            if visit.LickNumber != 0:
                                stratDict['(0,1,~) D'][ind] += 1
                            else:
                                stratDict['Other'][ind] += 1
                    else:
                        stratDict['Other'][ind] += 1
                else:
                    pass

        # Converting sequences to %visits, and adding the trait strings
        for key in stratDict:
            if key not in ['visRatio', 'Vis']:
                stratDict[key] /= stratDict['Vis']*0.01
                stratDict['visRatio'] += stratDict[key] 
                stratDict[key] = traitList + list(stratDict[key])

        stratDict['Vis'] = traitList + list(stratDict['Vis'])
        stratDict['visRatio'] = traitList + list(stratDict['visRatio'])

        aniDict[animal] = stratDict
    
    # Header info for dataframes and spreadsheets
    phaseDict = {}
    PHASES = ['sub_id', 'treat', 'phen'] + PHASES
    for ind, val in enumerate(PHASES):
        phaseDict[ind] = PHASES[ind]

    return Animals, phaseDict, aniDict
