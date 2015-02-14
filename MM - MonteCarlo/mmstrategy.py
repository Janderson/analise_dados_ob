import random
import numpy as np
from time import sleep 


class estrategiaWoOptimized:
	def __init__(self, conta, numero_de_apostas, aposta_inicial, payout = 81):
		self.debug = False
		self.napostas = numero_de_apostas
		self.aposta_inicial = aposta_inicial
		self.conta_inicial = conta
		self.conta = conta
		self.count_apostas = 0 
		self.wincount = 0
		self.losscount = 0
		self.payout = float(payout) / 100
		self.s_aposta_inicial()
		self.seq_loss=0
		self.max_seqloss=15

	def s_aposta_inicial(self):
		exception("Error dont set this apostainicial")

	def rollDice(self):
		roll = random.randint(1,100)
		fctorwin = 45
		if roll == 100:
			if self.seq_loss>=self.max_seqloss:
				self.seq_loss=0
				return True
			self.seLoss()
			self.seq_loss+=1
			return False

		elif roll <= fctorwin:
			if self.seq_loss>=self.max_seqloss:
				self.seq_loss=0
				return True
			self.seq_loss+=1
			return False

		elif 100 > roll > fctorwin:
			return True

	def seWin(self):
		exception("Error dont set this seWin")

	def seLoss(self):
		exception("Error dont set this seLoss")

	def teste(self):
		for i in range(self.napostas):
			if self.debug: print "aposta #"+str(i)+ " (",self.aposta,", ", "%2f" % float(self.conta),") ->"
			if self.rollDice():
				self.wincount+=1
				self.conta += self.aposta * self.payout
				self.seWin()
			else:
				self.losscount+=1
				self.conta -= self.aposta
				self.seLoss()

			if self.conta <=0:
				if self.debug: print "quebrado"
				break
			if self.debug: sleep(0.2)
			self.count_apostas+=1

		self.showresult()

	def g_conta(self):
		if self.conta < 0:
			return 0
		else:
			return self.conta

	def showresult(self):
		if self.debug:
			print "para",self.napostas, "erros: ", self.losscount, " acertos: ", self.wincount, " percentual: ", self.peracerto() , " conta: ", self.g_conta(), "\n"


	def peracerto(self):
		return (self.wincount / float(self.count_apostas))*100

	def profit(self):
		if self.conta> self.conta_inicial:
			return 1
		else:
			return 0

	def broke(self):
		if self.conta<=0:
			return 1
		else:
			return 0

# classe estrategia otimizada pelo numpy
class estrategia:
	def __init__(self, conta, numero_de_apostas, aposta_inicial, payout = 81):
		self.debug = False
		self.napostas = numero_de_apostas
		self.aposta_inicial = aposta_inicial
		self.conta_inicial = conta
		self.conta = conta
		self.count_apostas = 0 
		self.wincount = 0
		self.losscount = 0
		self.payout = float(payout) / 100
		self.s_aposta_inicial()
		self.seq_loss=0
		self.max_seqloss=15

	def s_aposta_inicial(self):
		exception("Error dont set this apostainicial")

	def rollDices(self):
		self.dices = np.random.random_integers(0,100,self.napostas)

	def rollDice(self, indexdices):
		roll = self.dices[indexdices]
		fctorwin = 58
		if roll == 100:
			if self.seq_loss>=self.max_seqloss:
				self.seq_loss=0
				return True
			self.seLoss()
			self.seq_loss+=1
			return False

		elif roll <= fctorwin:
			if self.seq_loss>=self.max_seqloss:
				self.seq_loss=0
				return True
			self.seq_loss+=1
			return False

		elif 100 > roll > fctorwin:
			return True

	def seWin(self):
		exception("Error dont set this seWin")

	def seLoss(self):
		exception("Error dont set this seLoss")

	def teste(self):
		self.rollDices()
		for i in range(self.napostas):
			if self.debug: print "aposta #"+str(i)+ " (",self.aposta,", ", "%2f" % float(self.conta),") ->"
			if self.rollDice(i):
				self.wincount+=1
				self.conta += self.aposta * self.payout
				self.seWin()
			else:
				self.losscount+=1
				self.conta -= self.aposta
				self.seLoss()

			if self.conta <=0:
				if self.debug: print "quebrado"
				break
			if self.debug: sleep(0.2)
			self.count_apostas+=1

		self.showresult()

	def g_conta(self):
		if self.conta < 0:
			return 0
		else:
			return self.conta

	def showresult(self):
		if self.debug:
			print "para",self.napostas, "erros: ", self.losscount, " acertos: ", self.wincount, " percentual: ", self.peracerto() , " conta: ", self.g_conta(), "\n"


	def peracerto(self):
		return (self.wincount / float(self.count_apostas))*100

	def profit(self):
		if self.conta> self.conta_inicial:
			return 1
		else:
			return 0

	def broke(self):
		if self.conta<=0:
			return 1
		else:
			return 0



class simpleestrategy(estrategia):
	def s_aposta_inicial(self):
		self.aposta = self.aposta_inicial

	def seWin(self):
		pass
	def seLoss(self):
		pass

class martestrategy(estrategia):
	def s_aposta_inicial(self):

		self.limit = self.il =round(250/20)
		self.aposta = self.aposta_inicial

	def seWin(self):
		self.il = 0
		self.aposta = self.aposta_inicial

	def seLoss(self):
		if self.il<=0:
			self.aposta = self.aposta_inicial
			self.il = self.limit
		else:
			self.il-=1
			self.aposta+= self.aposta

class kellystrategy(estrategia):
	def s_aposta_inicial(self):
		#self.debug = True
		self.aposta_inicial = self.conta / 20
		self.aposta = self.aposta_inicial 

	def seWin(self):
		if self.count_apostas<10:
			win_odds = 0.6
		else:
			win_odds = float(self.peracerto()/100)
		self.aposta = round(( self.conta * ((win_odds-(1-win_odds))/float(self.aposta)) ) )
		if self.aposta<=0:
			self.aposta = self.aposta_inicial

	def seLoss(self):
		self.seWin()

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


def single_test(estrategia, ITERACOES, CONTA):
	profit_count = 0
	broke_count = 0
	itercount = 0
	media_per = 0
	print "realizando", ITERACOES,"testes ", "em", estrategia.__name__," aguarde",
	for iter in range(1000,ITERACOES+1000):
		s = estrategia(CONTA, 80000, 1)
		s.teste()
		progress(iter)
		profit_count+= s.profit()
		broke_count+= s.broke()
		media_per+= s.peracerto()
		itercount+=1
	print "[OK]"
	print "chance de ganho (%i/%i)" % (profit_count , itercount), "->",(profit_count/float(itercount))*100, "%"
	print "chance de zerar (%i/%i)" % (broke_count , itercount), "->",(broke_count/float(itercount))*100, "%"
	print "media per. acerto (%i/%i)" % (media_per , itercount), "->",(media_per/float(itercount)), "%"

