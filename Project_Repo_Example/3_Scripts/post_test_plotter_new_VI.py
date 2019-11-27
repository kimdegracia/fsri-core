# post_test_plotter.py
#   by: J. Willi
# ***************************** Run Notes ***************************** #
# - Script used to generate data plots from files output by v2.3.1.1 of #
#       DAQ VI                                                          #
#                                                                       #
# - If plot_all = True, plots will be generated for all data files      #
#       present in data_dir                                             #
#                                                                       #
# - Script assumes csv or TDMS data file has been copied from DAQ       #
#       output directory to repo dir defined as data_dir                #
#       + if TDMS file is found, file will be converted to csv          #
#       + if csv file is found, timestamp will be removed from file's   #
#           name                                                        #
#                                                                       #
# - Script is written to get gas lag times from file in info_dir named  #
#       "Test_Description.csv" that contains columns for each gas group #
#       with inputs corresponding to lag times                          #
# ********************************************************************* #

# --------------- #
# Import Packages #
# --------------- #
import os
import socket
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.signal import savgol_filter
from itertools import cycle
from nptdms import TdmsFile
from pathlib import Path

# ---------------------------------- #
# Define Subdirectories & Info Files #
# ---------------------------------- #
repo_dir = Path.cwd() / '..'
info_dir = repo_dir / '01_Info'
data_dir = repo_dir / '02_Data'
plot_dir = repo_dir / '04_Charts'

# Read in channel list file & create list of sensor groups
channel_list = pd.read_csv(info_dir / 'channel_list.csv', index_col='Channel_Name')
channel_groups = channel_list.groupby('Chart')

test_info = pd.read_csv(info_dir / 'Test_Description.csv', index_col='Test')

# ------------------- #
# Set Plot Parameters #
# ------------------- #
plot_all = True    # if true, generate plots for every test

# Set seaborn as default plot config; define line & background colors, list of markers
sns.set()
sns.set_palette("deep")
sns.set_style("darkgrid", {"axes.facecolor": ".88"})

line_markers = ['s', 'o', '^', 'd', 'h', 'p','v', '8', 'D', '*', '<', '>', 'H']

# Define other general plot parameters
label_size = 18
tick_size = 16
line_width = 2
event_font = 10
font_rotation = 60
legend_font = 10
fig_width = 8
fig_height = 6

# ------------------------------------- #
# Convert new .tdms files to .csv files #
# ------------------------------------- #
for file_name in os.listdir(data_dir):
    if file_name.endswith('.tdms'):
        # Grab csv file name from tdms file name
        csv_name = file_name[:-21]

        # Create new csv files if they don't exist in data dir
        if not os.path.isfile(data_dir / f'{csv_name}.csv'):
            print('    Creating data & event csv files for ' + csv_name)
            # Read tdms file & convert to dataframe
            tdms_file = TdmsFile(data_dir / file_name)
            tdms_df = tdms_file.as_dataframe()

            # Create empty dataframes for data & event info
            data_df = pd.DataFrame()
            event_df = pd.DataFrame()
            # Loop through tdms file columns & populate dataframes
            for column in tdms_df.columns:
                if column.split('/')[1] == "'Channels'":
                    data_df[column.split('/')[-1][1:-1]] = tdms_df[column]
                elif column.split('/')[1] == "'Events'":
                    event_df[column.split('/')[-1][1:-1]] = tdms_df[column].dropna()

            data_df.set_index('Time', inplace=True)

            # Add events col to data_df; info lines above header, & save as csv
            data_df['Event'] = ''
            if not event_df.empty:
                event_df.set_index('Time', inplace=True)
                for event_idx in event_df.index.values:
                    idx = f'{event_idx[:10]} {event_idx[11:]}'
                    if idx in data_df.index:
                        data_df.loc[idx, 'Event'] = event_df.loc[event_idx, 'Event']
                    else:
                        ss = int(idx[-2:])
                        if ss != 0:
                            new_index = idx[:-2] + format(ss - 1, '02d')
                        else:
                            mm = int(idx[-5:-3])
                            if mm != 0:
                                new_index = idx[:-5] + format(mm - 1, '02d') + ':59'
                            else:
                                hh = int(idx[-8:-6])
                                new_index = idx[:-8] + format(hh - 1, '02d') + ':'.join(['59', '59'])

                        data_df.loc[new_index, 'Event'] = event_df.loc[event_idx, 'Event']

            full_csv = open(data_dir / f'{csv_name}.csv', "w")
            full_csv.write(f'Test Name,{csv_name}' + "\n")
            for label in ['Engineer', 'Location', 'Test Info']:
                full_csv.write(f'{label},' + "\n")
            full_csv.write("\n")
            full_csv.write("\n")
            data_df.to_csv(full_csv, index_label='Time')
            full_csv.close()

            print('    Saved ' + csv_name + '.csv')
            print()

    elif file_name.endswith('.csv'):
        # Drop timestamp from end of file name if present
        if len(file_name.split('_')[-1]) == 19:
            if len(file_name[-19:].split('-')) == 4:
                os.rename(data_dir / file_name, data_dir / f'{file_name[:-20]}.csv')

# ---------------------- #
# User-Defined Functions #
# ---------------------- #
def timestamp_to_seconds(timestamp):
    timestamp = timestamp.split(' ')[-1]
    hh, mm, ss = timestamp.split(':')
    return(3600 * int(hh) + 60 * int(mm) + int(ss))

def convert_timestamps(timestamps, start_time):
    raw_seconds = map(timestamp_to_seconds, timestamps)
    return([s - start_time for s in list(raw_seconds)])

def apply_savgol_filter(raw_data):
    raw_data = raw_data.dropna().loc[0:]
    converted_data = savgol_filter(raw_data, 51, 5)
    filtered_data = pd.Series(converted_data, index=raw_data.index.values)
    return(filtered_data.loc[0:])

def prep_data_for_plot(scale_factor, offset, data_type)
    y2_label = 'None'

    if data_type == 'Temperature':
        filtered_data = exp_data[channel].rolling(window=5, center=True).mean()
        plot_data = filtered_data.dropna().loc[0:]
        y1_label = 'Temperature ($^\circ$C)'
        y2_label = 'Temperature ($^\circ$F)'

    elif data_type == 'Velocity':
        zeroed_data = exp_data.loc[:, channel] - exp_data.loc[:-1, channel].mean()
        converted_data = np.sign(zeroed_data) * 0.0698 * ((exp_data[channel[0] + 'TC' + channel[3:]] + 273.15) * (scale_factor * abs(zeroed_data)))**0.5
        plot_data = apply_savgol_filter(converted_data)
        y1_label = 'Velocity (m/s)'
        y2_label = 'Velocity (mph)'

    elif data_type == 'Differential Pressure':
        converted_data = scale_factor * exp_data[channel] + offset
        zeroed_data = converted_data - converted_data.loc[:-1].mean()
        plot_data = apply_savgol_filter(zeroed_data)
        y1_label = 'Pressure (Pa)'

    elif data_type == 'Heat Flux' or data_type == 'Radiant Heat Flux':
        zeroed_data = exp_data[channel] - exp_data[channel].loc[:-1].mean()
        converted_data = zeroed_data * scale_factor
        plot_data = apply_savgol_filter(converted_data)
        y1_label = 'Heat Flux (kW/m$^2$)'

    elif any([data_type == string for string in ['Oxygen', 'Carbon Monoxide', 'Carbon Dioxide']]):
        if data_type == 'Oxygen':
            # Use next line for O2 ranging from 0-5 V (scale_factor = 5 in channel list)
            # zeroed_data = exp_data.loc[:, channel] - (exp_data.loc[:lag_time - 1, channel].mean() - 5. * (20.98 / 25))
            # Use next line for O2 ranging from 1-5 V (scale_factor = 6.25 in channel list)
            zeroed_data = exp_data.loc[:, channel] - (exp_data.loc[:lag_time - 1, channel].mean() - 4. * (20.98 / 25) - 1) - 1
        else:
            zeroed_data = exp_data.loc[:, channel] - exp_data.loc[:lag_time - 1, channel].mean()
        converted_data = scale_factor * zeroed_data + offset
        filtered_data = converted_data.rolling(window=5, center=True).mean()
        plot_data = filtered_data.dropna().loc[0:]
        y1_label = 'Concentration (% vol)'

    else:
        print(f'Data type for {channel} not found!')
        exit()

    return(plot_data, y1_label, y2_label)

def format_and_save_plot(y_lims, x_lims, y2_label, file_loc):
    # Set tick parameters
    ax1.tick_params(labelsize=tick_size, length=0, width=0)

    # Scale axes limits & labels
    ax1.set_ylim(bottom=y_lims[0], top=y_lims[1])
    ax1.set_xlim(left=x_lims[0] - x_lims[1] / 400, right=x_lims[1])
    ax1.set_xlabel('Time (s)', fontsize=label_size)

    # Secondary y-axis parameters
    if y2_label != 'None':
        ax2 = ax1.twinx()
        ax2.tick_params(labelsize=tick_size, length=0, width=0)
        ax2.set_ylabel(secondary_axis_label, fontsize=label_size)
        if y2_label == 'Temperature ($^\circ$F)':
            ax2.set_ylim([y_lims[0] * 1.8 + 32., y_lims[1] * 1.8 + 32.])
        else:
            ax2.set_ylim([secondary_axis_scale * y_lims[0], secondary_axis_scale * y_lims[1]])

        ax2.yaxis.grid(b=None)

    # Add labels for timing information (if available)
    ax3 = ax1.twiny()
    ax3.set_xlim(left=x_lims[0] - x_lims[1] / 400, right=x_lims[1])
    ax3.set_xticks(exp_data[pd.notna(exp_data['Event'])].index.values)
    ax3.tick_params(axis='x', width=1, labelrotation=font_rotation, labelsize=event_font)
    ax3.set_xticklabels(exp_data[pd.notna(exp_data['Event'])]['Event'].values, fontsize=event_font, ha='left')
    ax3.xaxis.grid(b=None)

    # Add legend, clean up whitespace padding, save chart as pdf, & close fig
    handles1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(handles1, labels1, loc='best', fontsize=legend_font, handlelength=3, frameon=True, framealpha=0.75)
    fig.tight_layout()
    plt.savefig(file_loc)
    plt.close()

# ----------------- #
# Main Body of Code #
# ----------------- #
# Determine which test data to plot
data_file_ls = []
for f in data_dir.iterdir():
    if f.suffix == '.csv':
        if plot_all:
            data_file_ls.append(f.name)
        else:
            if not (plot_dir / f.name[:-4]).exists():
                data_file_ls.append(f.name)

# Loop through test data files & create plots
for f in data_file_ls:
    # Read in data for experiment & replace blank fields with nan
    exp_data = pd.read_csv(data_dir / f, skiprows=6)
    exp_data.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    # Get test name from file
    Test_Name = f[:-4]
    print (f'--- Loaded data file for {Test_Name} ---')

    # Create index column of time relative to ignition in exp_data
    exp_data.rename(columns={'Time':'Timestamp'}, inplace=True)
    ignition_idx_ls = exp_data.index[exp_data['Event'] == 'Ignition'].tolist()
    start_timestamp = exp_data.loc[ignition_idx_ls[-1], 'Timestamp'].split(' ')[-1]
    hh,mm,ss = start_timestamp.split(':')
    start_time = 3600 * int(hh) + 60 * int(mm) + int(ss)
    exp_data['Time'] = convert_timestamps(exp_data['Timestamp'], start_time)

    exp_data = exp_data.set_index('Time')

    # Define name of dir for experiment's plots & create if needed
    save_dir = plot_dir / Test_Name
    save_dir.mkdir(parents=True, exist_ok=True)

    # Loop through channel groups & generate data plots for each
    for group in channel_groups.groups:
        print (f"  Plotting {group.replace('_',' ')}")

        # Create figure for data plot(s)
        fig, ax1 = plt.subplots(figsize=(fig_width, fig_height))
        plot_markers = cycle(line_markers)
        x_max, y_min, y_max = 0, 0, 0

        if group.endswith('_Gas'):
            lag_time = test_info.loc[Test_Name, group]

        # Plot data from each channel associated with group
        for channel in channel_groups.get_group(group).index.values:
            # Get scale factor, offset, & data type based on channel list
            scale_factor = channel_list.loc[channel,'Scale']
            offset = channel_list.loc[channel,'Offset']
            data_type = channel_list.loc[channel,'Type']

            # Zero/filter data & set plot parameters based on data type
            plot_data, y1_label, y2_label = prep_data_for_plot(scale_factor, offset, data_type)

            # Plot channel data
            ax1.plot([i for i in plot_data.index], [y for y in plot_data.values], lw=line_width,
                marker=next(plot_markers), markevery=60, mew=3, mec='none', ms=7, 
                label=channel_list.loc[channel, 'Label'])

            # Check if x_max, y_min, y_max need updating
            if len(plot_data) > x_max:
                x_max = len(plot_data)
            if min(plot_data) - abs(min(plot_data) * .1) < y_min:
                y_min = min(plot_data) - abs(min(plot_data) * .1)
            if max(plot_data) * 1.1 > y_max:
                y_max = max(plot_data) * 1.1

        # Add vertical lines for event labels; label to y axis
        [ax1.axvline(_x, color='0.25', lw=1) for _x in exp_data[pd.notna(exp_data['Event'])].index.values]
        ax1.set_ylabel(y1_label, fontsize=label_size)

        format_and_save_plot([y_min, y_max], [0, x_max], y2_label, save_dir / f'{group}.pdf')

    print()