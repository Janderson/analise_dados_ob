#
# Gerenciamentos de Dinheiro Baseados no Criterio de Kelly
#


class somaperda_with_kelly_est(estrategia):
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

class kellystrategy(estrategia):
	def s_aposta_inicial(self, params):
		#self.debug = True
		self.aposta_inicial = self.conta / 20
		self.aposta = self.aposta_inicial 
		self.p = params

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