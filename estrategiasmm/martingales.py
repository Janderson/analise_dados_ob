#
# Gerenciamentos de Dinheiro Baseados no Martingale
#
from estrategia import estrategia



class simpleestrategy(estrategia):
	def s_aposta_inicial(self):
		if not "percentual" in self.params_estrategia.keys():
			self.params_estrategia["percentual"] = 1.0
		self.p["aposta_inicial"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))
		self.p["aposta"] = self.p["aposta_inicial"] 

	def seWin(self):
		self.p["aposta"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))

	def seLoss(self):
		self.p["aposta"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))

class labouchere_est(estrategia):
	def s_aposta_inicial(self):
		self.system = []
		if not "percentual" in self.params_estrategia.keys():
			self.params_estrategia["percentual"] = 10
		if (not "stop_inc" in self.params_estrategia.keys()) or (self.params_estrategia["stop_inc"]<=0):
			self.params_estrategia["stop_inc"] = 40
		odd = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0)) / self.params_estrategia["stop_inc"]
		if self.debug: print "odd:", odd
		for i in range(self.params_estrategia["stop_inc"]):
			self.system.append(odd)
		if self.debug: print self.system
		self.aposta()

	def aposta(self):
		if len(self.system)<=1:
			self.s_aposta_inicial()
		if self.debug: print "aposta:", self.system
		payout = 0.8
		first = self.system[0]
		last = self.system[-1]
		self.p["aposta"] = round((first+last))
		if self.p["aposta"]<1: self.p["aposta"] = 1
		if self.debug: print "ret aposta", self.p["aposta"], "->", self.system

	def seWin(self):
		self.system.pop(0) 
		self.system.pop(len(self.system)-1)
		self.aposta()

	def seLoss(self):
		self.system.append(self.p["aposta"]/0.8)
		self.aposta()


class martingale_est(estrategia):
	def s_aposta_inicial(self):
		#self.debug = True
		if not "percentual" in self.params_estrategia.keys():
			self.params_estrategia["percentual"] = 1.0
		if not "stop_inc" in self.params_estrategia.keys():
			self.params_estrategia["stop_inc"] = -1
		self.p["aposta_inicial"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))
		self.p["aposta"] = self.p["aposta_inicial"] 
		self.count_mart = 0
		self.last_aposta = self.p["aposta"]

	def seWin(self):
		self.count_mart = 0
		self.p["aposta"] = self.p["aposta_inicial"]
		self.last_aposta = self.p["aposta"]

	def seLoss(self):
		limit = self.params_estrategia["stop_inc"]
		if self.debug: print "los mart-> limit: %s, count_mart: %s, last_aposta: %s " % (limit, self.count_mart, self.last_aposta)
		if limit ==-1 or self.count_mart <= limit:
			self.p["aposta"] = self.last_aposta * 2
			self.last_aposta = self.p["aposta"]
		else:
			self.p["aposta"] = self.p["aposta_inicial"]
			self.last_aposta = self.p["aposta"]

class fibo_est(estrategia):
	def s_aposta_inicial(self):
		self.debug = True
		#self.p["aposta_inicial"] = self.p["conta"] / 50.0
		self.p["aposta"] = self.p["aposta_inicial"] 
		self.index_soma = 0
		self.fib = [1,2,3,5,8,13,21,34,55,89,144,233,337,570,907,1497] # multiplicador_fibo

	def seWin(self):
		self.p["aposta"] = self.fib[self.index_soma] * self.p["aposta_inicial"]
		if self.debug: print "WIS", self.index_soma, ":", self.fib[self.index_soma]
		if self.index_soma>=1:
			self.index_soma-=1

	def seLoss(self):
		self.p["aposta"] = self.fib[self.index_soma] * self.p["aposta_inicial"]
		if self.debug: print "LIS", self.index_soma, ":", self.fib[self.index_soma]
		self.index_soma+=1

#
# params_estrategia = {"stop_inc":6, "percentual": 1.0}
class somaperda_est(estrategia):
	def s_aposta_inicial(self):
		#self.debug = True
		if not "stop_inc" in self.params_estrategia.keys():
			self.params_estrategia["stop_inc"] = 7
		if not "percentual" in self.params_estrategia.keys():
			self.params_estrategia["percentual"] = 1.0
		self.p["aposta_inicial"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))
		self.p["aposta"] = self.p["aposta_inicial"] 
		self.params_estrategia["stop_inc"]-=1
		self.index_soma = 0
		self.store = {}

	def seWin(self):
		if self.index_soma == 0:
			self.p["aposta_inicial"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))
			self.p["aposta"] = self.p["aposta_inicial"]
		elif self.index_soma == 1:
			self.p["aposta"] = self.p["aposta_inicial"]
			self.index_soma-=1
		elif self.index_soma > 1:
			self.index_soma-=1
			self.p["aposta"] = self.store[self.index_soma]
		elif self.index_soma > self.params_estrategia["stop_inc"]:
			self.index_soma=0
			self.p["aposta"] = self.p["aposta_inicial"] 



		if self.debug: print "WIS", self.index_soma, ":", self.p["aposta"]

	def store_aposta(self):
		self.store[self.index_soma] = self.p["aposta"]
		if self.debug: print "store aposta: (%s)" % self.index_soma, self.store

	def seLoss(self):
		if self.debug: print "LIS", self.index_soma, ":", self.p["aposta"]
		if self.index_soma == 0:
			self.store_aposta()
			self.p["aposta"] = self.p["aposta"]*2
		elif self.index_soma > self.params_estrategia["stop_inc"]:
			self.index_soma=0
			self.p["aposta"] = self.p["aposta_inicial"] 
		else:
			self.p["aposta"] = self.store[self.index_soma] + self.store[self.index_soma-1] # soma das se
		self.index_soma+=1
		self.store_aposta()

#
# params_estrategia = {"stop_inc":-1, "percentual": 1.0}
# estrategia no bug, muito boa
class somaperda_boa_est(estrategia):
	def s_aposta_inicial(self):
		#self.debug = True
		self.params_estrategia["stop_inc"] = -1
		if not "percentual" in self.params_estrategia.keys():
			self.params_estrategia["percentual"] = 1.0
		self.p["aposta_inicial"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))
		self.p["aposta"] = self.p["aposta_inicial"] 
		self.params_estrategia["stop_inc"]-=1
		self.index_soma = 0
		self.store = {}

	def seWin(self):
		if self.index_soma == 0:
			self.p["aposta_inicial"] = round(self.p["conta"] * (self.params_estrategia["percentual"]/100.0))
			self.p["aposta"] = self.p["aposta_inicial"]
		elif self.index_soma == 1:
			self.p["aposta"] = self.p["aposta_inicial"]
			self.index_soma-=1
		elif self.index_soma > 1:
			self.index_soma-=1
			self.p["aposta"] = self.store[self.index_soma]
		elif self.index_soma > self.params_estrategia["stop_inc"]:
			self.index_soma=0
			self.p["aposta"] = self.p["aposta_inicial"] 



		if self.debug: print "WIS", self.index_soma, ":", self.p["aposta"]

	def store_aposta(self):
		self.store[self.index_soma] = self.p["aposta"]
		if self.debug: print "store aposta: (%s)" % self.index_soma, self.store

	def seLoss(self):
		if self.debug: print "LIS", self.index_soma, ":", self.p["aposta"]
		if self.index_soma == 0:
			self.store_aposta()
			self.p["aposta"] = self.p["aposta"]*2
		elif self.index_soma > self.params_estrategia["stop_inc"]:
			self.index_soma=0
			self.p["aposta"] = self.p["aposta_inicial"] 
		else:
			self.p["aposta"] = self.store[self.index_soma] + self.store[self.index_soma-1] # soma das se
		self.index_soma+=1
		self.store_aposta()
