import numpy as np
import matplotlib.pyplot as plt


def visualize(aggDur, aggNum, meanCorrs, posthocs, halfs, anova_pars):

    # Time series of behavioral fluctuations
    def plotGraphs(values = [], yAxName = '', xAxName = 'Phase', legName = [], saveName = '', colors = [], xticks = [], errBar = True, lineStyle = False, shading = True):
        
        fig, axe = plt.subplots(1,1, figsize = (8,5))
        tsz = 16
        
        lines = [None]*len(values)
        
        if errBar:
            if lineStyle:
                ls = ['--','-.']
            else:
                ls = ['--', '--']
            for ind, val in enumerate(values):
                if len(values) == 1:
                    axe.set_ylim([0,20])
                
                color = colors[ind]
                lines[ind] = axe.errorbar(np.arange(len(val[0])), val[0], yerr = val[1], linestyle = ls[ind], lw = 2, c = color, elinewidth = 2, capsize = 5)
        else:
            for ind, val in enumerate(values):
                color = colors[ind]
                lines[ind], = axe.plot(np.arange(len(val)), val, linestyle = '--', marker = 'o', lw = 2, c = color)
            axe.set_yticks([0,100,200,300,400,500,600])
            
        axe.set_ylabel(yAxName, fontsize = tsz)
        axe.set_xlabel(xAxName, fontsize = tsz)
        xticks = xticks
    
        if shading:
            for xind, xval in enumerate(xticks):
                if xval[1] == 'D':
                    axe.axvspan(xind-0.5, xind+0.5, color='#B0B0B0', alpha = 0.5)
    
        axe.set_xticks(np.arange(len(xticks)))
        axe.set_xticklabels(xticks)
        axe.tick_params(axis='both', labelsize=tsz-4)
        axe.set_alpha(0)
        axe.set_frame_on(False)
        lgd = axe.legend(lines, legName, framealpha=0.0, bbox_to_anchor = [0.7,1.1], ncol = len(lines), fontsize = tsz-2)
        fig.tight_layout()
        fig.savefig(saveName + '.png', bbox_inches = 'tight', dpi = 300)
        plt.close()
    
    # Bar plot of behavioral fluctuations
    def plotBars(values = [], figsize = (5,7), yAxName = '', xticklabels = [], yticks = [], xticks = [0, 0.2], saveName = '', colors = [], width = 0.1, fontsize = 20, alpha = 1, annotate = True, errBar = False, groupBar = False):
    
        fb, ab = plt.subplots(1,1, figsize = figsize)
        
        np.arange(len(xticklabels))
        width = width
        tsz = fontsize
        
        if not groupBar:
            if errBar:
                alpha = 1
                x = [0, 0.2]
                aa = ab.bar(x , values[0], yerr = values[1], width = width, color = colors, alpha = alpha)
            else:
                alpha = 1
                x = np.arange(len(values))
                aa = ab.bar(x , values, width = width, color = colors, alpha = alpha)
        else:
            alpha = 1
            x = [0, 0.4]
            bars = []
            for ind, val in enumerate(values):
                aa = ab.bar(np.array(x)+np.array(0.1*ind) , val[0], yerr = val[1], width = width, color = colors[ind], alpha = alpha)
                bars.append(aa)
                
            fb.legend(['Sham', 'Trimmed'], framealpha=0.0, bbox_to_anchor = [0.9,1.1], ncol = len(values), fontsize = tsz-3)
        
        
        def autolabel(rects, vec):
            for ind, rect in enumerate(rects):
                val = round(vec[ind],3)
                height = rect.get_height()
                ab.annotate('{}'.format(val),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 4),
                            textcoords="offset points",
                            ha='center', va='bottom',fontsize = tsz - 5, fontweight = 10)
    
        ab.set_yticks(yticks)
        ab.tick_params(axis='y', which='major', labelsize=tsz - 5)
        ab.set_ylabel(yAxName, size = tsz - 5)
        ab.set_xticks(xticks)
        ab.set_xticklabels(xticklabels, size = tsz - 5)
        ab.tick_params(axis='x',which='both',bottom=False,top=False)
    
        ab.patch.set_alpha(0.)
        ab.set_frame_on(False)
        if annotate:
            autolabel(aa, values)
        fb.tight_layout()
    
        fb.savefig(saveName + '.png', dpi=400, format='png', bbox_inches = 'tight')
        plt.close()
        
        
        
    # Pairwise t-tests of different groups
    # 1: Epileptic only, grouped by treatment
    # 2: Control only, grouped by phenotype
    sequences = ['(0,-1,~)','(0,1,~) D', '0NP', '1NP', 'Other']
    
    for half in halfs:
        betDict = posthocs[half[1]]
        pcols = half[2]
    
        for bet in betDict.keys():
    
            if bet == 'phen':
                name = half[1] + '-' + 'control'
                legs = ['Epi', 'Non']
                colors = ['darkred', 'darkblue']
                lengths = [9, 4]
            else:
                name = half[1] + '-' + 'epi'
                legs = ['Sham', 'Trimmed']
                colors = ['forestgreen', 'darkorange']
                lengths = [9, 10]
            for key in sequences[:-1]:
                temPlot = betDict[bet][key].loc[29:].set_index('phase').reindex(pcols)
                values = [(temPlot['mean(A)'], temPlot['std(A)']/np.sqrt(lengths[0])), (temPlot['mean(B)'], temPlot['std(B)']/np.sqrt(lengths[1]))]
                _ = plotGraphs(values = values,
                               yAxName = 'Group mean',
                               legName = legs,
                               saveName = key + '_' + name + '_' + bet + '_' + 'pairwise_Plot',
                               colors = colors, xticks = pcols, shading = False)
            


    # Average general activity in light vs dark phases (except two animals)
    df = aggNum['Vis']
    nVis = df[(df['sub_id'] != 'B2K2') & (df['sub_id'] != 'B2K4')]
    
    values = ((nVis.loc[:, halfs[0][2]].mean(axis=0),nVis.loc[:, halfs[0][2]].sem(axis=0)),
              (nVis.loc[:, halfs[1][2]].mean(axis=0),nVis.loc[:, halfs[1][2]].sem(axis=0)))
    
    _ = plotGraphs(values = values,
                   yAxName = 'General activity',
                   legName = ['Days', 'Nights'],
                   saveName = 'Day_Night_General_Activity',
                   colors = ['gray', 'black'],
                   xticks = ['1','2','3','4','5','6','7','8'],
                   shading = False, lineStyle = True, errBar = True)
    
    # General activity of epileptic animals grouped by treatment
    ctrl = df[(df['phen'] == 'epi') & (df['treat'] == 'control')].loc[:, halfs[1][0]]
    trim = df[(df['phen'] == 'epi') & (df['treat'] == 'trimmed')].loc[:, halfs[1][0]]
    values = ((ctrl.loc[:, halfs[1][2]].mean(axis=0),ctrl.loc[:, halfs[1][2]].sem(axis=0)),
              (trim.loc[:, halfs[1][2]].mean(axis=0),trim.loc[:, halfs[1][2]].sem(axis=0)))
    
    _ = plotGraphs(values = values,
                   yAxName = 'Group mean',
                   legName = ['Sham', 'Trimmed'],
                   saveName = 'Epi_Treat_General_Activity',
                   colors = ['forestgreen', 'darkorange'],
                   xticks = halfs[1][2], shading = False)
    
    # Mean number of visits grouped by treatment (Epileptic only)
    df = aggDur['(0,1,~) D']
    ctrl = df[(df['phen'] == 'epi') & (df['treat'] == 'control')].loc[:, halfs[1][0]]
    trim = df[(df['phen'] == 'epi') & (df['treat'] == 'trimmed')].loc[:, halfs[1][0]]
    values = ((ctrl.loc[:, halfs[1][2]].mean(axis=0),ctrl.loc[:, halfs[1][2]].sem(axis=0)),
              (trim.loc[:, halfs[1][2]].mean(axis=0),trim.loc[:, halfs[1][2]].sem(axis=0)))
    
    _ = plotGraphs(values = values,
                   yAxName = 'Group mean',
                   legName = ['Sham', 'Trimmed'],
                   saveName = 'Epi_Treat_Mean_Visits',
                   colors = ['forestgreen', 'darkorange'],
                   xticks = halfs[1][2], shading = False)
    
    
    # Effects of whisker trimming on characteristics of SWD 
    tTime = {'control': ((25.8711979, 47.987741), (4.11579693,5.55635669)),
            'trimmed': ((62.1009626, 63.7322738), (7.33861697,6.36133814)),}
    
    tNum = {'control': ((4.56475111, 7.40478165), (0.602568253,0.660836021)),
            'trimmed': ((9.43682261, 8.52896083), (0.833265136,0.693828953))}
    
    tDur = {'control': ((5.51111111, 6.41446792), (0.383131992,0.366371807)),
            'trimmed': ((6.56, 7.46233768),(0.391066917,0.456307591))}
    
    # xticks = ['5 months', '7 months']
    names = ['time', 'number', 'duration']
    
    ranges = [(20, 80, 10), (4, 12, 1), (4, 9, 1)]
    
    for ind, tdict in enumerate([tTime, tNum, tDur]):
        values = list(tdict.values())
        yRange = ranges[ind]
        _ = plotBars(values = values,
                       yAxName = '',
                       xticklabels = ['5 months', '7 months'],
                       yticks = np.arange(yRange[0], yRange[1], yRange[2]),
                       xticks = [0.05, 0.45],
                       saveName = 'Treat_Months_Bar_' + names[ind].title(),
                       colors = ['forestgreen', 'darkorange'], errBar = True, annotate = False, groupBar = True)

    # Total number of visits in light or dark phases
    values = [(2474.7, 3119.2), (228.9, 195.4)]
    colors = ['lightgray', 'dimgray']
    _ = plotBars(values = values,
                   yAxName = 'Total number of visits',
                   xticklabels = ['Light', 'Dark'],
                   yticks = np.arange(1000,4000, 500),
                   saveName = 'Total_Number_Visits_LD',
                   colors = colors, errBar = True, annotate = False)

    # Mean of visit durations grouped by treatment
    values = [(12.6, 9.1), (1.1, 1.1)]
    colors = ['forestgreen', 'darkorange']
    _ = plotBars(values = values,
                   yAxName = 'Mean duration of visits ' + r'$(S)$',
                   xticklabels = ['Trimmed', 'Sham'],
                   yticks = np.arange(4,15, 2),
                   saveName = 'Mean_Duration_Visits_Treat',
                   colors = colors, errBar = True, annotate = False)
    
    # Mean of visit durations grouped by phenotype
    values = [(9.1, 14.5), (1.1, 1.7)]
    colors = ['darkred', 'darkblue']
    _ = plotBars(values = values,
                   yAxName = 'Mean duration of visits ' + r'$(S)$',
                   xticklabels = ['Epi', 'Non'],
                   yticks = np.arange(5,18, 3),
                   saveName = 'Mean_Duration_Visits_Phen',
                   colors = colors, errBar = True, annotate = False)
    
    # Averaged activity for behavioral sequences
    piePars = [('(0,-1,~)', 'Impulsive', 'firebrick', 0),
               ('(0,1,~) D', 'Self-control', 'forestgreen', 1),
               ('0NP', 'Exploring', 'lightslategray', 2),
              ('1NP', 'Checking', 'dimgray', 3),
              ('Other', 'Misc', 'darkslategray', 4)]

    varDict = {'Mean':{}}
    for par in piePars:
        varDict['Mean'][par[0]] = aggNum[par[0]].loc[:, '1L':'8D'].mean().mean()

    fp, ap = plt.subplots(1,1, figsize = (5,5))
    tsz = 15
    
    wedges, labels = ap.pie(varDict['Mean'].values(), labels = np.array(list(varDict['Mean'].values())).round(1),
                           wedgeprops=dict(width=0.5), colors = [par[2] for par in piePars], normalize = True, startangle = 0, counterclock = True)
    
    plt.setp(labels, fontsize=tsz)
    handles, labels2 = ap.get_legend_handles_labels()
    ap.legend(handles,[par[1] for par in piePars],bbox_to_anchor = [1.05,1], frameon = False, ncol = 1, fontsize = tsz)
    fp.savefig('aggDonut.png', dpi = 400, format = 'png', bbox_inches = 'tight')
    plt.close()
    
    # Correlation of manual vs automated analysis
    rePars = [piePars[order] for order in [2, 3, 1, 0]]

    _ = plotBars(values = np.array(list(meanCorrs.values())),
                   yAxName = 'Correlation mean',
                   figsize = (7,5),
                   width = 0.5,
                   xticklabels = [par[1] for par in rePars],
                   xticks = np.arange(len(rePars)),
                   yticks = np.linspace(0,1,6),
                   saveName = 'meanCorr',
                   colors = [par[2] for par in rePars], errBar = False, annotate = True, groupBar = False)
    
    
    
