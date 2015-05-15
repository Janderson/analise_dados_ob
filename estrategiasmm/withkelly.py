#
# Gerenciamentos de Dinheiro Baseados no Criterio de Kelly
#
from estrategia import estrategia
import numpy as np

class somaperda_with_kelly_est(estrategia):
	def s_aposta_inicial(self):
		#self.debug = True
		self.start_percent = 0.62
		self.percentual_conta = 0.01
		self.payout = np.mean(self.tester.array_payout)
		if self.debug: print self.p["conta"], self.p, self.payout
		self.aposta_inicial = self.p["conta"] * self.percentual_conta
		self.aposta = self.aposta_inicial 
		self.index_soma = 0
		self.count_win = 0
		self.count_loss = 0
		self.count =0

	def kelly(self):
		if self.p["count_apostas"]<10:
			win_odds = self.start_percent
			loss_odds = (1-win_odds)
		else:
			win_odds = self.count_win / float(self.p["count_apostas"])
			loss_odds = self.count_loss / float(self.p["count_apostas"])
		p_kelly = ((win_odds-loss_odds)/float(self.payout))
		if p_kelly<0.0:
			p_kelly = self.percentual_conta
		return p_kelly

	def seWin(self):
		self.count_win+=1
		k = self.kelly()
		self.p["aposta"] = round( float(self.p["conta"]) * float(k))
		if self.debug: print "WIN", self.p["conta"], self.p,
		if self.index_soma>0:
			self.index_soma==0


	def seLoss(self):
		if self.count == 500:
			#raw_input(">")
			self.count = 0
		self.count +=1
		if self.index_soma==0:
			k = self.kelly()
			self.p["aposta"] = round( float(self.p["conta"]) * float(k)) * 2
			self.last_aposta = self.p["aposta"]
			self.index_soma+=1
		else:
			self.count_loss+=1
			k = self.kelly()
			self.p["aposta"] = self.last_aposta * 2 #round( float(self.p["conta"]) * float(k))
		if self.debug: print "LOSS", self.p["conta"], self.p,
		if self.debug: print "\nw/l:%s/%s payout: %s per_acerto: %s --> kelly: %s" % (self.count_win, self.count_loss, self.payout, self.tester.per_acerto(), k*100)
		if self.debug: print "APOSTA %s " % self.p["aposta"]
		return self.p["aposta"]


class kelly_fraction_est(estrategia):
	def s_aposta_inicial(self):
		#self.debug = True
		self.start_percent = 0.62
		self.payout = np.mean(self.tester.array_payout)
		if self.debug: print self.p["conta"], self.p, self.payout
		self.aposta_inicial = self.p["conta"] / 20
		self.aposta = self.aposta_inicial 
		self.count_win = 0
		self.count_loss = 0
		self.count =0

	def kelly(self):
		if self.p["count_apostas"]<10:
			win_odds = self.start_percent
			loss_odds = (1-win_odds)
			self.p_kelly = ((win_odds-(1-win_odds))/float(self.payout)) 
		else:
			win_odds = self.count_win / float(self.p["count_apostas"])
			loss_odds = self.count_loss / float(self.p["count_apostas"])
			self.p_kelly = ((win_odds-(1-win_odds))/float(self.payout)) 
		self.p["aposta"]  = round( float(self.p["conta"]) * float(self.p_kelly))
		if self.debug: print "\nwin_odds: %s w/l:%s/%s payout: %s loss_odds: %s = %s kelly: %s" % (win_odds, self.count_win, self.count_loss, self.payout, loss_odds,(1-win_odds), self.p_kelly*100)
		if self.p["aposta"] <=0:
			self.p["aposta"] = self.aposta_inicial
			if self.debug: print "APOSTA %s > %s " % (self.p["aposta"], self.aposta_inicial)
		else:
			if self.debug: print "APOSTA %s " % self.p["aposta"]
		if self.count == 500:
			#raw_input(">")
			self.count = 0
		self.count +=1
	def seWin(self):
		self.count_win+=1
		if self.debug: print "WIN", self.p["conta"], self.p,
		self.kelly()

	def seLoss(self):
		self.count_loss+=1
		if self.debug: print "LOSS", self.p["conta"], self.p,
		self.kelly()

class kellystrategyB(estrategia):
	def s_aposta_inicial(self):
		self.debug = True
		self.divisor = 10
		self.fib = [1,1,2,3,5,8,13,21,34,55,89,144,233,337,570,907,1497]
		self.aposta = self.aposta_inicial 

	def seWin(self):
		self.divisor+=1
		if self.divisor>=len(self.fib)-5:
			self.divisor=len(self.fib)-5
		self.kellycal()

	def kellycal(self):
		if self.count_apostas<10:
			win_odds = 0.65
		else:
			win_odds = float(self.peracerto()/100)

		self.aposta = round(self.fib[self.divisor] * (( self.conta * ((win_odds-(1-win_odds))/float(self.aposta)) )) )
		if self.aposta<=0:
			self.aposta = self.aposta_inicial

	def seLoss(self):
		self.divisor-=1
		if self.divisor<=0:
			self.divisor =1
		self.kellycal()

class cerstrategy(estrategia):
	def s_aposta_inicial(self):
		#self.debug = True
		self.divisor = 5
		self.aposta = self.aposta_inicial 

	def seWin(self):
		if self.count_apostas<5:
			win_odds = 0.6
		else:
			win_odds = float(self.peracerto()/100)
		self.aposta = ( self.conta * ((win_odds-(1-win_odds))/float(self.aposta)) ) / self.divisor 
		if self.aposta<=0:
			self.aposta = self.aposta_inicial

	def seLoss(self):
		self.seWin()


class guetting_est(estrategia):
	def s_aposta_inicial(self):
		self.start_percent = 0.62
		self.payout = np.mean(self.tester.array_payout)
		if self.debug: print self.p["conta"], self.p, self.payout
		self.aposta_inicial = self.p["conta"] / 20
		self.aposta = self.aposta_inicial 
		self.count_win = 0
		self.count_loss = 0
		self.count =0

	def seWin(self):
		if self.count_apostas<5:
			win_odds = 0.6
		else:
			win_odds = float(self.peracerto()/100)
		self.aposta = ( self.conta * ((win_odds-(1-win_odds))/float(self.aposta)) ) / self.divisor 
		if self.aposta<=0:
			self.aposta = self.aposta_inicial

	def seLoss(self):
		self.seWin()