# -*- coding: utf-8 -*-

## pega todos os arquivos csv da pasta arquivos
## o arquivo deve OBRIGATORIAMENTE seguir o padrao nome do [PAR/ATIVO]_
## e gera um arquivao, resumo.csv
from __future__ import division
import csv, os, codecs
from time import sleep
from datetime import datetime
from decimal import *
from forexdata import FxData, IndicatorData
from strategies import StrategyBOTrend

class AnalisysData:
	def __init__(self, par, timeframe, strategy, dt_ini, dt_end):
		self.timeframe = str(timeframe)
		self.par = str(par)
		self.strategy = strategy
		self.strategy.setMain(self)
		self.escala = 100000
		self.trades = {} # dicionario com o tipo da operacao e o preco da compra/venda
		self.qtdtrades=0
		self.trade_open = False
		self.seq_trades = 0
		self.win_position = 0
		self.loss_position = 0
		self.debug = True

	#operation_buy = False -> PUT OR operation_buy = True -> CALL
	def open_trade(self, operation_type, price, date):
		if operation_type==1:
			direction = "CALL"
		else:
			direction = "PUT"
		if self.debug: print "TRADE #", selfqtd.trades, " ->",self.fname_ori, direction,", price:", price, "date:", date
		self.trades[self.qtdtrades] = (operation_type, price)
		self.qtdtrades+=1
		print 



	def close_trade(self, candle_up, candle_size=0, candle_body_size=0):
		self.trade_open = False
		if candle_up ==  self.trades[-1]:
			if self.martingale:
				self.win_position+=self.seq_trades
			else:
				self.win_position+=1
		else:
			if self.martingale:
				self.loss_position+=self.seq_trades
			else:
				self.loss_position+=1
		if self.trades[-1]:
			direction = "CALL"
		else:
			direction = "PUT"
		if self.debug: print "[CLOSE",direction,"]",candle_up, self.trades[-1], "W(",self.win_position,") L(", self.loss_position,")", candle_size, "-", candle_body_size
		if self.debug: sleep(2)

	# Limpeza do arquivo original do metatrader 
	def clear_file(self):
		fname = 'temp/dt_an'+self.fname_ori+'.csv'
		if not os.path.isfile(fname) or clear_old_data:
			destfile = open(fname, 'wb')
			i_point = 0 
			if self.debug: print ". limpando",
			
			with open(dir_of_files+self.fname_ori+'.csv', 'rb') as orifile:
				for line in orifile:
					#frag = line.split(" ")
					#if len(frag)>0:
					#	age = int(frag[0].split(".")[0])
					#	month = int(frag[0].split(".")[1])
					#	day = int(frag[0].split(".")[2])
					#if age >= ano_inicio and month>=mes_inicio and day>=dia_inicio:
					destfile.write(line)
			destfile.close()
		return fname.replace(".csv","")


			
	# conta os candles
	# estrutura resultante
	def backtest(self):
		fdt = FxData(self.par)
		df = fdt.g_data(self.timeframe)
		for i,row in df.iterrows():
			self.strategy.onTime(row.tolist())
		if self.debug: print "[ok]"
		return len(df)

	def resumo(self, format_csv=False):
		t_trade = self.win_position+self.loss_position
		char_csv = ";"
		if format_csv:
			rstring= self.par + char_csv + self.timeframe + char_csv + str(t_trade) + char_csv + str(self.win_position)
		else:
			rstring= "RESUMO (" + self.par +": "+ self.timeframe + ") -> Trades: " + str(t_trade) + "   W:" + str(self.win_position) + " Tx:" 
		if self.win_position > 0:
			if format_csv:
				rstring+= char_csv + ('%.2f' % ( (self.win_position/t_trade)*100 )) + char_csv
			else:
				rstring+= ('%.1f' % ( (self.win_position/t_trade)*100 )) + "%"
		return rstring

def list_files():
	return os.listdir(dir_of_files)


if __name__=="__main__":
	dt_ini = datetime(2014,1,1)
	dt_end = datetime(2014,9,1)
	all_count = []
	pares = ["GBPJPY"]
	timeframes = ["H1"]
	for par in pares:
		for timeframe in timeframes:
			sbo = StrategyBOTrend()
			for hipotese in range(sbo.getVariations()):
				sbo.loadParamsVariation(hipotese)
				analis = AnalisysData(par, timeframe,sbo, dt_ini, dt_end)
				r = analis.backtest()
				print analis.resumo()
			
	print "DONE"

			
