# create_channel_config_file_pxi.py
# by: J. Willi & R. Zevotek 
# ******************************* Run Notes ******************************* #
# - Uses channel list to create the .chcfg file that's to be used with the  #
#       PXI DAQ                                                             #
#       + Be sure channel list is properly formatted & ends with            #
#           'channel_list.csv'                                              #
#                                                                           #
# - Define variables listed under "Define Necessary Inputs" based on DAQ    #
#       configuration                                                       #
#       + Setting config_NI_Max = True & properly defining variables that   #
#           follow will produce .txt config file to import into NI Max to   #
#           properly set up channels (instead of having to manually define  #
#           them)                                                           #
#           > NOTE: current defs were obtained from FSI DAQ hardware; NEED  #
#               TO UPDATE FOR OURS                                          #
#       + If you are unsure about certain variables required for NI Max     #
#           config file, export a .txt config file from NI Max for DAQ      #
#           being used                                                      #
#           > serial numbers, product numbers, & accessory numbers for the  #
#               hardware will be listed in the exported file among other    #
#               things                                                      #
#                                                                           #
# - The NI Max config file is generated with the following assumptions:     #
#       + All temperature channels...                                       #
#           > are of type K                                                 #
#           > use the built-in temperature for its cold junction ref        #
#           > display units in deg C                                        #
#           > are configured to measure T within range of -200 to 1372 C    #
#       + All voltage channels...                                           #
#           > are analog inputs                                             #
#           > measure RSE voltage                                           #
#           > are configured within NI Max to measure V within range of     #
#               -10 to 10 V                                                 #
#                                                                           #
# - If we ever decide to incorporate a counting module, look to the version #
#       of this script in the IFSI_PPE_Interface repo for guidance          #
# ************************************************************************* #

# -------------- #
# Import Modules #
# -------------- #
import os
import pandas as pd
from itertools import cycle

# ----------------------- #
# Define Necessary Inputs #
# ----------------------- #
# Set location of dir containing channel lists
channel_list_dir = '../1_Info/Data_Channels/'

# Set name of system
sys_ID = 'PXI1'

# Dict with panel numbers as keys corresponding to array with [panel num, channel type]
panel_defs = {1:[2,'Temperature'],
              2:[3,'Temperature'],
              3:[4,'Temperature'],
              4:[5,'Temperature'],
              5:[6,'Temperature'],
              6:[7,'Temperature'],
              7:[8,'Voltage'],
              8:[8,'Voltage'],
              9:[8,'Voltage'],
              10:[8,'Voltage']}

# Dict to define channel numbers for panels in system
panel_chans =  {1:[0,32],
                2:[0,32],
                3:[0,32],
                4:[0,32],
                5:[0,32],
                6:[0,32],
                7:[0,32],
                8:[32,64],
                9:[64,96],
                10:[96,128]}

# Set flag to true if .txt config file should be generated to import into NI Max
config_NI_Max = False

# Define variables for NI Max config file based on DAQ being utilized
DAQmx_version = [19, 5]  # first input is major version, second is minor version of DAQmx

# dict contains device info for hardware in each slot; each key is the DAQmxDevice name corresponding to an 
#   array structured as [BusType, Serial #, Product #, Chassis #, Slot #] for given device
DAQmxDevice_info = {f'{sys_ID}Slot2': ['PXIe', '0x1E38119', '0x74B2C4C4', 'PXIe-4353', '1', '2'],
                    f'{sys_ID}Slot3': ['PXIe', '0x1E38110', '0x74B2C4C4', 'PXIe-4353', '1', '3'],
                    f'{sys_ID}Slot4': ['PXIe', '0x1E27AE9', '0x77A6C4C4', 'PXIe-6355', '1', '4'],
                    f'{sys_ID}Slot5': ['PXI', '0x1E56289', '0x1E40', 'PXI-6624', '1', '5']}

# dict contains keys corresponding to physical channels that point to serial #s of DAQmx accessories
DAQmxAccessory_info = {f'TC-4353/{sys_ID}Slot2/0': '31755019',
                       f'TC-4353/{sys_ID}Slot3/0': '31619400'}

# ----------------------- #
# Define Custom Functions #
# ----------------------- #
# Get headers for NI Max config file based on channel type
def get_DAQmxChannel_headers(ch_type):
    if ch_type == 'Temperature':
        return(['[DAQmxChannel]', 'AI.AutoZeroMode', 'AI.Max', 'AI.MeasType', 'AI.Min', 
                'AI.OpenThrmcplDetectEnable', 'AI.Temp.Units', 'AI.Thrmcpl.CJCChan', 'AI.Thrmcpl.CJCSrc', 
                'AI.Thrmcpl.CJCVal', 'AI.Thrmcpl.Type', 'ChanType', 'Descr', 'PhysicalChanName', ''])

    elif ch_type == 'Voltage':
        return(['[DAQmxChannel]', 'AI.Max', 'AI.MeasType', 'AI.Min', 'AI.TermCfg', 
                'AI.Voltage.Units', 'ChanType', 'Descr', 'PhysicalChanName', ''])

# Get DAQmxChannel row inputs for NI Max config file given channel label, physical name, & type
def get_DAQmxChannel_row(ch_label, phys_name, ch_type):
    if ch_type == 'Temperature':
        return([ch_label, 'Every Sample', '1372', f'{ch_type}:Thermocouple', '-200', '1', 
                      'Deg C', '', 'Built-In', '25', 'K', 'Analog Input', '', phys_name, ''])

    elif ch_type == 'Voltage':
        return([ch_label, '10', ch_type, '-10', 'RSE', 'Volts', 'Analog Input', '', phys_name, ''])

# function to get alarm ranges and units for different channel types.
def get_channel_vars(ch_type):
    if ch_type == 'Temperature':
        function = '"Thermocouple (K)"'
        units = '"C"'
        low_alarm_str = '"-17.777800"'
        high_alarm_str = '"1230.00000"'
        min_value_str = '"-245.729755"'
        max_value_str = '"1232.065825"'
    elif any([ch_type == string for string in ['Heat_Flux']]):
        function = '"Voltage"'
        units = '"V"'
        low_alarm_str = '"-0.099000"'
        high_alarm_str = '"0.099000"'
        min_value_str = '"-0.100000"'
        max_value_str = '"0.100000"'
    elif any([ch_type == 'Wind_Direction', ch_type == 'Wind_Velo']):
        function = '"Voltage"'
        units = '"V"'
        low_alarm_str = '"-0.099000"'
        high_alarm_str = '"9.999000"'
        min_value_str = '"-10.00000"'
        max_value_str = '"10.00000"'
    elif any([ch_type == string for string in ['Oxygen', 'Carbon_Monoxide', 'Carbon_Dioxide']]):
        function = '"Voltage"'
        units = '"V"'
        low_alarm_str = '"-0.099000"'
        high_alarm_str = '"4.999000"'
        min_value_str = '"-10.00000"'
        max_value_str = '"10.00000"'
    else:
        function = '"Voltage"'
        units = '"V"'
        low_alarm_str = '"-9.9990000"'
        high_alarm_str = '"9.999000"'
        min_value_str = '"-10.000000"'
        max_value_str = '"10.000000"'

    return(function, units, low_alarm_str, high_alarm_str, min_value_str, max_value_str)

def write_channel(array_num, bool_value, channel_type, pan_num, ch_num, name, phys_chan):
    # Define variables that will be used in lines of channel definition
    function, units, low_alarm, high_alarm, min_value, max_value = get_channel_vars(
        channel_type)
    line_start = 'Valid Channel Arrray '+str(array_num)+'.'

    file.write(line_start+'Use? = "'+bool_value+'"'+'\n')
    file.write(line_start+'Channel Name = "'+name+'"'+'\n')
    file.write(line_start+'Channel Function = '+function+'\n')
    file.write(line_start+'Units = '+units+'\n')

    phys_channel_str = '"'+phys_chan+'"'
    file.write(line_start+'Physical Channel = '+phys_channel_str+'\n')

    formatted_name = f'Pan{pan_num:02d}Ch{ch_num:02d}'
    global_ch_str = r'"\00\00\00	'+formatted_name+'"'
    file.write(line_start+'DAQmx Global Channel = '+global_ch_str+'\n')

    if any([channel_type == string for string in ['Oxygen', 'Carbon_Monoxide', 'Carbon_Dioxide']]):
        file.write(line_start + 'Alarm Info.Alarm = "High Only"'+'\n')
    else:
        file.write(line_start+'Alarm Info.Alarm = "High and Low"'+'\n')

    file.write(line_start+'Alarm Info.Low Limit = '+low_alarm+'\n')
    file.write(line_start+'Alarm Info.High Limit = '+high_alarm+'\n')
    file.write(line_start+'Min = '+min_value+'\n')
    file.write(line_start+'Max = '+max_value+'\n')

# Calculate total number of channels
num_of_channels = sum([len(range(x[0], x[1])) for x in panel_chans.values()])

# Create config file for NI Max if flag = True
if config_NI_Max:
    print(f'Generating NI Max config data file for {sys_ID}...')
    with open(f'{channel_list_dir}{sys_ID}_configData.txt', 'w') as f:
        # Write DAQmx version lines
        f.write('\t'.join(['[DAQmx]', 'MajorVersion', 'MinorVersion', '']) + '\n')
        f.write('\t'.join(['', str(DAQmx_version[0]), str(DAQmx_version[1]), '']) + '\n')

        # store data type of last panel to determine if new headers need to be written to file
        last_ch_type = 'None'

        # Write DAQmxChannel lines for channels on each panel
        for pan_num in panel_defs.keys():
            slot_num, ch_type = panel_defs[pan_num][0], panel_defs[pan_num][1]
            if ch_type != last_ch_type:
                f.write('\n' + '\t'.join(get_DAQmxChannel_headers(ch_type)) + '\n')

            # Add row for each channel on given panel
            start_range = panel_chans[pan_num][0]
            end_range = panel_chans[pan_num][1]
            for devc_ch_num in range(start_range, end_range):
                if ch_type == 'Voltage':
                    ch_label = f'Pan{int(pan_num):02d}Ch{devc_ch_num - start_range:02d}'
                else:
                    ch_label = f'Pan{int(pan_num):02d}Ch{devc_ch_num:02d}'
                phys_name = f'{sys_ID}Slot{slot_num}/ai{devc_ch_num}'
                f.write('\t'.join(get_DAQmxChannel_row(ch_label, phys_name, ch_type)) + '\n')

            last_ch_type = ch_type

        # Add DAQmxDevice headers & rows using info provided in DAQmxDevice_info
        f.write('\n' + '\t'.join(['[DAQmxDevice]', 'BusType', 'DevSerialNum', 'ProductNum', 'ProductType', 'PXI.ChassisNum', 'PXI.SlotNum', '']) + '\n')
        for device in DAQmxDevice_info.keys():
            f.write('\t'.join([device] + DAQmxDevice_info[device] + ['']) + '\n')

        # Add DAQmxAccessory rows using info provided in DAQmxAccessory_info
        f.write('\n' + '\t'.join(['[DAQmxAccessory]', 'Accessory.SerialNum', '']) + '\n')
        for accessory in DAQmxAccessory_info.keys():
            f.write('\t'.join([accessory, DAQmxAccessory_info[accessory], '']) + '\n')
        f.write('\n')

# Generate config file for each channel list csv within dir
for f in os.listdir(channel_list_dir):
    # Skip if file is not channel list csv file
    if not (f.lower().endswith('channel_list.csv')):
        continue
    else:
        print(f'Creating config file from {f}...')

    # Read in channel list csv as df
    channel_list = pd.read_csv(channel_list_dir+f, index_col='Channel_Name')

    # Group list by mod IDs
    active_panels = channel_list.groupby('Panel')

    # Create dict with Slot IDs as keys that ref list of tuples corresponding to active inputs for given module in the form (channel_input,channel_name)
    active_inputs = {}

    for panID in active_panels.groups:
        # Create empty list to populate with active channel inputs for given panID
        inputs = [channel_list.loc[idx,'Channel'] for idx in active_panels.groups[panID]]

        # Add series with index of input IDs referencing channel names to dict
        active_inputs[panID] = pd.Series(active_panels.groups[panID], index=inputs)

    # Create config file & write first 2 lines
    file = open(f'{channel_list_dir}{f[:-4]}.chcfg','w')
    file.write('[Saved Channels IN]' + '\n')
    file.write(f'Valid Channel Arrray.<size(s)> = "{num_of_channels}"' + '\n')

    channel_array_ID = 0
    for pan_ID in panel_defs.keys():
        default_input_type = panel_defs[pan_ID][1]
        start_range = panel_chans[pan_ID][0]
        end_range = panel_chans[pan_ID][1]
        if int(pan_ID) not in active_inputs.keys():
            # Write all inputs as false
            for ch_ID in range(0, 32):
                # Set channel label & physical name based on ch_ID & first num in panel_chans[pan_ID] array
                ch_num = ch_ID
                phys_chan_ID = f'{sys_ID}Slot{panel_defs[pan_ID][0]}/ai{ch_ID + start_range}'
                ch_label = f'Pan{int(pan_ID):02d}Ch{ch_num:02d}'

                write_channel(channel_array_ID, 'FALSE', default_input_type, pan_ID, ch_num, ch_label, phys_chan_ID)
                channel_array_ID += 1
        else:
            # Set list of active inputs & set channels accordingly
            active_channels = active_inputs[int(pan_ID)]
            for ch_ID in range(0, end_range - start_range):
                # Set channel label & physical name based on ch_ID & first num in panel_chans[pan_ID] array
                ch_num = ch_ID
                phys_chan_ID = f'{sys_ID}Slot{panel_defs[pan_ID][0]}/ai{ch_ID + start_range}'
                ch_label = f'Pan{int(pan_ID):02d}Ch{ch_num:02d}'

                if ch_num in active_channels:
                    bool_value = 'TRUE'
                    ch_label = active_channels[ch_num]
                    input_type = channel_list.loc[ch_label,'Type']
                    write_channel(channel_array_ID, 'TRUE', input_type, pan_ID, ch_num, ch_label, phys_chan_ID)
                else:
                    write_channel(channel_array_ID, 'FALSE', default_input_type, pan_ID, ch_num, ch_label, phys_chan_ID)

                channel_array_ID += 1

    file.close()