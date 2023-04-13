import numpy as np
from numpy.linalg import norm

def model(dev1_data, dev2_data, config):
    time_shift = config['model']['time_shift']
    start_index, end_index= getRound(dev1_data, config)

    result = []
    for round in range(start_index, end_index, time_shift):
        ans_list = getCS(dev1_data, dev2_data, config, round)
        relation = getRelation(ans_list, config)
        result.append(relation)
    return result


def getRelation(ans_list, config):
    average = sum(ans_list) / len(ans_list)
    middle = ans_list[config['model']['show_shift_time']]
    ans_max = max(ans_list)
    # print(f"Average = {average}, Difference = {ans_max - middle}")
    if average < config['model']['independent_threshold']:
        return 2
    elif ans_max - middle > config['model']['companion_threshold']:
        return 1
    else:
        return 0


def getRound(dev1_data, config):
    leader_follower_max_time = config['model']['leader_follower_max_time']
    show_shift_time = config['model']['show_shift_time']

    index_num = len(dev1_data.index)

    start_time = leader_follower_max_time
    end_time = index_num - leader_follower_max_time - show_shift_time
    return start_time, end_time


def getCS(dev1_data, dev2_data, config, round):
    leader_follower_max_time = config['model']['leader_follower_max_time']
    show_shift_time = config['model']['show_shift_time']
    ans_list1 = []
    ans_list2 = []
    for shift in  range(show_shift_time+1):
        data1 = devideData(dev1_data, round, 0, leader_follower_max_time)
        data2 = devideData(dev2_data, round, shift, leader_follower_max_time)
        cs = 0
        for i in range(len(data1.index)):
            cs = cs + innerProduct(data1.iloc[i], data2.iloc[i])
        cs = cs / (leader_follower_max_time * 2)
        ans_list1.append(cs)
    for shift in  range(show_shift_time+1):
        data1 = devideData(dev1_data, round, shift, leader_follower_max_time)
        data2 = devideData(dev2_data, round, 0, leader_follower_max_time)
        cs = 0
        for i in range(len(data1.index)):
            cs = cs + innerProduct(data1.iloc[i], data2.iloc[i])
        cs = cs / (leader_follower_max_time * 2)
        ans_list2.append(cs)

    ans_list1.pop(0)
    ans_list1.reverse()
    ans_list = ans_list1 + ans_list2
    return ans_list


def devideData(dev_data, round, shift, max_time):
    middle = round + shift
    return dev_data[middle - max_time : middle + max_time + 1]


def innerProduct(data1, data2):
    data1 = data1.to_numpy()
    data2 = data2.to_numpy()
    # print(data1, data2)
    if (norm(data1)*norm(data2)) != 0:
        ans = np.dot(data1, data2) / (norm(data1)*norm(data2))
    else:
        ans = 0
    return ans