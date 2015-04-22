import os

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.table import Table

set_timeframes = ["m15", "m30", "h1", "m5"]
set_assets = ["gbpusd", "gbpjpy", "audjpy", "usdjpy", "nzdusd", "xagusd","xauusd", "eurgbp", "audusd", "eurusd", "usdchf"]
set_timeframes = [ "m15"]
set_assets = ["audusd"]
dir_of_files = "minerdata/"
list_matriz_heat = []
def list_files():
    return os.listdir(dir_of_files)

def checkerboard_table(data, title):
    fig, ax = plt.subplots(ncols=1)
    bkg_colors=['white', 'yellow', 'lime', 'orange', 'red', 'blue', 'gray']
    ax.set_axis_off()
    ax.set_title("Analise: "+str(title))
    tb = Table(ax)
    nrows, ncols = data.shape
    width, height = 1.0 / ncols, 1.0 / nrows

    # Add cells
    for i,val in np.ndenumerate(data):
		# Index either the first or second item of bkg_colors based on
		# a checker board pattern
		color = bkg_colors[0]
		if val > 0:
			color = bkg_colors[1]
		if val > 5:
			color = bkg_colors[2]
		if val > 10:
			color = bkg_colors[3]
		if val > 25:
			color = bkg_colors[4]
		if val > 40:
			color = bkg_colors[5]
		if val > 50:
			color = bkg_colors[6]

		j = i[1]
		i = i[0]
		tb.add_cell(i, j, width, height, text=("%.f" % val), 
			loc='center', facecolor=color, edgecolor='blue')

    # Row Labels...
    for i in range(len(data[0])-1):
        tb.add_cell(i+1, -1, width, height, text=str(i+1), loc='right', 
                    edgecolor='none', facecolor='none')
    # Column Labels...
    for j in range(len(data[1])):
        tb.add_cell(0, j, width, height/2, text=str(j), loc='bottom', 
                           edgecolor='none', facecolor='none')
    ax.add_table(tb)
    return ax

def read_csv(data_file):
    m_temp = pd.read_csv(dir_of_files+data_file, delimiter=";", names= ['Par','Timeframe','Date', 'trendsize', 'trend', 'sequencia'], parse_dates=0)
    list_matriz_heat.append(m_temp)

def matrix_heatmap():
    t_heat = pd.concat(list_matriz_heat, ignore_index=True)
    max_value = t_heat["trendsize"].max()
    data_file = "teste"
    #t_heat =t
    # matriz [horas, trend]
    print "mv:", max_value
    mat = np.zeros((int(max_value)+1,24))
    for index in t_heat.index.values:
        hour = pd.to_datetime(str(t_heat.loc[index]["Date"])).hour
        mat[t_heat.loc[index].values[3], hour]+=1
    a = checkerboard_table(mat, data_file)
    a.plot()
    plt.savefig(data_file+".png", format='png')
    plt.close() 
    return mat

if __name__=="__main__":
    for filename in list_files():
        filename = filename.lower()
        filesplit = filename.replace(".csv", "").split("_")
        if ".csv" in filename and filesplit>1 and filesplit[1] in set_timeframes and filesplit[0] in set_assets:
            print "gerando", filename,
            read_csv(filename)
            #matrix_heatmap(miner_filename(filename))
            print "[ok]"
    matrix_heatmap()
