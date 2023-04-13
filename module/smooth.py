from  scipy.signal import savgol_filter as sf 
# import matplotlib.pyplot as plt

def smooth(merged_data, config):
    for mobile_name in merged_data:
        df = merged_data[mobile_name]
        column_list = getColumnList(df)
        for column_name in column_list:
            df = savgolFilter(column_name, df, config)
        merged_data[mobile_name] = df
    return merged_data

def savgolFilter(column_name, df, config):
    filtered_column = sf(df. loc[:, column_name], window_length = config['savgol']['window_length'], polyorder = config['savgol']['polyorder'])
    # drawChartComparison(column_name, df, filtered_column)
    df[column_name] = filtered_column
    return df

def getColumnList(df):
    column_list = df.columns.values.tolist()
    column_list.remove('time')
    return column_list

# def drawChartComparison(column_name, df, filtered_column):
#     figure, axis = plt.subplots(1, 2)
#     axis[0].plot(df. loc[:, column_name])
#     axis[0].set_title(column_name)

#     axis[1].plot(filtered_column)
#     axis[1].set_title(column_name + "_savgol")  
#     plt.show()