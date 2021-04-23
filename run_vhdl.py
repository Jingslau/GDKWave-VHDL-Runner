# -*- coding: utf-8 -*-

import subprocess
from subprocess import Popen, CREATE_NEW_CONSOLE
import os
import sys
 
def runVHDL(files, index, pathDir):
    for file in files:                                                                          #Loop um durch die Datein zu gehen
        
        isInPath = False
        for name in pathDir:
            if name == file:
                isInPath = True
                
        if isInPath == True:
            index += 1                                                                              # counter fuer die Bennenung unserer Testbenches
            
            print("Running " + file + " ...")
            try:                                                                                    # wir probieren alle ghdl 
                                                                                                    # commands und ueberspringen die Datei, 
                subprocess.check_output(["ghdl", "-s", file], stderr=subprocess.STDOUT)             # wenn ein Error ausgegeben wird. 
                print("Syntax-check OK")                                                            # Es folgt eine entsprechende Fehlermeldung.
                
                try:
                    subprocess.check_output(["ghdl", "-a", file], stderr=subprocess.STDOUT)
                    print("Analysis OK")
                except subprocess.CalledProcessError:
                    print ("Analysis nOK")
                    continue
                
                try:
                    file = file[:-5]
                    subprocess.check_output(["ghdl", "-e", file], stderr=subprocess.STDOUT)
                    print("Build OK")
                except subprocess.CalledProcessError:
                    print ("Build failed")
                    continue
                    
                try:
                    subprocess.check_output(["ghdl", "-r", file, "--vcd=testbench" + str(index) + ".vcd"], stderr=subprocess.STDOUT)
                    print("VCD-Dump OK")
                except subprocess.CalledProcessError:
                    print ("VCD-Dump failed")
                    continue
                    
                try:
                    print("Starting GTKWave \n")
                   # os.system('gnome-terminal -x gtkwave testbench' + "testbench" + str(index) +".vcd")
                    subprocess.Popen("gtkwave testbench" + str(index) +".vcd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    #Popen(["gtkwave", "testbench" + str(index) +".vcd"], stderr=subprocess.STDOUT, shell=True) # GTKWave wird in einem
                except subprocess.CalledProcessError:                                                                                # neuen Terminal geoeffnet
                    print("Starting GTKWave failed")
                    continue
            except subprocess.CalledProcessError:
                print ("Syntax-check nOK")
                continue
            
        elif isInPath == False:
            print (file + " could not be found \n")
            
 
        
sys.argv.pop(0)     # anpassen des Arrays der uebergebenen Datein
files = sys.argv
index = -1          
pathDir = os.listdir() # speichern der Elemente im ausführenden Verzeichnis

runVHDL(files, index, pathDir) # ausführen der Funktion 