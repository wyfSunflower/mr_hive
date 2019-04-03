# encoding: utf-8
#从样本训练模型，保存结果
import lightgbm as lgb
TRAIN_DATA = './KYEIndoorLocation/train_sample_set'
TEST_DATA = './KYEIndoorLocation/test_sample_set'
# import json
# with open('./KYEIndoorLocation/params.json', 'r') as f:
#   param_data = json.load(f)
import pickle
with open('./KYEIndoorLocation/params.pickle', 'rb') as f:
  param_data = pickle.load(f)
FEATURE_DIMENSION = len(param_data['beacons'])
CLASS_NUMBER = len(param_data['ids'])
def load_data(file_path):
  sample_count=sum(1 for line in open(file_path))
  feature_set = [[0 for feature_index in range(FEATURE_DIMENSION)] for sample in range(sample_count)]
  label_set = [0 for sample in range(sample_count)]
  with open(file_path, 'r') as f:
    index = 0
    for line in f.readlines():
      items = line.strip().split(',')
      try:
        label_set[index] = int(items[-1])
        del items[-1]
        for k, v in enumerate(items):
          feature_set[index][k] = float(v)
        index = index+1
      except Exception as e:
        # print(e.value)
        continue
  return feature_set, label_set
X_train, y_train = load_data(TRAIN_DATA)
X_test, y_test = load_data(TEST_DATA)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_norm = sc.fit_transform(X_train)
X_test_norm = sc.transform(X_test)
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score,roc_auc_score
def outputPrecisionRecall(clf, y_test, y_pred):
  print("classifier:%s \n\naccuracy: %f" % (clf, accuracy_score(y_true=y_test, y_pred=y_pred)))
  print("{} \n\nprecision: {}".format(clf, precision_score(y_true=y_test, y_pred=y_pred, average=None)))
  print("{} \n\nrecall: {}" .format(clf, recall_score(y_true=y_test, y_pred=y_pred, average=None)))
  print("{} \n\nf1: {}" .format(clf, f1_score(y_true=y_test, y_pred=y_pred, average=None)))
train_data=lgb.Dataset(X_train_norm, label=y_train)
validation_data=lgb.Dataset(X_test_norm, label=y_test)
params={'learning_rate': 0.086, 'lambda_l1': 0.05, 'lambda_l2': 0.1, 'max_depth': 50, 'objective': 'multiclass',
        'num_class': CLASS_NUMBER, 'verbose': -1}
clf=lgb.train(params, train_data, valid_sets=[validation_data])
y_pred=clf.predict(X_test_norm)
y_pred=[list(x).index(max(x)) for x in y_pred]
outputPrecisionRecall(clf=clf, y_test=y_test, y_pred=y_pred)
print('auc {}'.format(roc_auc_score(y_test, y_pred, average=None)))
clf.save_model('./KYEIndoorLocation/model.txt')
# try:
#   import cPickle as pickle
# except BaseException:
#   import pickle
# with open('model.pkl', 'wb') as fout:
#   pickle.dump(clf, fout)
# import json
# model_json = clf.dump_model()
# with open('model.json', 'w+') as f:
#   json.dump(model_json, f, indent=4)