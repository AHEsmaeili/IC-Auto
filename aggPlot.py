import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def visualize(aggDict, betDict, meanCorrs, cStats):

    # Time series of behavioral fluctuations
    def plotgraphs(values, yAxName, legName, saveName, colors, xticks):
    
        fig, axe = plt.subplots(1,1, figsize = (8,5))
        tsz = 18
        
        lines = [None]*len(values)
        
        for ind, val in enumerate(values):
            if len(values) == 1:
                axe.set_ylim([0,20])
    
            color = colors[ind]
            lines[ind] = axe.errorbar(np.arange(len(val[0])),
                                      val[0], yerr = val[1],
                                      linestyle = '--', lw = 2,
                                      c = color, elinewidth = 2,
                                      capsize = 5)

        axe.set_ylabel(yAxName, fontsize = tsz)
        axe.set_xlabel('Phase', fontsize = tsz)
    
        for xind, xval in enumerate(xticks):
            if xval[1] == 'D':
                axe.axvspan(xind-0.5, xind+0.5, color='#B0B0B0', alpha = 0.5)
    
        axe.set_xticks(np.arange(len(xticks)))
        axe.set_xticklabels(xticks)
        axe.tick_params(axis='both', labelsize=tsz-4)
        axe.set_alpha(0)
        axe.set_frame_on(False)
        _ = axe.legend(lines, legName, framealpha=0.0,
                       bbox_to_anchor = [0.3,1.],ncol = len(lines), fontsize = tsz-2)
        fig.tight_layout()
        fig.savefig(saveName + '.png', bbox_inches = 'tight', dpi = 300)
        plt.close()  
    
        
    # Phase labels
    xticks = ['1L', '1D', '2L', '2D', '3L', '3D', '4L', '4D',
              '5L', '5D', '6L', '6D', '7L', '7D', '8L', '8D']
    sequences = ['(0,-1,~)','(0,1,~) D', '0NP', '1NP', 'Other']
    
    # Arguments for between-group plots
    for bet in betDict.keys():
        colors = ['darkred', 'darkblue']    
        if bet == 'phen':
            legs = ['Epi', 'Non']
        else:
            legs = ['Sham', 'Trimmed']
            colors = colors[::-1]
        
        for key in sequences[:-1]:
            # Pingouin sorts stats alphabetically
            # so a reindexing based on phase labels is needed
            temPlot = betDict[bet][key].loc[121:].set_index('phase').reindex(xticks)
            values = [(temPlot['mean(A)'], temPlot['std(A)']/np.sqrt(25)),
                      (temPlot['mean(B)'], temPlot['std(B)']/np.sqrt(25))]


            plotgraphs(values = values,
                       yAxName = 'Group mean',
                       legName = legs,
                       saveName = key + '_' + bet + '_' + 'pairwise_Plot',
                       colors = colors,
                       xticks = xticks);
            
    # %Visits in self-control
    legs = ['All animals']
    savename = '(0,1,~) D MeanPlot'
    axname = '%Visits'
    plotgraphs(values = cStats,
               yAxName = axname,
               legName = legs,
               saveName = savename,
               colors = ['darkblue'],
               xticks = xticks);
    
    # Arguments for pie chart and bar plot. 
    varChars = {'0NP': ('Exploring', 'lightslategray', 2),
                '1NP': ('Checking', 'dimgray', 3),
                '(0,1,~) D': ('Self-control', 'forestgreen', 1),
                '(0,-1,~)': ('Impulsive', 'firebrick', 0),
                'Other': ('Misc', 'darkslategray', 4)}

    varDict = {'Mean': {}, 'Corr': {}, 'Label': {}, 'Color': {}, 'Order': {}}

    for key in sequences:
        varDict['Mean'][key] = aggDict[key].loc[:, '1L':'8D'].mean().mean()
        varDict['Label'][key] = varChars[key][0]
        varDict['Color'][key] = varChars[key][1]
        varDict['Order'][key] = varChars[key][2]     
        
    
    # Pie chart  
    fp, ap = plt.subplots(1,1, figsize = (5,5))
    tsz = 15
    
    wedges, labels = ap.pie([mean for mean in varDict['Mean'].values()],
                            labels = np.array([mean for mean in varDict['Mean'].values()]).round(1),
                            wedgeprops=dict(width=0.5),
                            colors = [c for c in varDict['Color'].values()],
                            normalize = True,
                            startangle = 0,
                            counterclock = True)
    
    plt.setp(labels, fontsize=tsz)
    handles, labels2 = ap.get_legend_handles_labels()
    ap.legend(handles,[label for label in varDict['Label'].values()],
              bbox_to_anchor = [1.05,1], frameon = False, ncol = 1, 
              fontsize = tsz)
    fp.savefig('aggDonut.png', dpi = 400, format = 'png', bbox_inches = 'tight')
    plt.close()  

    
    # Bar plot
    fb, ab = plt.subplots(1,1, figsize = (7,5))

    # Changing bar order
    sequences = ['0NP', '1NP', '(0,1,~) D','(0,-1,~)']
    goodvalues = [meanCorrs[key] for key in sequences]

    x = np.arange(len(sequences))
    
    width = 0.5
    tsz = 20
    
    aa = ab.bar(x , goodvalues, width,
                color = [varDict['Color'][key] for key in sequences])
    
    def autolabel(rects, vec):
        for ind, rect in enumerate(rects):
            val = round(vec[ind],3)
            height = rect.get_height()
            ab.annotate('{}'.format(val),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4),
                        textcoords="offset points",
                        ha='center',
                        va='bottom',
                        fontsize = tsz - 5, fontweight = 10)
            
    ab.tick_params(axis='y', which='major', labelsize=tsz - 5)
    ab.set_ylabel('Correlation mean', size = tsz - 5)
    ab.set_xticks(x)
    ab.set_xticklabels([varDict['Label'][key] for  key in sequences], size = tsz - 5)
    ab.tick_params(axis='x', which='both', bottom=False, top=False)
    
    ab.patch.set_alpha(0.)
    ab.set_frame_on(False)
    autolabel(aa, goodvalues)
    fb.tight_layout()
    
    fb.savefig('meanCorr.png', dpi=400, format='png', bbox_inches='tight')
    plt.close()  
