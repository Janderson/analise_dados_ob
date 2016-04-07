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
tam_trend = 2 # TAMANHO MINIMO DA TENDENCIA
size_limit = 50
clear_old_data = True
dir_of_files = "history_data/"
set_assets = ["gbpusd", "usdjpy", "audusd", "eurusd"]
set_timeframes = ["m15"]
set_assets = ["eurusd"]
#set_timeframes = ["h1"]
DATA_RESULT= "miner_result.csv"

def list_files():
	return os.listdir(dir_of_files)


class MinerData:
	def __init__(self, file_to_miner, minertype="HL", doji_size=2):
		self.doji_size = doji_size
		self.minertype = minertype  # BD - Body, HL - HighLow Juntos, H - Apenas High, L - Apenas Low
		self.filename_miner  = file_to_miner
		self.count_linhas = 0 
		self.trend = 0
		self.size_candles = []
		self.fullsize_candles = []
		self.count_trend = {}
		self.bar_data = dict()
		self.clear_resultcsv()
		self.persist_extr_data = False
		self.datafile = open('temp/dt_an%s.csv' % self.filename_miner, 'r')

	# Limpeza do arquivo original do metatrader 
	def clear_file(self):
		fname = 'temp/dt_an%s.csv' % self.filename_miner
		if not os.path.isfile(fname) or clear_old_data:
	         copyfile('%s%s.csv' % (dir_of_files, self.filename_miner), fname)
		return fname.replace(".csv","")

	def clear_resultcsv(self):
		with open(self.result_filename(), "w") as csvfile:
			csvfile.write("")

	def writeline_csv(self):
		if debug: raw_input()
		self.result_csv = open(self.result_filename(), "a")

		line = [self.filename_miner.split("_")[0], self.filename_miner.split("_")[1]] # linha 1 e 2 (par, timeframe)
		line.append(str(self.bar_data["vdata"])) 									  # linha 3 = data primeiro candle evento
		line.append(str(self.minertype))											  # linha 4 - tipo da mineraçao
		line.append(str(abs(self.trend)))
		line.append(str(self.trend))
		line.append("\""+str(self.size_candles).replace("[","").replace("]","") + "\"" )
		line.append("\""+str(self.fullsize_candles).replace("[","").replace("]","") + "\"" )
		self.extract_data(True)
		line.append(str(self.sizecandle()))
		self.result_csv.write(";".join(line) + "\n")
		self.result_csv.close()

	def result_filename(self):
		return "minerdata/%s_%s.csv" % (self.filename_miner, self.minertype)

	def end_miner(self):
		self.datafile.close()

	def store_stats(self):
		if not self.count_trend.has_key(abs(self.trend)):
			self.count_trend[abs(self.trend)]=1
		else:
			self.count_trend[abs(self.trend)]+=1

	def extract_data(self, persist=False):
		if not self.persist_extr_data:
			self.lastbar_data = self.bar_data
			line = self.datafile.readline()
			if line!='':
				sline = line.split(",")
				vdata = str(sline[0] + " "+ sline[1]).replace(".", "/")
				vopen, vhigh, vlow, vclose = Decimal(sline[2]), Decimal(sline[3]), Decimal(sline[4]), Decimal(sline[5])
				self.bar_data = dict(vdata=vdata,vopen=vopen,vhigh=vhigh,vlow=vlow,vclose=vclose)
				if debug: sleep(1)
				self.persist_extr_data = persist
			self.last_line= line
			return line
		else:
			self.persist_extr_data = False
			return self.last_line


	def gt(self): # define, dependendo do tipo de mineração se o valor é maior
		if self.minertype == "BD":
			if self.bar_data["vclose"] > self.bar_data["vopen"]:
				return True
			else:
				return False
		elif self.minertype == "HL":
			if self.lastbar_data != {} and self.bar_data["vhigh"] > self.lastbar_data["vhigh"] and self.bar_data["vlow"] > self.lastbar_data["vlow"]:
				return True
			else:
				return False

	def lt(self): # define, dependendo do tipo de mineração se o valor é maior
		if self.minertype == "BD":
			if self.bar_data["vclose"] < self.bar_data["vopen"]:
				return True
			else:
				return False
		elif self.minertype == "HL":
			if self.lastbar_data != {} and self.bar_data["vhigh"] < self.lastbar_data["vhigh"] and self.bar_data["vlow"] < self.lastbar_data["vlow"]:
				return True
			else:
				return False

	def sizecandle(self, absolute = True):
		if absolute:
			return int( abs(self.bar_data["vclose"] - self.bar_data["vopen"]) * 10 ** abs(Decimal(str((self.bar_data["vclose"] - self.bar_data["vopen"]))).as_tuple().exponent))
		else:
			return int( (self.bar_data["vclose"] - self.bar_data["vopen"]) * 10 ** abs(Decimal(str((self.bar_data["vclose"] - self.bar_data["vopen"]))).as_tuple().exponent))



	def analise(self):
		self.clear_file()
		print "analisando", self.filename_miner, " tp:", self.minertype, 
		line = self.extract_data()
		while (line != ''):
			vdata, vopen, vhigh, vlow, vclose = self.bar_data["vdata"], self.bar_data["vopen"], self.bar_data["vhigh"], self.bar_data["vlow"], self.bar_data["vclose"]
			alta=False
			baixa=False
			fullsize = int( abs(vhigh - vlow) * 10 ** abs(Decimal(str((vhigh - vlow))).as_tuple().exponent))
			self.size_candles.append(self.sizecandle())
			self.fullsize_candles.append(fullsize)
			if debug: print "\n\n\n##############> self.trend:", self.trend, " size:", self.sizecandle(), "->",self.sizecandle(False), ",",fullsize, ":", self.size_candles
			if debug: print "\nBarDt:",self.bar_data,  "\nLastBarDt:", self.lastbar_data
			if self.gt():
				alta=True
				if self.trend >=0:
					if self.trend==0: 
						self.size_candles = []
						self.fullsize_candles = []
					self.trend+=1
				else:
					if abs(self.trend)>= tam_trend:
						if debug: 
							print self.filename_miner, " ----> BIG TREND ", self.trend, "end data", vdata
						self.writeline_csv()
						self.store_stats()
					self.size_candles = []
					self.fullsize_candles = []
					self.trend=1
			if self.lt():
				baixa=True
				if self.trend <=0:
					if self.trend==0:
						self.size_candles = []
						self.fullsize_candles = []
					self.trend-=1
				else:
					# Fim da tendencia atual
					if abs(self.trend)>= tam_trend:
						if debug: 
							print self.filename_miner, " ----> BIG TREND ", self.trend, "end data", vdata
						#print str(self.size_candles)
						self.writeline_csv()
						self.store_stats()
					self.size_candles = []
					self.fullsize_candles = []
					self.trend=-1
			if alta == False and baixa == False:
				self.trend=0
			

			self.count_linhas+=1
			line = self.extract_data()
		self.end_miner()
		print "[ok]"
		return self.count_linhas, self.count_trend

if __name__=="__main__":
	#all_count = []

	
	for filename in list_files():
		filename = filename.lower()
		filesplit = filename.replace(".csv", "").split("_")
		if ".csv" in filename and filesplit>1 and filesplit[1] in set_timeframes and filesplit[0] in set_assets:
			for typem in ["BD", "HL"]:
				filename = filename.replace(".csv", "")
				md = MinerData(filename, typem)
				r = md.analise()
				#for item in r[1].iteritems():
				#	all_count.append((filename.upper(), filename.split("_")[0].upper() + ";" + filename.split("_")[1] + ";" + str(r[0]) +  ";" +str(item[0]) + ";" + str(item[1])))

	#resume_f = file('resumo_miner.csv','w')
	#resume_f.write("\n")
	#print "gerando resumo ... ", 
	#for i in all_count:
#		resume_f.write(str(i[1]))
#		resume_f.write("\n")
	#resume_f.close()
	print "DONE"

			
