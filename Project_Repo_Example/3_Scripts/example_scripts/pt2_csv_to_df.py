# pt2_csv_to_df.py
#   by: __________
# ***************************** Run Notes ***************************** #
# - This file should be used in conjunction with the fsri-core wiki     #
#       page titled "Python Examples: pt2_csv_to_df.py", which          #
#       introduces the use of the Pandas library                        #
#                                                                       #
# - It provides the reader of the wiki with a concrete examples of      #
#       various topics that are discussed & should be used to follow    #
#       along with the line numbers/content referenced in the wiki      #
#                                                                       #
# - After properly editing this script based on instructions outlined   #
#       in the wiki, execution of this script will:                     #
#           + Load .csv files to be used in the code                    #
#           + Set the index of a DataFrame                              #
#           + Load files from the data directory as DataFrames          #
# ********************************************************************* #

# --------------- #
# Import Packages #
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
print(___________)
print(___________)

# ------------------------------- #
# Set Index in Existing DataFrame #
# ------------------------------- #
# Define channel_list as df_no_spec_idx with 'Channel' column as index
__________ = ___________.set_index(_______)
print(___________)
print(___________)

# ------------------ #
# Using .iloc & .loc #
# ------------------ #
# Print only the rows in channel_list that are of type temperature
print(_________.loc[_____________, :])

# ----------------------- #
# Loop Through Data Files #
# ----------------------- #
for f in __.______(________):
    # Print the file name


    # Read in file & print first 4 rows of DataFrame

