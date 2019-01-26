# 1-begin_script.py
#   by: Joe Willi
# ***************************** Run Notes ***************************** #
# - This file should be used in conjunction with the instructions on    #
#       the wiki page titled "Python: Python: Example Scripts" located  #
#       in the fsri-core GitHub repo, which can be accessed via the     #
#       following link:	                                                #
#    https://github.com/ulfsri/fsri-core/wiki/Python:-Example-Scripts   #
#                                                                       #
# - The intent of this script is to guide you through the process of    #
#       initializing a Python script; that is, writing content that     #
#       should almost, if not always, come before the main body of code #
#       in a Python script                                              #
#                                                                       #
# - After adding the necessary lines of code outlined in the section on #
#       the wiki page about this file, executing the script will result #
#       in the following:                                               #
#           + specified packages being imported                         #
#           + the definition of certain global variables                #
#           + output of text via the print() function                   #
# ********************************************************************* #

# --------------- #
# Import packages #
# --------------- #
import os
import _____ as __
import _____ as __
import _____ as __

# -------------------- #
# Set Global Variables #
# -------------------- #
________________________
info_dir = '../../1_Info/'
events_dir = info_dir + ________
data_dir = _______________
plot_dir = _______________

# Uncomment lines 41/42 & build script to see failed build/error message
# for file in os.listdir(plot_dir):
#     print(file)

# Resolve error by creating directory if needed
if ____ os._____(plot_dir): 
    os._____(_____)
    print(____ + '______________________')
    
# Print each directory that's been defined above
print('Directory locations are defined as follows:')
print('  Info   ---> ' + _______)
print('  Events ---> ' + _______)
print('  Data   ---> ' + _______)
print('  Plot   ---> ' + _______)