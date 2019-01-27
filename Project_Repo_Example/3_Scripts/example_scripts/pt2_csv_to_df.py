# pt2_csv_to_df.py
#   by: __________
# ***************************** Run Notes ***************************** #
# - This file should be used in conjunction with the fsri-core wiki     #
#       page titled "Python Examples: pt2_csv_to_df.py", which          #
#       describes _________________                                     #
#                                                                       #
# - It provides the reader of the wiki with a concrete examples of      #
#       various topics that are discussed & should be used to follow    #
#       along with the line numbers/content referenced in the wiki      #
#                                                                       #
# - After properly editing this script based on instructions outlined   #
#       on the wiki page, execution of this script will:                #
#                                           
# ********************************************************************* #

# --------------- #
# Import packages #
# --------------- #
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- #
# Set Global Variables #
# -------------------- #
# Define directory locations
info_dir = '../../1_Info/'
events_dir = info_dir + '/Events/'
data_dir = '../../2_Data/'
plot_dir = '../../4_Plots/Example_Script_Plots/'
# Create plot directory if needed
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# ---------------------------------- #
# Load .csv File as Pandas DataFrame #
# ---------------------------------- #
# Read in channel list file as df with only argument being file's location
df_no_spec_idx = pd.read_csv(____+'________________')

# Read in channel list file again, this adding argument to specify an index column
df_idx_spec = pd.read_csv(____+'________________', index_col='_______')

# print both dataframes to compare differences
print(df_no_spec_idx)
print(df_idx_spec)
exit()

# Assign the channel column as index in df_no_spec_idx


# Compare dfs to show assignment was effective, use df.head()

# Print df.head(), df.tail()

# Show how index can be changed

# Show how index can be specified when reading in file

# Show how columns can be renamed

# Use of df.describe()

# Show how to print column labels, index values, etc.

# Use for loop to loop through data files, will analyze data in Part 3
