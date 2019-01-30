# pt1_begin_script.py
#   by: __________
# ***************************** Run Notes ***************************** #
# - This file should be used in conjunction with the fsri-core wiki     #
#       page titled "Python Examples: pt1_begin_script.py", which       #
#       describes how to structure & things to include within the first #
#       few portions of a Python script based on fsri guidelines        #
#                                                                       #
# - It provides the reader of the wiki with a concrete examples of      #
#       various topics that are discussed & should be used to follow    #
#       along with the line numbers/content referenced in the wiki      #
#                                                                       #
# - After properly editing this script based on instructions outlined   #
#       in the wiki, execution of this script will:                     #
#           + import a number of specified modules/packages             #
#           + set variables as desired directory locations              #
#           + create directories that don't exist locally if necessary  #
#           + output of numerous lines of text to check that variables  #
#               have been defined properly                              #
# ********************************************************************* #

# --------------- #
# Import Packages #
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

# --------------- #
# Check Your Work #
# --------------- #
# Print each directory that's been defined above
print('Directory locations are defined as follows:')
print('  Info   ---> ' + _______)
print('  Events ---> ' + _______)
print('  Data   ---> ' + _______)
print('  Plot   ---> ' + _______)