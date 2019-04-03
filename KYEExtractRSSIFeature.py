# encoding: utf-8
import sys
#计算蓝牙个数和位置个数
beacon_set = set()
id_set = set()
for line in sys.stdin:
  item = line.strip().split(',')
  id_set.add(int(eval(item[1])))
  info = item[2]
  for sub_info in info.strip().split('#'):
    try:
      beacon_set.add(sub_info.strip().split('%')[0].strip('"'))
    except:
      continue
beacon_set.remove('')

# print('{}, {}'.format(len(beacon_set), len(id_set)))
# print('{}\n{}'.format(beacon_set, id_set))
# for i in range(132):
#   if i not in id_set:
#     print(i)
# print('*'*80)
# for k, v in enumerate(beacon_set):
#   print(k, v)
EFFECTIVE_BLUETOOTH_COUNT = 5
#将结果转换成格式数据，保存到csv
beacon_dict = {value: key for key, value in enumerate(beacon_set)}
id_dict = {value: key for key, value in enumerate(id_set)}
import pickle
param_data = {}
param_data['beacon_count'] = len(beacon_set)
param_data['id_count'] = len(id_set)
param_data['beacons'] = beacon_dict
param_data['ids'] = id_dict
with open('./KYEIndoorLocation/params.pickle', 'wb') as f:
  pickle.dump(param_data, f, pickle.HIGHEST_PROTOCOL)
beacon_count = len(beacon_dict)
with open(sys.argv[1], 'r') as f:
  for line in f.readlines():
# for line in sys.stdin:
    each_sample = [0 for i in range(0, beacon_count + 1)]
    item = line.strip().split(',')
    each_sample[-1] = id_dict[int(eval(item[1]))]
    info = item[2]
    count = 0
    for sub_info in info.strip().split('#'):
      try:
        beacon_key = sub_info.strip().split('%')[0].strip('"')
        beacon_value = int(sub_info.strip().split('%')[1].strip('"'))
        each_sample[beacon_dict[beacon_key]] = beacon_value
        count = count + 1
        if count % EFFECTIVE_BLUETOOTH_COUNT == 0:
          print(','.join(str(x) for x in each_sample))
          for i in range(beacon_count):
            each_sample[i] = 0
          count = 0
      except Exception as e:
        if sub_info:
          # print('except line:{}'.format(sub_info))
          # print(e.value)
          continue
# print(id_dict)

