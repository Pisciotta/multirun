import os

def createF(CMDFILE, param):
	instdir = os.path.dirname(os.path.realpath(__file__))
	sendir = os.path.join(instdir, "sendto")
	with open(os.path.join(sendir, CMDFILE),"w") as f:
		f.write("@echo off\ncls\npython ")
		f.write(os.path.join(instdir,"multirun.py"))
		f.write(" ")
		f.write(param)
		f.write(" %1\npause")
		f.close()

createF("MULTIRUN___add.cmd", "append")
createF("MULTIRUN___load.cmd", "load")
createF("MULTIRUN___info.cmd", "showlog")
createF("MULTIRUN___test.cmd", "runTests")
createF("MULTIRUN___set-as-newest.cmd", "setasnewest")
createF("MULTIRUN___get-newest.cmd", "getnewest")