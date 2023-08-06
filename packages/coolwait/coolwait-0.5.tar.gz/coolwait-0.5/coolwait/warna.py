import random as ran
import time

#author: KANG-NEWBIE a.k.a Noobie
#Python3
stop=False
def pelangi(word,delay=None,tab=None):
	if tab:
		ct=["\t" for i in range(tab)]
	else:
		ct=''
	start=time.time()
	while 1:
		myl=[f"\033[9{ran.randint(0,9)}m{x}" for x in word]
		print(end=f"{''.join(ct)}"+f"{''.join(myl)}"+"\r",flush=True)
		if stop:
			break
		elif delay:
			if int(time.time()-start) == int(delay):
				break
		time.sleep(0.1)
	print(end=f"\r{'   '.join('    '*len(word))}\r\033[97m",flush=True)
