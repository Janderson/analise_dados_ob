#coding: utf8
from __future__ import division
import random
from matplotlib import pyplot as plt
from mmstrategy import *


ORI_PI = 3.14159265359 # SOURCE GOOGLE
#ITERACOES=20000000 #numero ideal de iterações
ITERACOES=5000 #limite de iterações
CONTA = 250


# o metodo mc_pi observa que um bom numero de iteracoes do metodo monte carlo seria 20.000.000 
def mc_pi(iteracoes):
	sucessos = 0
	tentativas = 0
	for i in range (1, iteracoes):
	    tentativas += 1 #tentativas de calcular, que basicamente vai ser n-1
	    x, y = random.random(), random.random() #sorteia dois numeros aleatorios de 0 a 1 e atribui pra x e y
	    if (x*x + y*y) <= 1.0: # se a soma dos quadrados for menor ou igual que 1, equação do circulo (x^2 + y^2 ≤ 1^2)
	        sucessos += 1.0 #houve sucesso
	         
	pi = (sucessos / tentativas) * 4
	 
	print "Pi (%s) = %s" % (iteracoes, pi)



estrategias = [simpleestrategy,martestrategy,kellystrategy,cerstrategy, kellystrategy]

vX = []
vProfit = []
vBroke = []
c = 1

def test(estrategia):
	profit_count = 0
	broke_count = 0
	itercount = 0
	media_per = 0
	print "realizando", ITERACOES,"testes ", "em", estrategia.__name__," aguarde",
	for iter in range(1000,ITERACOES+1000):
		s = estrategia(CONTA, 5000, 1)
		s.teste()
		progress(iter)
		profit_count+= s.profit()
		broke_count+= s.broke()
		#print s.peracerto()
		media_per+= s.peracerto()
		itercount+=1
	print "[OK]"
	print "chance de ganho (%i/%i)" % (profit_count , itercount), "->",(profit_count/float(itercount))*100, "%"
	print "chance de zerar (%i/%i)" % (broke_count , itercount), "->",(broke_count/float(itercount))*100, "%"
	print "media per. acerto (%i/%i)" % (media_per , itercount), "->",(media_per/float(itercount)), "%"
	vProfit.append((profit_count/float(itercount))*100)
	vBroke.append(-(broke_count/float(itercount))*100)

for e in estrategias:
	test(e)
	vX.append(c)
	c+=1

#plt.bar(vX, vBroke, color='r', label='Simple Aposta')
#plt.bar(vX, vProfit, color='b', label='Simple Aposta')
#plt.show()

#single_test(martestrategy, 800, 250)
ORI_PI = 3.14159265359 # SOURCE GOOGLE
for i in range(100):
	mc_pi(1000000)
#mc_pi(800000)


"""mc_pi(1000)
mc_pi(10000)
mc_pi(100000)
mc_pi(10000000)
mc_pi(20000000)"""


