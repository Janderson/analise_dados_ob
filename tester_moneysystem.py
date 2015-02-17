#coding: utf8
from __future__ import division
import random
from matplotlib import pyplot as plt
from mmstrategy import *

ORI_PI = 3.14159265359 # SOURCE GOOGLE
#ITERACOES=20000000 #numero ideal de iterações


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

def massive_test(estrategia):
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


def single_test(estrategia, extra_params):
	profit_count = 0
	broke_count = 0
	itercount = 0.0
	minimo_per = 100
	media_per = 0
	maximo_per = 0
	in_goal = 0

	print "realizando %s testes em %s aguarde " % (iteracoes,estrategia.__name__),
	for iter in range(1000,iteracoes+1000):
		s = estrategia(extra_params["tamanho_conta"], extra_params["qtd_apostas"], 1, debug=False)
		s.teste()
		progress(iter)
		if s.g_conta() >= objetivo:
			in_goal+=1
		profit_count+= s.profit()
		broke_count+= s.broke()
		media_per+= s.peracerto()
		if s.peracerto()> maximo_per:
			maximo_per = s.peracerto()
		if s.peracerto()< minimo_per:
			minimo_per = s.peracerto()
		if s.peracerto() > 0.5:
			s.showresult(True)
		itercount+=1

	print "[OK]"
	tax_profit = "{:.2%}".format((profit_count/itercount))
	tax_objetivo = "{:.2%}".format((in_goal/itercount))
	chance_zerar = "{:.2%}".format((broke_count/itercount))
	media_acerto = "{:.2%}".format((media_per/itercount))
	minimo_per = "{:.2%}".format((minimo_per))
	maximo_per = "{:.2%}".format((maximo_per))

	print "chance de ganho (%i/%i)" % (profit_count, itercount), "-> %s" % tax_profit
	print "chance do objetivo %s (%i/%i) -> %s" % (objetivo, in_goal, itercount, tax_objetivo)
	print "chance de zerar (%i/%i)" % (broke_count, itercount), "-> %s" % chance_zerar
	print "Per. acerto (%i/%i) " % (media_per, itercount), "-> Min: %s Med: %s Max: %s" % (minimo_per, media_acerto, maximo_per)
	tx_acertos = " %s, %s, %s" % (minimo_per, media_acerto, maximo_per)
	with open("resultado.csv", "a") as fresult:
		store=[str(estrategia.__name__), str(profit_count), str(chance_zerar), str(tx_acertos), str(tax_objetivo)]
		for i, s in enumerate(extra_params.values()):
			store.insert(i, str(s))
		fresult.write(";".join(store) + "\n")


if __name__=="__main__":
	estrategias = [simpleestrategy,martingale_est,kellystrategy,cerstrategy, somaperda_est, somaperda_with_kelly_est]
	iteracoes=50 #limite de iterações
	tamanho_conta = 1000
	objetivo = tamanho_conta * 2
	media_apostas_dia = 5
	apostas = 253*media_apostas_dia
	extra_params = {"iteracoes":iteracoes, "tamanho_conta": tamanho_conta, "objetivo":objetivo, "qtd_apostas":apostas}
	with open("resultado.csv", "w") as fresult:
		fresult.write(";".join(extra_params.keys()) + ";")
		fresult.write("estrategia; profit_count; chance_zerar; Acerto (Min,Med,Max); chance_do_objetivo;\n")
	for e in estrategias:
		single_test(e, extra_params)

	#single_test(martestrategy, 800, 250)
	ORI_PI = 3.14159265359 # SOURCE GOOGLE

