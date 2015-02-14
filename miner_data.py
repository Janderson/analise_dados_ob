# -*- coding: utf-8 -*-

## pega todos os arquivos csv da pasta arquivos
## o arquivo deve OBRIGATORIAMENTE seguir o padrao nome do [PAR/ATIVO]_
## e gera um arquivao, resumo.csv
import csv, os, codecs
from time import sleep

import pandas as pd
import numpy as np

from decimal import *
from shutil import copyfile
from pylab import *

debug = False
ano_inicio = 2014
mes_inicio = 01
dia_inicio = 01
tam_para_doji = 5
tam_trend = 3 # TAMANHO MINIMO DA TENDENCIA
size_limit = 50
clear_old_data = True
dir_of_files = "D:/TickDataDownloader/tickdata/____COMPLETE_DATA_____/"
set_timeframes = ["m15", "m30", "h1", "m5"]
set_assets = ["gbpusd", "gbpjpy", "audjpy", "nzdusd", "xauusd", "eurgbp", "audusd", "eurusd", "usdchf"]
DATA_RESULT= "miner_result.csv"

def list_files():
	return os.listdir(dir_of_files)

# Limpeza do arquivo original do metatrader 
def clear_file(fname_ori):
	fname = 'temp/dt_an%s.csv' % fname_ori
	if not os.path.isfile(fname) or clear_old_data:
         copyfile('%s%s.csv' % (dir_of_files, fname_ori), fname)
	return fname.replace(".csv","")


# conta os candles
# estrutura resultante
def analise_trend(fname_ori):
	print ". analisando", fname_ori,
	count_trend = {}
	count_linhas = 0 
	# linha dados data,open,vhigh,low,close,0
	resultcsvname ="minerdata/%s_data.csv" % fname_ori
	result_csv = open(resultcsvname, "a")
	with open('temp/dt_an%s.csv' % fname_ori, 'r') as csvfile:
		i = 0
		trend = 0
		size_candles = []
		for line in csvfile:
			alta=False
			baixa=False
			sline = line.split(",")
			#print "SLINE", sline
			vdata = str(sline[0] + " "+ sline[1]).replace(".", "/")
			vopen, vhigh, vlow, vclose = Decimal(sline[2]), Decimal(sline[3]), Decimal(sline[4]), Decimal(sline[5])
			size = int( abs(vclose - vopen) * 10 ** abs(Decimal(str((vclose - vopen))).as_tuple().exponent))
			size_candles.append(size)
			#print "trend:", trend, " size:", size
			if debug: print fname_ori, "-> vdata", vdata, "vopen", vopen, "vclose", vclose, "size",  size, "trend", trend

			if vclose > vopen:
				alta=True
				if trend >=0:
					trend+=1
				else:
					if abs(trend)>= tam_trend:
						if debug: 
							print fname_ori, " BIG TREND ", trend, "end data", vdata
						#print str(size_candles)
						result_csv.write(fname_ori.split("_")[0] + ";" + fname_ori.split("_")[1] + ";" + str(vdata) + ";" + str(abs(trend)) +";" + str(trend) 
							+";\"" + str(size_candles).replace("[","").replace("]","") + "\"\n")
						if not count_trend.has_key(abs(trend)):
							count_trend[abs(trend)]=1
						else:
							count_trend[abs(trend)]+=1
					size_candles = []
					trend=1
			if vclose < vopen:
				baixa=True
				if trend <=0:
					trend-=1
				else:
					# Fim da tendencia atual
					if abs(trend)>= tam_trend:
						if debug: 
							print fname_ori, " BIG TREND ", trend, "end data", vdata
						#print str(size_candles)
						result_csv.write(fname_ori.split("_")[0] + ";" + fname_ori.split("_")[1] + ";" + str(vdata) + ";" + str(abs(trend)) +";" + str(trend) 
							+";\"" + str(size_candles).replace("[","").replace("]","") + "\"\n")
						if not count_trend.has_key(abs(trend)):
								count_trend[abs(trend)]=1
						else:
								count_trend[abs(trend)]+=1
					size_candles = []
					trend=-1
			if alta == False and baixa == False:
				#size_candles = []
				if trend > 0:
					trend+=1
				else:
					trend-=1
			

			i+=1
		count_linhas=i
	result_csv.close()
	print "[ok]"
	return count_linhas, count_trend

if __name__=="__main__":
	all_count = []
	with open(DATA_RESULT, "w") as rcsvfile:
		rcsvfile.write("")

	result_csv = open(DATA_RESULT, "w")
	
	for filename in list_files():
		filename = filename.lower()
		filesplit = filename.replace(".csv", "").split("_")
		if ".csv" in filename and filesplit>1 and filesplit[1] in set_timeframes and filesplit[0] in set_assets:
			filename = filename.replace(".csv", "")
			print "analisando", filename,
			clear_file(filename)
			r = analise_trend(filename)
			for item in r[1].iteritems():
				all_count.append((filename.upper(), filename.split("_")[0].upper() + ";" + filename.split("_")[1] + ";" + str(r[0]) +  ";" +str(item[0]) + ";" + str(item[1])))
	result_csv.close()			

	print "gerando heatmap ... ",
	try: 
		matrix_heatmap(DATA_RESULT)
		print "DONE"
	except :
		print "ERRO"

	resume_f = file('resumo_miner.csv','w')
	resume_f.write("\n")
	print "gerando resumo ... ", 
	for i in all_count:
		resume_f.write(str(i[1]))
		resume_f.write("\n")

	resume_f.close()
	
	print "DONE"

			
