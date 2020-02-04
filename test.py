import time
from datetime import datetime
timestr = '2020-01-20 16:36:14.183'

# timestr = '2020-01-19 17:22:37.101'
datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
obj_stamp1 = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
print(obj_stamp1)



input = '10.092'
obj_stamp2 = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0 + float(input)* 1000.0)
print(obj_stamp2)


# 1579425712141
# 1579469713101


# 1579425757101
# 1579425757101




def readTXT(file_path): # this file can be very big!!!
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines

BIG_LIST = readTXT('/home/yuehu/PycharmProjects/Elevator_data_analyse/example_data/Air_log2.txt')

def findMatchedTS(begin_ts, end_ts):
    # collect all Inf_Event between 2 timestamps
    res = []
    for line in BIG_LIST:
        line = line.strip('\n')
        if not line:
            continue

        this_ts = line.split(',')[1]
        fix_ts = int(this_ts[:-3])
        if begin_ts <= fix_ts and fix_ts <= end_ts:
            inf_event = line.split(',')[-2]
            res.append(inf_event)
            print(line)
        elif fix_ts > end_ts:
            break
    return res

print(findMatchedTS(obj_stamp1,obj_stamp2))

