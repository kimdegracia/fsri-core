# pt4_plotting_basics.py
#   by: __________
# ***************************** Run Notes ***************************** #
# - This file should be used in conjunction with the fsri-core wiki     #
#       page titled "Python Examples: pt4_plotting_basics.py", which    #
#       describes how to use matplotlib to create figures containing    #
#       plotted channel data                                            #
#                                                                       #
# - It provides the reader of the wiki with concrete examples of        #
#       various topics that are discussed & should be used to follow    #
#       along with the line numbers/content referenced in the wiki      #
#                                                                       #
# - After properly editing this script based on instructions outlined   #
#       on the wiki page, execution of this script will:                #
#           + create figures of plotted channel data for desired        #
#               sensor groups                                           #
#           + properly format the charts based on specified criteria    #
#           + save the charts as pdfs in 4_Plots/Example_Script_Plots/  #
# ********************************************************************* #

# --------------- #
# Import Packages #
# --------------- #
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import cycle

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
channel_list = pd.read_csv(info_dir+'Data_Channels/Channel_List.csv', index_col='Channel')
test_info = pd.read_csv(info_dir+'Test_Description.csv', index_col='Test')

# Reduce channel list to only contain relevant channels
channel_df_reduced = channel_list.loc[:'GAS21', :]
channel_df_reduced = channel_df_reduced.loc[channel_df_reduced['Type']!= 'Velocity', :]

# Group channels based on primary chart label
channel_groups = channel_df_reduced.groupby('Primary_Chart')

# ------------------- #
# Set Plot Parameters #
# ------------------- #
# Set seaborn as default plot config
sns.set()
sns.color_palette('colorblind')

# Set flag to determine if axis scales should be fixed based on data type
equal_scales = True

# Define other general plot parameters
label_size = 18 # Size of x/y axis label
tick_size = 16 # Size of numbers or other labels used for tick markers
line_width = 1.5 # thickness of plot lines
event_font = 8 # size of font used for event callouts
font_rotation = 60 # rotation of event callout labels
legend_font = 10 # size of font used inside legend
fig_width = 10 # width of figure saved as pdf
fig_height = 8 # height of figure saved as pdf

# ---------------------- #
# User-Defined Functions #
# ---------------------- #
def format_and_save_plot(y_lims, x_lims, secondary_axis_label, file_loc):
    # Format primary axes
	# Set tick parameters, axes limits, & labels
	ax1.tick_params(labelsize=tick_size, length=0, width=0)

	ax1.________(bottom=y_lims[0], top=_________)
	___.set_xlim(left=_________, right=x_lims[1])
	___.__________('Time (s)', fontsize=__________)

	# Add secondary y-axis (if desired)
	if secondary_axis_label != 'None':
		ax2 = ax1.twinx()
		___.___________(___________________, l_______, _______)
		ax2.__________(____________________, ___________________)
		if secondary_axis_label == 'Temperature ($^\circ$F)':
			ax2.set_ylim([y_lim * 1.8 + 32. for y_lim in y_lims])
		else:
			ax2.set_ylim([secondary_axis_scale * y_lim for y_lim in y_lims])
		ax2.yaxis.grid(b=None)

	# Add event labels
	ax3 = ax1.twiny()
	___.set_xlim(left=_________, right=_________)
	ax3.set_xticks(Events['Time'])
	ax3.tick_params(axis='x', width=1, labelrotation=font_rotation, labelsize=event_font)
	ax3.set_xticklabels(Events['Event'], ha='left')
    ax3.xaxis.grid(b=None)
    
	# Add legend to the figure
	________, _______ = ___._________________________()
	ax1.legend(handles1, labels1, loc='best', fontsize=legend_font, 
            handlelength=3, frameon=True, framealpha=0.75)

	# Clean up whitespace padding
	fig.tight_layout()

	# Save plot to file
	plt.savefig(file_loc)
	plt.close()

# ----------------------- #
# Loop Through Data Files #
# ----------------------- #
for f in os.listdir(data_dir):
    # Skip file if not a data file
    if not (f.startswith('Test_') and f.endswith('7.csv')):
        continue

    # Get test name from f & print
    Test_Name = ______


    # Read in file & print first 4 rows of DataFrame
    exp_data = pd.read_csv(data_dir + f, index_col='Time')

    # Read in event file as df
    ______ = pd.________(_____________________)

    # Iterate through channel groups
    for _____ in ____________._____:
        # ----------------- #
        # Initialize Figure #
        # ----------------- #
        # Define figure for plotting
        ___, ___ = ___.________(_______=_______________________)
        
        # Reset marker cycle, variables for axis limits, & secondary axis label
        plot_markers = cycle(['s', 'o', '^', 'd', 'h', 'p',
                        'v', '8', 'D', '*', '<', '>', 'H'])
        x_max, y_min, y_max = 0, 0, 0
        secondary_axis_label = 'None'



        # Iterate through channels in group
        for _______ in ______________._________(_____)._____:
            # ------------------- #
            # Prepare & Plot Data #
            # ------------------- #
            # Define channel_data; grab data type & leg label from channel_df_reduced
            channel_data = ________.___[_, _______]
            data_type = __________________.___[_______, ______]
            leg_label = __________________.___[_______, _______]



            # Convert &/or filter channel_data if necessary based on data type
            if data_type == 'Temperature':
                # Apply moving average
                plot_data = channel_data.rolling(window=5, center=True).mean()
                plot_data = plot_data.dropna()

                # Set y-axis labels
                ax1.set_ylabel('Temperature ($^\circ$C)', fontsize=label_size)
                secondary_axis_label = 'Temperature ($^\circ$F)'

                if equal_scales:
                    y_max = 1200

            elif data_type == 'Pressure':
                # Define scale & offset used to convert channel_data
                scale_factor = channel_df_reduced.loc[channel, 'ScaleFactor']
                offset = channel_df_reduced.loc[channel, 'Offset']

                # Convert voltage to pressure & zero the converted data
                converted_data = channel_data * scale_factor + offset
                converted_data = converted_data - converted_data.loc[:0].mean()

                plot_data = converted_data.rolling(window=5, center=True).mean()
                plot_data = plot_data.dropna()

                # Set y-axis label
                ax1.set_ylabel('Pressure (Pa)', fontsize=label_size)

                if equal_scales:
                    y_min = -100
                    y_max = 150

            elif data_type == 'Heat Flux':
                # Get scale factor for exp from info file
                scale_factor = test_info.loc[f[:-4], channel]

                # Zero voltages & convert to HF
                zeroed_data = channel_data - channel_data.loc[:0].mean()
                converted_data = zeroed_data * scale_factor

                plot_data = converted_data.rolling(window=5, center=True).mean()
                plot_data = plot_data.dropna()

                # Set y-axis label
                ax1.set_ylabel('Heat Flux (kW/m$^2$)', fontsize=label_size)

                if equal_scales:
                    y_max = 50

            elif data_type == 'Oxygen':
                # Get scale factor & offset from channel list
                scale_factor = channel_df_reduced.loc[channel, 'ScaleFactor']
                offset = channel_df_reduced.loc[channel, 'Offset']

                # Convert voltage to oxygen
                converted_data = channel_data * scale_factor + offset

                plot_data = converted_data.rolling(window=5, center=True).mean()
                plot_data = plot_data.dropna()

                # Set y-axis label
                ax1.set_ylabel('Gas Concentration (%)', fontsize=label_size)

                if equal_scales:
                    y_max = 22

            # Plot the data
            ax1.plot(plot_data.index, plot_data, lw=line_width,
                marker=next(plot_markers), mew=3, mec='none', ms=7,
                markevery=int(plot_data.index.values[-1]/20),
                label=leg_label)

            # Check if x_max needs to be updated
            if plot_data.index.values[-1] > x_max:
                x_max = plot_data.index.values[-1]
            
            # Check if y_min & y_max need to be updated if equal_scales set to False
            if not equal_scales:
                if y_min > plot_data.min() - abs(0.1 * plot_data.min()):
                    y_min = plot_data.min() - abs(0.1 * plot_data.min())

                if y_max < 1.1 * plot_data.max():
                    y_max = 1.1 * plot_data.max()

        # -------------------- #
        # Format & Save Figure #
        # -------------------- #
        # Create dir in which to save plot (if needed)
        if not __.____.______(________ + _________):
            __.________(________ + _________)

        # Add vertical lines for event labels
        [___.axvline(_x, color='0.25', lw=1) for _x in ______['____']]

        # Format & save plot
        format_and_save_plot([_____, _____], [0, _____], ____________________,
                            plot_dir + Test_Name + '/' + group + '.pdf')
