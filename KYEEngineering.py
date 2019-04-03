# encoding: utf-8
#模型应用示范
import lightgbm as lgb
import pickle
clf = lgb.Booster(model_file='./KYEIndoorLocation/model.txt')
with open('./KYEIndoorLocation/params.pickle', 'rb') as f:
  params = pickle.load(f)
feature_number = params['beacon_count']
class_number = params['id_count']
beacon2index = params['beacons']
id2index = params['ids']
# print(id2index)
index2id = {index: id for id, index in id2index.items()}
# target_input_json = {
# 	[{
# 		"RSS": 65,
# 		"MAC": "40:06:A0:5F:08:3C"
# 	}, {
# 		"RSS": 73,
# 		"MAC": "40:06:A0:5F:22:42"
# 	}, {
# 		"RSS": 80,
# 		"MAC": "40:06:A0:60:3C:AE"
# 	}, {
# 		"RSS": 85,
# 		"MAC": "40:06:A0:5F:19:BE"
# 	}, {
# 		"RSS": 88,
# 		"MAC": "40:06:A0:60:27:E5"
# 	}, {
# 		"RSS": 65,
# 		"MAC": "40:06:A0:5F:08:3C"
# 	}, {
# 		"RSS": 73,
# 		"MAC": "40:06:A0:5F:22:42"
# 	}, {
# 		"RSS": 78,
# 		"MAC": "40:06:A0:60:20:8F"
#   }]
# }
# print(target_input_json)
X = [[0,0,0,0,72,0,0,0,0,0,93,0,0,0,0,0,0,0,0,92,0,69,0,0,0,0,0,0,0,72,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,93,0,0,93,0,0,0,0,91,0,0,0,0,0,0,0,0,0,89,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,90,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,88,0,85,90,0,0,0,0,84,0,0,0,0,83,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,77,0,0,0,79,0,75,76,0,0,0,0,0,78,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,87,0,86,0,0,0,0,0,0,0,0,0,0,0,0,80,0,0,83,0,0,0,0,0,84,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

def predict_location_id(X_test):
  y_pred = clf.predict(X_test, num_iteration=clf.best_iteration)
  return y_pred
import numpy as np
y_pred = predict_location_id(X)
print([np.argmax(item) for item in y_pred])
print([index2id[list(x).index(max(x))] for x in y_pred])