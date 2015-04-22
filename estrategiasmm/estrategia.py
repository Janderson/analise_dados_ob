from copy import copy
## Classe template para as estrategias
class estrategia:
	def __init__(self, params_estrategia, tester):
		self.defaults_estrategia= copy(params_estrategia)
		self.params_estrategia = params_estrategia
		self.tester = tester

	def init_estrategia(self, params, debug):
		self.p = params
		self.debug = debug

	def g_stop_inc(self):
		return self.defaults_estrategia["stop_inc"]

	def seWin(self):
		exception("Error dont set this seWin")

	def seLoss(self):
		exception("Error dont set this seLoss")

	def per_acerto(self):
		return self.tester.per_acerto()
