# -*- coding: utf-8 -*-
import pandas as pd
import operator
import csv, os, codecs
from time import sleep
from decimal import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.table import Table
from time import time

DATA_FILE = "result_last.csv"
print "ANALYSIS_DATA V1: lê arquivos gerados pelo miner_data.py e gera possíveis insign, por favor, rode primeiro o miner_data"

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

def matrix_heatmap():
    t = pd.read_csv(DATA_FILE, delimiter=";", names= ['Par','Timeframe','Date', 'trendsize', 'trend', 'sequencia'], parse_dates=0)
    #print filename
    max_value = t["trendsize"].max()
    global t_heat
    t_heat =t
    # matriz [horas, trend]
    mat = np.zeros((max_value+1,24))
    for index in t.index.values:
        hour = pd.to_datetime(str(t.loc[index]["Date"])).hour
        mat[t.loc[index].values[3], hour]+=1
    a = checkerboard_table(mat, DATA_FILE)
    a.plot()
    plt.savefig("heat_map.png", format='png')
    plt.close() 
    return mat

class PatternAnalisys():
    def __init__(self, array_pattern = 
            ["p_trendcolor","p_sizefirst_c", "p_candledecinc"], result_name="pattern_analisy",
            filter_size=5, asset_timeframes={"set_assets":["gbpjpy"], "set_timeframes":["m5"]},
            remove_in_filter = []
            ):
        self.asset_timeframes = asset_timeframes
        self.array_pattern = array_pattern
        # remove os padraos que nao sao usados no filtro
        for p in remove_in_filter:
        	array_pattern.remove(p)
        self.array_pattern_filter = array_pattern
        self.patternfilename = "result/%s.csv" % result_name
        self.filter_candlesize = filter_size
        self.result_name = result_name
        self.debug = False
        with open(self.patternfilename, "w") as patternfile:
                store = ["analisy", "filter=%s" % filter_size, ",".join(array_pattern)]
                patternfile.write(";".join(store) + "\n")
    
    def p_candledecinc(self, table, index, extra_attr):
        candlebodysize = extra_attr["candlebodysize"]
        pstr=""
        for pindex in range(1, len(candlebodysize)):
            val, val_old = int(candlebodysize[pindex]),int(candlebodysize[pindex-1])
            if val>val_old:
                pstr+="+"
            elif val<val_old:
                pstr+="-"
            else:
                pstr+="-"
        return pstr
    
    def p_sizefirst_c(self, table, index, extra_attr):
        candlebodysize = extra_attr["candlebodysize"]
        pstr=""
        val_ini = int(candlebodysize[0])
        if val_ini<=20:
            pstr+="s"
        elif val_ini>=250:
            pstr+="L"
        else:
            pstr+="N"
        return pstr

    def p_trendcolor(self, table, index, extra_attr):
        pstr=""
        if extra_attr["trend"]>0:
            pstr+="^"
        else:
            pstr+="v"
        return pstr

    def p_onlycount(self, table, index, extra_attr):
        return str(extra_attr["trendsize"])
        
    def p_weekday(self, table, index, extra_attr):
    	return "|" + str(pd.to_datetime(extra_attr["date"]).weekday())

    def p_timesession(self, table, index, extra_attr):
    	hour = int(pd.to_datetime(extra_attr["date"]).hour)
    	session="p"
    	if 0 <= hour < 4: session += "1"
    	elif 4 <= hour < 8: session += "2"
    	elif 8 <= hour < 12: session += "3"
    	elif 12 <= hour < 16: session += "4"
    	elif 16 <= hour < 20: session += "5"
    	elif 20 <= hour < 24: session += "6"
    	if session == "_": print hour
        return str(session)
            
    def make_pattern(self, table, index,extra_attr):
        ## lista de padraos a serem usados
        pattern_string = ""
        for f in self.array_pattern:
            funct =  getattr(self, f)
            pattern_string+= funct(table,index,extra_attr)
        return pattern_string

    def make_pattern_filter(self, table, index,extra_attr):
        ## lista de padraos a serem usados
        pattern_string = "#"
        for f in self.array_pattern_filter:
            funct =  getattr(self, f)
            pattern_string+= funct(table,index,extra_attr)
        return pattern_string
        
    def analisy(self):
		start_time = time()
		d_result = {}
		assets_and_timeframes = [] # to report

		for asset in self.asset_timeframes["set_assets"]:
		    for timeframe in self.asset_timeframes["set_timeframes"]:

				data_file = "minerdata/%s_%s_data.csv" % (asset, timeframe)
				print "gerando patterns [%s] ->" % self.result_name, "%s:%s" % (asset, timeframe),
				if self.debug: print ""

				if not os.path.exists(data_file):
				    print " --- file notfound ---"
				else:
					assets_and_timeframes.append("%s:%s" % (asset, timeframe))
					table = pd.read_csv(data_file, delimiter=";", names= ['Par','Timeframe','Date', 'trendsize', 'trend', 'candlebodysize'], parse_dates=0)
					#print filename
					max_value = table["trendsize"].max()
					count_i = 0
					for index in table.index.values:
					    # usado para reduzir processamento
					    extra_attr = {
					        "candlebodysize": str(table.loc[index]["candlebodysize"]).split(","),
					        "date": str(table.loc[index]["Date"]),
					        "trend": int(table.loc[index]["trend"]),
					        "trendsize": int(table.loc[index]["trendsize"])
					    }

					    if int(table.loc[index]["trendsize"]) > self.filter_candlesize:
					        pstr= self.make_pattern_filter(table, index, extra_attr)
					    else:
					        pstr = self.make_pattern(table, index, extra_attr)
					    
					    if pstr in d_result.keys():
					        d_result[pstr]+=1
					    else:
					        if self.debug: print "new pattern found ", pstr
					        d_result[pstr]=1
					        
					    if count_i == 5000: 
					        print ".",
					        count_i=0
					        sleep(0.5)
					    
					    count_i+=1

					print "ok"

		with open(self.patternfilename, "a") as p1file:
			store = ["assets_and_timeframes", "", ",".join(assets_and_timeframes)]
			p1file.write(";".join(store) + "\n")
			total = 0
			for vl in d_result.values():
			    total+=vl
			sorted_dict = sorted(d_result.items(), key=operator.itemgetter(1), reverse=True)            
			for item in sorted_dict:
			    store = [item[0], str(item[1]), str((float(item[1]) / float(total) )*100)] 
			    p1file.write(";".join(store) + "\n")

		print "------------------------------\n"
		print "ANALISY DATA (%s) TERMINATED" % self.result_name
		print "pattern founded: ", len(d_result)
		elapsed_time = time() - start_time        
		print "time:",elapsed_time
		print "\n------------------------------\n",
		return d_result



if __name__=="__main__":
	set_timeframes = ["m15", "m30", "h1", "m5"]
	set_assets = ["gbpusd", "gbpjpy", "audjpy", "nzdusd", "xauusd", "eurgbp", 
	              "audusd", "eurusd", "usdchf"]
	asset_timeframes = {"set_assets": set_assets, "set_timeframes": set_timeframes}

	#
	# ANALISES    
	#
	pa = PatternAnalisys(
		array_pattern = ["p_onlycount", "p_weekday"], result_name="analis_week_", 
		filter_size=5, asset_timeframes= {"set_assets": set_assets, "set_timeframes": ["M5"]},
		remove_in_filter = ["p_onlycount"])
	pa.analisy()

	pa = PatternAnalisys(
		array_pattern = ["p_onlycount", "p_timesession", "p_weekday"], 
		result_name="analis_session_with_week_M5", 
		filter_size=5, asset_timeframes= {"set_assets": set_assets, "set_timeframes": ["M5"]},
		remove_in_filter = ["p_onlycount"]
		); 
	pa.analisy()
	pa = PatternAnalisys(
		array_pattern = ["p_timesession", "p_weekday"], 
		result_name="analis_week_nocount_M5", 
		filter_size=5, asset_timeframes= {"set_assets": set_assets, "set_timeframes": ["M5"]}); 
	pa.analisy()

	pa = PatternAnalisys(
		array_pattern = ["p_trendcolor","p_onlycount", "p_timesession", "p_weekday"], 
		result_name="analis_session_with_w_andcolor_M5", 
		filter_size=5, asset_timeframes= {"set_assets": set_assets, "set_timeframes": ["M5"]}); 
	pa.analisy()
