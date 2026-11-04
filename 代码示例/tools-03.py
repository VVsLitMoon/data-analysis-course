from _lecture_data import *

from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
y_true = [0,0,0,1,1,1]
y_pred = [0,0,1,0,1,1]
print(confusion_matrix(y_true,y_pred))
print("精确率/召回/F1：",precision_score(y_true,y_pred),recall_score(y_true,y_pred),f1_score(y_true,y_pred))
