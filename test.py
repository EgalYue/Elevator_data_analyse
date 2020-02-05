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

# print(findMatchedTS(obj_stamp1,obj_stamp2))



def readTXT(file_path): # this file can be very big!!!
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines



def count_sensor_status(begin_ts, end_ts):
    res = []

    for line in BIG_LIST:
        line = line.strip('\n')
        if not line:
            continue

        this_ts = line.split(',')[1]
        fix_ts = int(this_ts[:-3]) # ms
        if begin_ts <= fix_ts and fix_ts <= end_ts:
            res.append(line)
            print(line)
        elif fix_ts > end_ts:
            break


    # with open('problem.txt', 'w') as f:
    #     for each in res:
    #         res.append(each)

def realTime_to_timeStamp(rt_str):
    datetime_obj = datetime.strptime(rt_str, "%Y-%m-%d %H:%M:%S.%f")
    obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return obj_stamp # ms

begin_ts = realTime_to_timeStamp('2020-01-20 15:56:42.290')
end_ts = realTime_to_timeStamp('2020-01-20 15:57:03.092')
BIG_LIST = readTXT('/home/yuehu/PycharmProjects/Elevator_data_analyse/example_data/Air_log2.txt')
count_sensor_status(begin_ts,end_ts)



