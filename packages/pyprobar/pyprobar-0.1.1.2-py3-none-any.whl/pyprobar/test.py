from progressbar import bar, probar
import time


def test_bar():
	N = 20
	sj = "la" * 20
	for i in range(N):
		time.sleep(0.5)
		bar(i, N, "update_random", symbol_2="o")
		print(sj, end='', flush=True)
		sj =sj[:-1]


def test_probar():
	for idx, i in probar(range(1234), symbol_2="o"):
		time.sleep(0.01)


# from colorama import Fore
test_bar()
# test_probar()