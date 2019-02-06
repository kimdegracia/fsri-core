# pt3_df_manipulation.py
#   by: __________
# ***************************** Run Notes ***************************** #
# - This file should be used in conjunction with the fsri-core wiki     #
#       page titled "Python Examples: pt3_df_manipulation.py", which    #
#       describes how to manipulate, populate, & save DataFrames        #
#                                                                       #
# - It provides the reader of the wiki with concrete examples of        #
#       various topics that are discussed & should be used to follow    #
#       along with the line numbers/content referenced in the wiki      #
#                                                                       #
# - After properly editing this script based on instructions outlined   #
#       on the wiki page, execution of this script will:                #
#           + remove unnecessary columns & rows from channel_df_reduced #
#               & exp_data                                              #
#           + convert voltage data in exp_data to the appropriate data  #
#               types                                                   #
#           + create, populate, & save a .csv file containing the max,  #
#               min, & mean values of channel data within exp_data      #
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
events_dir = info_dir + 'Events/'
data_dir = '../../2_Data/'
plot_dir = '../../4_Plots/Example_Script_Plots/'
# Create plot directory if needed
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

# ------------------------------------ #
# Load .csv Files as Pandas DataFrames #
# ------------------------------------ #
channel_list = pd.read_csv(info_dir + 'Data_Channels/Channel_List.csv', index_col='Channel')
test_info = pd.read_csv(info_dir + 'Test_Description.csv', index_col='Test')

# ----------------------- #
# Loop Through Data Files #
# ----------------------- #
for f in os.listdir(data_dir):
    # Skip file if not a data file
    if not (f.startswith('Test_') and f.endswith('7.csv')):
        continue

    # Print the file name
    print(f)

    # Read in file & print first 4 rows of DataFrame
    exp_data = pd.read_csv(data_dir + f, index_col='Time')
    # print(exp_data.head())

    # ----------------------------- #
    # Reduce channel_list DataFrame #
    # ----------------------------- #
    # Print the channel list & exit the code



    # Select only the rows up to GAS21 in channel list
    channel_df_reduced = ___________.loc[_______, _______]

    # Reduce further by selecting rows with "Type" not equal to Velocity
    channel_df_reduced = channel_df_reduced.___[_____________________, :]



    # ----------------------- #
    # Edit exp_data DataFrame #
    # ----------------------- #
    # Drop unnecessary time columns from exp_data
    ________.drop(__________________, ____________)

    # Drop all rows after 400 s
    exp_data._____(index=_____________, _____________)



    # -------------------- #
    # Convert Voltage Data #
    # -------------------- #
    for ________ in _______________._____:
        # Define column as channel_data
        channel_data = ________.___[_, ________]

        # Convert channel_data if necessary
        if channel_df_reduced.loc[channel, 'Type'] == 'Pressure':
            # Define scale & offset used to convert channel_data
            scale_factor = channel_df_reduced.loc[channel, 'ScaleFactor']
            offset = channel_df_reduced.loc[channel, 'Offset']

            # Convert voltage to pressure & zero the converted data
            converted_data = channel_data * scale_factor + offset
            converted_data = converted_data - converted_data.loc[:0].mean()

        elif ____________________.___[________, _______] == __________:
            # Get scale factor for exp from info file
            ____________ = _________.___[______, ________]

            # Zero voltages & convert to HF
            zeroed_data = ______________ - _______________.__[__].____()
            converted_data = ____________ * _____________

        elif ____________________.___[________, _______] == __________:
            # Get scale factor & offset from channel list
            ______________ = _________________.___[_________, ____________]
            ______ = ___________________.___[_______, ________]

            # Convert voltage to oxygen
            ______________ = ____________ * ____________ + ______




        # Replace voltages in exp_data with converted data
        ________.___[_, ________] = converted_data

    # ------------------------------ #
    # Compute Max, Min, Mean of Data #
    # ------------------------------ #
    # Define DataFrame to populate with computed values
    ________ = pd._________(columns=[___________________], index=________________________)



    # Iterate through index of stats_df & compute/add values
    for idx in _______________:


        # Define data for current index
        channel_data = ________.___[__, ___]

        # Define the max, min, mean of the channel data
        max_val = _____________.___()
        min_val = _____________.___()
        mean_val = _____________.___()

        # Add values to stats_df
        ________.___[___, _________] = np.round(max_val, 3)
        ________.___[___, _________] = np.round(min_val, 3)
        ________.___[___, _________] = np.round(mean_val, 3)

    # Save stats_df as csv
    stats_df.______(data_dir + _____ + _____________)

