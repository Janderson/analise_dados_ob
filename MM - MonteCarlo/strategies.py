# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

class StrategyBO(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def onTime(self, line_data):
        """An implementation is required to return the DataFrame of symbols 
        containing the signals to go long, short or hold (1, -1 or 0)."""
        raise NotImplementedError("Should implement onTime()!")
    def getName(self):
        raise NotImplementedError("Should implement getName()!")
    
    def getParams(self, csv=False):
	"""Retorna a lista de parametros usado na strategia"""
	raise NotImplementedError("Should implement getParams()!")
    def getVariations(self):
	"""Retorna a lista de todas as variacoes da estrategia"""
	pass
    
    
    
class StrategyBOTrend(StrategyBO):
	def __init__(self, tipo ="A"):
	    # chama o analisador, para chamar as funcoes opentrade e close trade
	    self.variations = []
	    self.trend = 0
	    self.Varitions()

	def setMain(self, main):
	    self.analis = main
	    
	#operation_buy = False -> PUT OR operation_buy = True -> CALL
	def open_trade(self, operation_type, vector_op):
		if operation_type==1:
			direction = "CALL"
		else:
			direction = "PUT"
		if self.seq_trades < self.max_seq_apostas:
			self.seq_trades+=1
			if self.debug: print self.fname_ori, direction,", lastdata:", vector_op[0],", seq", self.seq_trades
			self.trade_open = True
			self.trades.append(operation_buy)
			if self.debug: sleep(1)
		else:
			if self.debug: print "max_apostas limit"



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
	
	
	def Varitions(self):
	    p = []
	    p.append({"tam_trend":3, "maxseq_apostas":2, "martingale":True, "tam_doji":10})
	    p.append({"tam_trend":5, "maxseq_apostas":2, "martingale":True, "tam_doji":10})
	    
	    self.variations = p
	    
	def loadParamsVariation(self, variation, csv=False):
	    self.tam_trend = self.variations[variation]["tam_trend"]
	    self.max_seq_apostas = self.variations[variation]["maxseq_apostas"]
	    self.martingale = self.variations[variation]["martingale"]
	    self.tam_doji = self.variations[variation]["tam_doji"]
	    
	def getParams(self, csv=False):
	    pass
	def getVariations(self):
	    return len(self.variations)
	    
	def onTime(self, line_data):
	    vdata = line_data[0]
	    vopen = float(line_data[1])
	    vhigh = float(line_data[2])
	    vlow = float(line_data[3])
	    vclose = float(line_data[4])
	    alta = False
	    baixa = False
	    
	    print "LINEDATA", line_data
	    #if self.debug: print "vdata", vdata, "vopen", vopen, "vclose", vclose,
	    if vclose > vopen + self.tam_doji:
		    alta=True
		    #if self.debug: print "[+]"
		    if self.trade_open: self.analis.close_trade(alta, vhigh-vlow, vclose-vopen) 
		    if self.trend>=0:
			    if abs(trend)>= self.tam_trend:
				    self.oanalis.pen_trade(False, vector_op)
			    trend+=1
		    else:
			    self.seq_trades=0
			    trend=1
	    if vclose+self.tam_doji < vopen:
		    baixa=True
		    #if self.debug: print "[-]"
		    if self.trade_open: self.analis.close_trade(alta, vhigh-vlow, vopen-vclose) 
		    if self.trend<=0:
			    if abs(trend)>= self.tam_trend:
				    self.analis.open_trade(True, vector_op)
			    trend-=1
		    else:
			    # Fim da tendencia atual
			    self.seq_trades=0
			    trend=-1
	    if alta == False and baixa == False:
		    #if self.debug: print "[*]"
		    self.seq_trades=0
		    if self.trend> 0:
			    if self.trade_open: self.analis.close_trade(True, vhigh-vlow) 
		    else:
			    if self.trade_open: self.analis.close_trade(False, vhigh-vlow) 
		    self.trend= 0
	    
	    i+=1
	    count_linhas=i


		