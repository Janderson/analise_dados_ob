#coding: utf8
import random, sys
import numpy as np
from time import sleep 
from copy import copy
from decimal import Decimal
import pandas as pd
#from estrategiasmm import estrategia

from estrategiasmm.martingales import *
from estrategiasmm.withkelly import *


def progress(iter):
	if iter==1000: print ".",
	if iter==2000: print ".",
	if iter==3000: print ".",
	if iter==4000: print ".",
	if iter==5000: print "*",
	if iter==6000: print ".",
	if iter==7000: print ".",
	if iter==8000: print ".",
	if iter==9000: print ".",
	if iter==10000: print "*",
	if iter==15000: print ".",
	if iter==20000: print "*",
	if iter==25000: print ".",
	if iter==30000: print "*",
	if iter==35000: print ".",
	if iter==40000: print "*",
	if iter==45000: print ".",
	if iter==50000: print "*",
	if iter==55000: print ".",
	if iter==60000: print "*",


# template para os metodos de testes de estrategias
class MetodoTeste:
	def __init__(self, params, payout = [72,79,70,81], factor_win = 63, debug = False):
		self.debug = debug
		self.defaults = {"params":params, "payout": payout, "factor_win": factor_win, "debug": debug}
		self.reset_test()
		self.init_teste()

	def reset_test(self):
		params = copy(self.defaults["params"])
		self.p = params
		self.napostas, self.aposta_inicial, self.factor_win = params["numero_de_apostas"], params["aposta_inicial"], copy(self.defaults["factor_win"])
		self.conta_inicial, self.p["aposta"], self.isbroke = float(params["conta"]), params["aposta_inicial"], False
		self.p["count_apostas"], self.wincount,self.losscount = 0, 0, 0
		self.seq_loss, self.max_seqloss, self.drawdown = 0, 0, 0
		self.roll, self.max_drawdown = 0, 0
		self.maioraposta = params["aposta_inicial"]
		self.array_payout = copy(self.defaults["payout"])

	def set_test_strategy(self, test_class):
		self.main_testeclass = test_class
		self.reset_test()
		self.main_testeclass.init_estrategia(self.p, self.debug)
		#print self.p
		self.main_testeclass.s_aposta_inicial()

	def teste(self):
		Exception("Error dont set this teste")

	def init_teste(self):
		Exception("Error dont set this init_teste")

	def g_conta(self):
		if self.p["conta"] < 0:
			return 0
		else:
			return self.p["conta"]

	def showresult(self, debug=False, save_csv=None):
		result = {"apostas": str(self.p["count_apostas"]), "erros" : str(self.losscount), "acertos": str(self.wincount), "percentual": "{:.2%}".format(self.per_acerto())}
		result["_iter"] = str(self.iteracao)
		result["lucro_prejuizo"] = " %.2f" % (self.g_conta()-self.conta_inicial)
		result["max_drawdown"], result["max_seqloss"], result["broke"] = str(self.max_drawdown), str(self.max_seqloss), str(self.isbroke)
		result["estrategia"] = str(self.main_testeclass.__class__)
		result["metodo_teste"] = str(self.__class__)
		if self.debug or debug:
			print result
		if hasattr(self,"name_csv"):
			with open(self.name_csv, "a") as csv_file:
				if self.first_line_csv:
					csv_file.write(";".join(result.keys())+ ";" + ";".join(self.defaults.keys())+";" + ";".join(self.main_testeclass.defaults_estrategia.keys())+"\n")
					self.first_line_csv = False
				default_list, default_est_list = [], []

				for vl in self.defaults.values(): default_list.append(str(vl))
				for vl in self.main_testeclass.defaults_estrategia.values(): default_est_list.append(str(vl))
				csv_file.write(";".join(result.values()) + ";" + ";".join(default_list) + ";" + ";".join(default_est_list) + "\n")

	def start_csv(self, name="mmstrategy", append=False, first_line_csv=True, iteracao=0):
		self.name_csv = "result/%s.csv" % (name)
		self.iteracao= iteracao
		self.first_line_csv = first_line_csv
		if append:
			typef = "a"
		else:
			typef = "w"
		with open(self.name_csv, typef) as csv_file:
			csv_file.write("")
		return self.name_csv

	def per_acerto(self):
		if self.p["count_apostas"] != 0:
			return self.wincount/float(self.p["count_apostas"])
		else: 
			return -1

	def profit(self):
		if self.p["conta"] > self.conta_inicial:
			return 1
		else:
			return 0

	def broke(self):
		if self.isbroke: return 1
		else: return 0

	def test_win(self):
		self.wincount+=1
		payout = self.array_payout[np.random.random_integers(0,len(self.array_payout)-1)]
		pay = self.p["aposta"] * float(payout/100.0)
		self.p["conta"] += pay
		if self.debug: print ("WIN (%i%s: %s) ->" % (payout,"%", "{0}".format(pay))).ljust(22) ,
		self.drawdown = 0

	def test_loss(self):
		self.losscount+=1
		if self.seq_loss> self.max_seqloss:
			self.max_seqloss = self.seq_loss
		self.p["conta"] -= self.p["aposta"]
		self.drawdown= self.drawdown + self.p["aposta"]
		if self.drawdown> self.max_drawdown:
			self.max_drawdown = self.drawdown
		if self.debug: print "LOSS -> ".ljust(22),


	def test_loop(self, index):
		if not hasattr(self, "main_testeclass"):
			Exception("testclass nao setada use o metodo: set_test_strategy")
			return False

		if self.p["aposta"] > self.maioraposta:
				self.maioraposta = self.p["aposta"]
		if (self.p["conta"] - self.p["aposta"]) <=0:
				self.isbroke = True
				if self.debug: print "[CONTA QUEBRADA] Aposta: %s faltou: %s" % (self.p["aposta"], self.p["conta"] - self.p["aposta"] + -1)
				return False
		if self.debug: 
			print "conta: %s, drawdown: %s, max_dd: %s max_los: %s \n" % ("{0}".format(self.p["conta"]), self.drawdown, self.max_drawdown, self.max_seqloss)
			print "--- APOSTA #%s {valor: %s, maioraposta: %s, percentual_atual: %s}  ---" % (self.p["count_apostas"]+1, self.p["aposta"], self.maioraposta, "{:.2%}".format(self.per_acerto()))
		return True

#
# Executa testes aleatoreos baseados no método de monte carlos
#
class estrategiaAleatoriaMC(MetodoTeste):
	def init_teste(self):
		# rooldices
		self.max_per_seqloss=15
		self.dices = np.random.random_integers(0,100,self.p["numero_de_apostas"])

	def rollDice(self, indexdices):
		roll = self.dices[indexdices]
		self.roll = roll
		if roll == 100:
			if self.seq_loss>=self.max_per_seqloss:
				self.seq_loss=0
				return True
			self.seq_loss+=1
			return False

		elif roll <= (100-self.factor_win):
			if self.seq_loss>=self.max_per_seqloss:
				self.seq_loss=0
				return True
			self.seq_loss+=1
			return False

		elif 100 > roll > (100-self.factor_win):
			self.seq_loss=0
			return True

	def teste(self):
		for index in xrange(self.p["numero_de_apostas"]):
			if not self.test_loop(index):
				break
			if self.rollDice(index):
				self.test_win()
				self.main_testeclass.seWin()
			else:
				self.test_loss()
				self.main_testeclass.seLoss()

			self.p["count_apostas"]+=1
			if self.debug: sleep(0.1)

#
# Executa testes baseado no padrão 3 ou x velas, usando os dados gerados pelo miner_data.py
#
class estrategiaMinerData(MetodoTeste):
	def init_teste(self):
		# rooldices
		self.max_per_seqloss=15
		data_file = "minerdata/%s_%s_data.csv" % (self.p["par"], self.p["timeframe"])
		print data_file
		self.table = pd.read_csv(data_file, delimiter=";", names= ['Par','Timeframe','Date', 'trendsize', 'trend', 'candlebodysize'], parse_dates=0)
		#self.dices = np.random.random_integers(0,100,self.p["numero_de_apostas"])
		self.seq_loss = 0

	def get_row(self, index):
			return self.table.loc[index]


	def teste(self):
		for index in self.table.index.values:
			if self.isbroke:
				break
			if self.debug: print "\n################## \n\n### TEST ON ", self.get_row(index).tolist(), "   \n\n##################"
			if self.get_row(index)["trendsize"] >= self.p["start_vela"]-1:
				for iteracoes, trend  in enumerate(range(self.p["start_vela"]-2, self.get_row(index)["trendsize"])):
					trend+=1
					if self.debug: print "\n --------->TREND:", trend, "i:", iteracoes, ">", self.p["stop_vela"] 
					if ("stop_vela" in self.p and iteracoes > self.p["stop_vela"]) or (self.main_testeclass.g_stop_inc()!=-1 and iteracoes > self.main_testeclass.g_stop_inc()):
						if self.debug: print "STOP INC:",self.main_testeclass.g_stop_inc(), "iter:", iteracoes, "stop_vela", self.p["stop_vela"]
						break
					if not self.test_loop(index):
						break
					if trend == self.get_row(index)["trendsize"]:
						self.seq_loss = 0
						self.test_win()
						self.main_testeclass.seWin()
					else:
						self.seq_loss += 1
						self.test_loss()
						self.main_testeclass.seLoss()
					self.p["count_apostas"]+=1
				if self.debug: sleep(1)


if "-md" in sys.argv:
	need_init_csv = True
	for par in ["xauusd", "audusd",  "gbpjpy", "eurusd", "nzdusd", "usdjpy", "eurgbp"]:
		for timeframe in ["m30",  "h1"]:
			for start_vela in range(4,7):
				for stop_vela in range(4):
					teste_params = {"numero_de_apostas": 5, "aposta_inicial": 1, "conta": 500, "par":par, "timeframe":timeframe, "start_vela": start_vela, "stop_vela": stop_vela}
					e_mc = estrategiaMinerData(teste_params, payout=[72], debug=False)
					if need_init_csv:
						e_mc.start_csv("mmstrategy_md")
						need_init_csv = False
					else:
						e_mc.start_csv("mmstrategy_md", append=True, first_line_csv=False)
					for stop_inc in [-1]:
						for per in [1.5]:
							par_est = {"stop_inc":stop_inc, "percentual": per}
							for estrategia in [somaperda_with_kelly_est(par_est, e_mc), kelly_fraction_est(par_est, e_mc), somaperda_est(par_est, e_mc)]:
								print "ESTRATEGIA:", estrategia.__class__, "PARAMETROS:", par_est, teste_params
								e_mc.set_test_strategy(estrategia)
								e_mc.teste()
								e_mc.showresult()
							print "###\n" 
			print "-------------------\n\n"				

elif "-mc" in sys.argv:
	need_init_csv = True
	for iteracao in range(500):
		for factor_win in range(52,62,4):
			teste_params = {"numero_de_apostas": 5000, "aposta_inicial": 1, "conta": 500 }
			e_mc = estrategiaAleatoriaMC(teste_params, payout=[72,81,73,79], factor_win=factor_win, debug=False)
			if need_init_csv:
				e_mc.start_csv("mmstrategy_mc", iteracao=iteracao)
				need_init_csv = False
			else:
				e_mc.start_csv("mmstrategy_mc", append=True, first_line_csv=False, iteracao=iteracao)
			for stop_inc in [-1, 6]:
				for per in [2,5,10.0,20.0]:
					par_est = {"stop_inc":stop_inc, "percentual": per}
					for estrategia in [labouchere_est(par_est, e_mc)]:
						print "ESTRATEGIA:", estrategia.__class__, "PARAMETROS:", par_est
						e_mc.set_test_strategy(estrategia)
						e_mc.teste()
						e_mc.showresult()
					print "###\n" 
		#sleep(0.1)	
		print "-------------------\n\n"				

else:
	print "sem parametros use -mc ou -md"