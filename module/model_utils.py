import pandas as pd
import numpy as np
import itertools
from module.log import printLog
from module.model import model
from itertools import combinations
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

def runModel(config):
    target_name = ["Companion", "Leader-Follower", "Independent"]
    mobile_combination = list(combinations(config['mobile_list'], 2))
    y_pred = []
    y_true = []
    for combination in mobile_combination:
        printLog("Starting calculating " + str(combination))
        dev1_data = pd.read_csv('data/' + str(config['date']) + '/'+ combination[0] + '.csv')
        dev2_data = pd.read_csv('data/' + str(config['date']) + '/'+ combination[1] + '.csv')
        dev1_data = dataPreProcess(dev1_data, config)
        dev2_data = dataPreProcess(dev2_data, config)
        pred = model(dev1_data, dev2_data, config)
        true = checkResult(len(pred), combination, config)
        y_pred = y_pred + pred
        y_true = y_true + true
    print(classification_report(y_true, y_pred, target_names = target_name, digits = 3))
    printConfusionMatrix(y_true, y_pred, target_name)
    return


def dataPreProcess(data, config):
    data = data.drop('time', axis=1)
    sniffer_list = config['sniffer_list']
    for column_name in data.columns:
        if column_name not in sniffer_list:
            data = data.drop(column_name, axis = 1)
    data = data.reset_index()
    data = data.drop('index', axis=1)
    return data

def printConfusionMatrix(y_true, y_pred, target_name):
    plt.figure()
    cnf_matrix = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cnf_matrix, classes=target_name,normalize=True,title="confusion matrix")
    plt.show()
    return


def checkResult(list_len, combination, config):
    ans = 0
    for relation in config['relation']:
        if combination[0] in relation and combination[1] in relation:
            ans = relation[0]
    return  [ans] * list_len


def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()