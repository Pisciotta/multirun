import os

instdir = os.path.dirname(os.path.realpath(__file__))

def createF(CMDFILE, param):
	sendir = os.path.join(instdir, "sendto")
	with open(os.path.join(sendir, CMDFILE),"w") as f:
		f.write("@echo off\ncls\npython ")
		f.write(os.path.join(instdir,"multirun.py"))
		f.write(" ")
		f.write(param)
		f.write(" %1\npause")
		f.close()

if not os.path.exists(os.path.join(instdir,"add")):
    os.makedirs(os.path.join(instdir,"add"))
	
if not os.path.exists(os.path.join(instdir,"sendto")):
    os.makedirs(os.path.join(instdir,"sendto"))
	
if not os.path.exists(os.path.join(instdir,"db")):
    os.makedirs(os.path.join(instdir,"db"))

createF("MULTIRUN___add.cmd", "append")
createF("MULTIRUN___load.cmd", "load")
createF("MULTIRUN___info.cmd", "showlog")
createF("MULTIRUN___test.cmd", "runTests")
createF("MULTIRUN___set-as-newest.cmd", "setasnewest")
createF("MULTIRUN___get-newest.cmd", "getnewest")