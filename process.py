import csv
import datetime
from datetime import datetime
import time

def realTime_to_timeStamp(rt_str):
    datetime_obj = datetime.strptime(rt_str, "%Y-%m-%d %H:%M:%S.%f")
    obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return obj_stamp # ms

def convert_ts_to_realTime(timeNum): # ms
    timeStamp = float(timeNum/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(type( otherStyleTime))
    return otherStyleTime # str


rollback_t_list = []
rollback_sensor1_list = []
rollback_sensor2_list = []

goin_t_list = []
goin_sensor1_list = []
goin_sensor2_list = []

goout_t_list = []
goout_sensor1_list = []
goout_sensor2_list = []


def diagnoseCSV(file_path):
    with open(file_path, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            # print(line)
            if line[1] == 'go in elevator': # not succ, Inf_Event == 0
                go_in_elevator_time = line[2]
                goin_rollback_duration = float(line[5]) if line[5] != '' else 0
                begin_ts = realTime_to_timeStamp(go_in_elevator_time) # ms
                end_ts = int(begin_ts + goin_rollback_duration * 1000.0)
                end_rt = convert_ts_to_realTime(end_ts) + '.' + str(end_ts)[-3:]
                rollback_t_list.append(go_in_elevator_time + '~' + end_rt)

            # TODO
            elif line[1] == 'go out elevator': # succ, Inf_Event != 0. twice: in and out.
                # 1. go in
                go_in_elevator_time = line[2]
                goin_duration = float(line[4]) if line[4] != '' else 0
                begin_in_ts = realTime_to_timeStamp(go_in_elevator_time)
                end_in_ts = int(begin_in_ts + goin_duration * 1000.0)
                end_in_rt = convert_ts_to_realTime(end_in_ts) + '.' + str(end_in_ts)[-3:]
                goin_t_list.append(go_in_elevator_time + '~' + end_in_rt)

                # 2. go out
                go_out_elevator_time = line[3]
                goout_duration = float(line[6]) if line[6] != '' else 0
                begin_out_ts = realTime_to_timeStamp(go_out_elevator_time)
                end_out_ts = int(begin_out_ts + goout_duration * 1000.0)
                end_out_rt = convert_ts_to_realTime(end_out_ts) + '.' + str(end_out_ts)[-3:]
                goout_t_list.append(go_out_elevator_time + '~' + end_out_rt)


def readTXT(file_path): # this file can be very big!!!
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines

BIG_LIST = readTXT('/home/yuehu/PycharmProjects/Elevator_data_analyse/example_data/Air_log2.txt')


def count_sensor_status(begin_ts, end_ts):
    sensor1_tri = 0
    sensor2_tri  = 0
    for line in BIG_LIST:
        line = line.strip('\n')
        if not line:
            continue

        this_ts = line.split(',')[1]
        fix_ts = int(this_ts[:-3])
        if begin_ts <= fix_ts and fix_ts <= end_ts:
            inf_event = line.split(',')[-2]
            if inf_event == '1':
                sensor1_tri = sensor1_tri + 1
            elif inf_event == '2':
                sensor2_tri = sensor2_tri + 1

        elif fix_ts > end_ts:
            break
    return sensor1_tri, sensor2_tri

def getSensorStatus(t_list, sensor1_list, sensor2_list):
    for each in t_list:
        begin_t = each.split('~')[0]
        end_t = each.split('~')[1]
        begin_ts = realTime_to_timeStamp(begin_t)
        end_ts = realTime_to_timeStamp(end_t)
        sensor1_num, sensor2_num = count_sensor_status(begin_ts, end_ts)
        sensor1_list.append(sensor1_num)
        sensor2_list.append(sensor2_num)



diagnoseCSV('/home/yuehu/PycharmProjects/Elevator_data_analyse/example_data/elevator_data.csv')
getSensorStatus(rollback_t_list, rollback_sensor1_list, rollback_sensor2_list)
getSensorStatus(goin_t_list, goin_sensor1_list, goin_sensor2_list)
getSensorStatus(goout_t_list, goout_sensor1_list, goout_sensor2_list)

# plot
def plot(t_list, sensor1_list, sensor2_list, title_str, htmlName):
    from pyecharts.charts.basic_charts.bar import Bar #导入相应包
    from pyecharts import options as opts
    from pyecharts.options import DataZoomOpts

    bar = Bar()#生成对象，title为柱状图标题
    #is_stack=True表示将数据堆叠，is_label_show=True表示显示对应数值
    bar.add_xaxis(t_list)
    bar.add_yaxis("sensor1触发次数",sensor1_list)
    bar.add_yaxis("sensor2触发次数",sensor2_list)
    bar.set_global_opts(title_opts=opts.TitleOpts(title=title_str),datazoom_opts=[DataZoomOpts(is_show=True, type_="slider")])

    bar.render(htmlName)


plot(rollback_t_list, rollback_sensor1_list, rollback_sensor2_list, 'rollback', 'rollback.html')
plot(goin_t_list, goin_sensor1_list, goin_sensor2_list, 'goin', 'goin.html')
plot(goout_t_list, goout_sensor1_list, goout_sensor2_list, 'goout', 'goout.html')