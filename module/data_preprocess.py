import datetime
# import numpy as np
import pandas as pd
from module.log import printLog
from module.normalizaion import normalization
from module.smooth import smooth


def dataPreprocess(config):
    wireless_data = getWirelessData(config)
    wireless_data = normalization(wireless_data)
    wireless_data = smooth(wireless_data, config)
    saveFile(wireless_data, config)
    return


def saveFile(wireless_data, config):
    for mobile_name in wireless_data:
        df = wireless_data[mobile_name]
        df.to_csv('data/' + config['date'] + '/' + mobile_name + '.csv', sep = ',', index = False)
    return


def getWirelessData(config):
    file_list = []
    for file_name in config['sniffer_list']:
        file_list.append(getSnifferFile(file_name, config))
    df_dict = {}
    for mobile_name in config['mobile_list']:
        printLog("Start preprocessing " + mobile_name + ".")
        df = createDF1(config = config)
        for experiment_nummber in range(len(config['end_time'])):
            df1 = createDF1(config = config)
            df1 = addRow(config, df1 , config['mobile_list'][mobile_name], file_list, experiment_nummber)
            df = pd.concat([df, df1])
        df_dict[mobile_name] = df
    return df_dict

def getSnifferFile(wireless_file_name, config):
    df = pd.read_csv('rawdata/' + str(config['date']) + '/' + wireless_file_name + '.csv', parse_dates=[0])
    df.columns = ['time','mac','type','rssi','uuid']
    df = df.drop('mac', axis=1)
    df = df.drop('type', axis=1)
    df = df.astype({'time':'string'})
    df = df.astype({'uuid':'string'})
    for i in range(len(df.index)):
        df._set_value(i, 'time', str(df['time'][i])[:-7])
        df._set_value(i, 'time', str(df['time'][i])[11:])
    return df

def createDF1(config):
    column = ['time']
    column.extend(config['sniffer_list'])
    df = pd.DataFrame(columns = column)
    return df

def addRow(config, df, uuid, file_list, experiment_number):
    for i in range(getRowNum(config, experiment_number)):
        df.loc[len(df.index)] = getRowData(i, config, uuid, file_list, experiment_number)
    return df

def getRowNum(config, experiment_number):
    start_time = string2datetime(config['start_time'][experiment_number]).time()
    end_time = string2datetime(config['end_time'][experiment_number]).time()
    duration = datetime.datetime.combine(datetime.date.min, end_time) - datetime.datetime.combine(datetime.date.min, start_time)
    return duration.seconds


def getRowData(second, config, uuid, file_list, experiment_number):
    ans = []
    time = string2datetime(config['start_time'][experiment_number]) + datetime.timedelta(0, second)
    ans.append(str(time)[11:])
    for file in range(len(config['sniffer_list'])):
        ans.append(getRSSI(time, file_list[file], uuid))
    return ans


def getRSSI(time, raw_data, uuid):
    raw_data = raw_data.loc[raw_data['time'] == str(time)[11:]]
    raw_data = raw_data.loc[raw_data['uuid'] == uuid]
    sum = raw_data['rssi'].sum()
    frequency = raw_data.shape[0]
    if sum == 0:
        return 0
    else:
        return sum / frequency
    

def string2datetime(time):
    date = '2023/01/06 '
    format = '%Y/%m/%d %H:%M:%S'
    output = datetime.datetime.strptime(date + time, format)
    return output
