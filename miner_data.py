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


debug = True
ano_inicio = 2014
mes_inicio = 01
dia_inicio = 01
tam_para_doji = 5
tam_self.trend = 2 # TAMANHO MINIMO DA TENDENCIA
size_limit = 50
clear_old_data = True
dir_of_files = "D:/TickDataDownloader/tickdata/____COMPLETE_DATA_____/"
set_assets = ["gbpusd", "usdjpy", "audusd", "eurusd"]
set_timeframes = ["m15"]
#set_assets = ["audusd"]
DATA_RESULT= "miner_result.csv"

def list_files():
	return os.listdir(dir_of_files)


class MinerData:
	def __init__(self, file_to_miner, only_body=True):
		self.filename_miner  = file_to_miner
		self.i = 0
		self.trend = 0
		self.size_candles = []

	# Limpeza do arquivo original do metatrader 
	def clear_file(self):
		fname = 'temp/dt_an%s.csv' % self.filename_miner
		if not os.path.isfile(fname) or clear_old_data:
	         copyfile('%s%s.csv' % (dir_of_files, self.filename_miner), fname)
		return fname.replace(".csv","")

	def result_filename(self, filename, type):
		return "minerdata/%s_data.csv" % filename

	def analise(self):
		self.clear_file()
		print ". analisando", self.filename_miner,
		count_self.trend = {}
		count_linhas = 0 
		# linha dados data,open,vhigh,low,close,0
		resultcsvname = miner_filename(self.filename_miner)
		result_csv = open(resultcsvname, "a")
		with open('temp/dt_an%s.csv' % self.filename_miner, 'r') as csvfile:
			for line in csvfile:
				alta=False
				baixa=False
				sline = line.split(",")
				#print "SLINE", sline
				vdata = str(sline[0] + " "+ sline[1]).replace(".", "/")
				vopen, vhigh, vlow, vclose = Decimal(sline[2]), Decimal(sline[3]), Decimal(sline[4]), Decimal(sline[5])
				size = int( abs(vclose - vopen) * 10 ** abs(Decimal(str((vclose - vopen))).as_tuple().exponent))
				self.size_candles.append(size)
				if debug: print "##############> self.trend:", self.trend, " size:", size
				if debug: print self.filename_miner, "-> vdata", vdata, "vopen", vopen, "vclose", vclose, "size",  size, "self.trend", self.trend

				if vclose > vopen:
					alta=True
					if self.trend >=0:
						self.trend+=1
					else:
						if abs(self.trend)>= tam_self.trend:
							if debug: 
								print self.filename_miner, " BIG self.trend ", self.trend, "end data", vdata
							#print str(self.size_candles)
							result_csv.write(self.filename_miner.split("_")[0] + ";" + self.filename_miner.split("_")[1] + ";" + str(vdata) + ";" + str(abs(self.trend)) +";" + str(self.trend) 
								+";\"" + str(self.size_candles).replace("[","").replace("]","") + "\"\n")
							if not count_self.trend.has_key(abs(self.trend)):
								count_self.trend[abs(self.trend)]=1
							else:
								count_self.trend[abs(self.trend)]+=1
						self.size_candles = []
						self.trend=1
				if vclose < vopen:
					baixa=True
					if self.trend <=0:
						self.trend-=1
					else:
						# Fim da tendencia atual
						if abs(self.trend)>= tam_self.trend:
							if debug: 
								print self.filename_miner, " BIG self.trend ", self.trend, "end data", vdata
							#print str(self.size_candles)
							result_csv.write(self.filename_miner.split("_")[0] + ";" + self.filename_miner.split("_")[1] + ";" + str(vdata) + ";" + str(abs(self.trend)) +";" + str(self.trend) 
								+";\"" + str(self.size_candles).replace("[","").replace("]","") + "\"\n")
							if not count_self.trend.has_key(abs(self.trend)):
									count_self.trend[abs(self.trend)]=1
							else:
									count_self.trend[abs(self.trend)]+=1
						self.size_candles = []
						self.trend=-1
				if alta == False and baixa == False:
					self.trend=0
				

				i+=1
			count_linhas=i
		result_csv.close()
		print "[ok]"
		return count_linhas, count_self.trend

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
			md = MinerData()
			r = md.analise(filename)
			for item in r[1].iteritems():
				all_count.append((filename.upper(), filename.split("_")[0].upper() + ";" + filename.split("_")[1] + ";" + str(r[0]) +  ";" +str(item[0]) + ";" + str(item[1])))
	result_csv.close()			

	resume_f = file('resumo_miner.csv','w')
	resume_f.write("\n")
	print "gerando resumo ... ", 
	for i in all_count:
		resume_f.write(str(i[1]))
		resume_f.write("\n")

	resume_f.close()
	
	print "DONE"

			
