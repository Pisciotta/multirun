import sys
import os
from shutil import copyfile, copytree
import glob
import shelve

try:
	command = sys.argv[1]
	filePath = sys.argv[2]
	fileName = os.path.basename(filePath)
	currPath = os.path.realpath(__file__)
	dbPath = os.path.join(os.path.dirname(currPath), 'db', 'data1.db')
	dbPathThis = os.path.join(os.path.dirname(currPath), 'db', 'data2.db')
	dbPath3 = os.path.join(os.path.dirname(currPath), 'db', 'data3.db')
	
	def getDestinationPath(filePath):
		destFolder = getDestinationFolder(filePath)
		newName = "%s-"+os.path.basename(filePath)
		destPath = os.path.join(destFolder, newName)
		i = 0
		while os.path.exists(destPath % i):
			i += 1
		newName = str(i)+"-"+os.path.basename(filePath)
		destPath = os.path.join(destFolder, newName)
		return destPath
		
	def getDestinationFolder(filePath):
		destFolder = os.path.join(os.path.dirname(currPath), "add")
		return destFolder

	def replaceFile(filePath):
		nr = input("->")
		selected = os.path.join(os.path.dirname(currPath), "add", str(nr)+"-"+os.path.basename(filePath))
		if nr != "":
			copyfile(selected, filePath)
			s = shelve.open(dbPathThis)
			s[filePath] = str(nr)+"-"+os.path.basename(filePath)
			s.close()
		return nr
			
	def showAppendFiles(fileName):
		s = shelve.open(dbPath)
		for key in s:
			if fileName in key:
				print(key, "\n\t|________",s[key]["des"])
		s.close()			

	destPath = getDestinationPath(filePath)
	destFolder = getDestinationFolder(filePath)

	if command == "append":
		copyfile(filePath, destPath)
		des = input("Description: ")
		s = shelve.open(dbPath)
		s[os.path.basename(destPath)] = {"filename": os.path.basename(filePath), "des" : des}
		s.close()
		
		s = shelve.open(dbPathThis)
		s[filePath] = os.path.basename(destPath)
		s.close()		
		
	if command == "showlog":
		sThis = shelve.open(dbPathThis)	
		s = shelve.open(dbPath)
		for key in s:
			if fileName in key:
				if key == sThis[filePath]:
					print(key, " <<<<<<<<<\n\t|________",s[key])
				else:
					print(key, "\n\t|________",s[key])
		s.close()
		sThis.close()	
		replaceFile(filePath)
		
	if command == "load":
		s = shelve.open(dbPath)
		for key in s:
			if fileName in key:
				print(key, "\n\t|________",s[key]["des"])
		s.close()
		replaceFile(filePath)

	if command == "setasnewest":
		s = shelve.open(dbPath3)
		s["0"] = filePath
		s.close()
	
	if command == "getnewest":
		s = shelve.open(dbPath3)
		print(s["0"])
		s.close()

	if command == "runTests":
		howMany = int(input("How many tests do you want to run? "))
		print("\n")
		for i in range(0, howMany):
			dst = os.path.join(os.path.dirname(filePath),str(i+1),os.path.basename(filePath))
			copytree(filePath,dst)
		files = []

		# r=root, d=directories, f = files
		for r, d, f in os.walk(filePath):
			for file in f:
				files.append(os.path.join(r, file))
		print("All directory files:")
		for f in files:
			print(f)

		s = shelve.open(dbPath)
		logit = open("TestSetting.log","w")
		print("\n")
		for sim in range(1, howMany+1):
			print("TEST NR."+str(sim))
			print("________________________________")
			done = []
			for x_nr,x in enumerate(s):
				for f in files:
					if s[x]["filename"] not in done:
						if s[x]["filename"] in f:
							print(">"+s[x]["filename"])
							replaceThis = os.path.sep + fileName + os.path.sep
							withThis = os.path.sep + str(sim) + replaceThis
							dst = f.replace(replaceThis, withThis)
							c=input("Do you want to replace "+dst+" ? [y/n] ")
							if c == "y":
								print("\n")
								print("Select '"+s[x]["filename"]+"' version:")
								showAppendFiles(s[x]["filename"])
								ver = replaceFile(dst)
								logit.write(dst +" -> "+ver+"-"+s[x]["filename"]+"\n")
								done.append(s[x]["filename"])
							print("\n")
		logit.close()
		s.close()
	input("OK")
except Exception as e:
	print(e)
	input("Something went wrong!")