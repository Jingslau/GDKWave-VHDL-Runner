# -*- coding: utf-8 -*-

import subprocess
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys
 
sys.argv.pop(0)     # anpassen des Arrays der uebergebenen Datein
files = sys.argv 
index = -1

for file in files:                                                                          #Loop um durch die Datein zu gehen

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
            Popen(["gtkwave", "testbench" + str(index) +".vcd"], stderr=subprocess.STDOUT, creationflags=CREATE_NEW_CONSOLE) # GTKWave wird in einem
        except subprocess.CalledProcessError:                                                                                # neuen Terminal geoeffnet
            print("Starting GTKWave failed")
            continue
    except subprocess.CalledProcessError:
        print ("Syntax-check nOK")
        continue