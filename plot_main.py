import csv
import datetime
from datetime import datetime
import time
import os
import sys
import argparse


rollback_t_list = []
rollback_sensor1_list = []
rollback_sensor2_list = []

goin_t_list = []
goin_sensor1_list = []
goin_sensor2_list = []

goout_t_list = []
goout_sensor1_list = []
goout_sensor2_list = []


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


def filter_robot_ID(file_path, desired_ID, result_file_path):
    res = []
    with open(file_path, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            if line[7] == desired_ID:
                res.append(line)

    with open(result_file_path, 'w') as f:
        for each in res:
            csvWriter = csv.writer(f,  dialect='excel')
            csvWriter.writerow(each)


def diagnoseCSV(file_path):
    with open(file_path, 'r') as f:
        lines = csv.reader(f)
        for line in lines:
            # print(line)
            if line[1] == 'go in elevator': # Inf_Event == 0
                go_in_elevator_time = line[2]
                goin_rollback_duration = float(line[5]) if line[5] != '' else 0
                begin_ts = realTime_to_timeStamp(go_in_elevator_time) # ms
                end_ts = int(begin_ts + goin_rollback_duration * 1000.0)
                end_rt = convert_ts_to_realTime(end_ts) + '.' + str(end_ts)[-3:]
                rollback_t_list.append(go_in_elevator_time + '~' + end_rt)

            elif line[1] == 'go out elevator': # Inf_Event != 0. twice: in and out.
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


def count_sensor_status(begin_ts, end_ts, t_threshold):
    # time_threshold [s]
    sensor1_tri = 0
    sensor2_tri  = 0

    last_1_ts = 0
    last_2_ts = 0

    for line in BIG_LIST:
        line = line.strip('\n')
        if not line:
            continue

        this_ts = line.split(',')[1]
        fix_ts = int(this_ts[:-3]) # ms
        if begin_ts <= fix_ts and fix_ts <= end_ts:
            inf_event = line.split(',')[-2]
            if inf_event == '1' and fix_ts - last_1_ts >= t_threshold * 1000: # t_threshold * 1000
                last_1_ts = fix_ts
                sensor1_tri = sensor1_tri + 1
            elif inf_event == '2' and fix_ts - last_2_ts >= t_threshold * 1000: # t_threshold * 1000
                last_2_ts = fix_ts
                sensor2_tri = sensor2_tri + 1

        elif fix_ts > end_ts:
            break
    return sensor1_tri, sensor2_tri

def getSensorStatus(t_list, sensor1_list, sensor2_list, t_threshold):
    for each in t_list:
        begin_t = each.split('~')[0]
        end_t = each.split('~')[1]
        begin_ts = realTime_to_timeStamp(begin_t)
        end_ts = realTime_to_timeStamp(end_t)
        sensor1_num, sensor2_num = count_sensor_status(begin_ts, end_ts, t_threshold)
        sensor1_list.append(sensor1_num)
        sensor2_list.append(sensor2_num)



#====================== plot ====================================

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

def statistic(sensor1_list, sensor2_list, flag):
    # flag: '11' '10' '01' '00'
    count = 0
    if flag == '11':
        for s1,s2 in zip(sensor1_list, sensor2_list):
            if s1 != 0 and s2 != 0:
                count = count + 1
    elif flag == '10':
        for s1, s2 in zip(sensor1_list, sensor2_list):
            if s1 != 0 and s2 == 0:
                count = count + 1
    elif flag == '01':
        for s1, s2 in zip(sensor1_list, sensor2_list):
            if s1 == 0 and s2 != 0:
                count = count + 1
    elif flag == '00':
        for s1, s2 in zip(sensor1_list, sensor2_list):
            if s1 == 0 and s2 == 0:
                count = count + 1
    return count

def get_all_str(t_list, sensor1_list, sensor2_list):
    l = len(t_list)
    flag_11 = statistic(sensor1_list, sensor2_list, '11')
    flag_10 = statistic(sensor1_list, sensor2_list, '10')
    flag_01 = statistic(sensor1_list, sensor2_list, '01')
    flag_00 = statistic(sensor1_list, sensor2_list, '00')

    res = str(l) + " " + str(flag_11) + " " + str(flag_10) + " " + str(flag_01) + " " + str(flag_00)
    return res

def statistic_3_actions(rollback_t_list, rollback_sensor1_list, rollback_sensor2_list,
                        goin_t_list, goin_sensor1_list, goin_sensor2_list,
                        goout_t_list, goout_sensor1_list, goout_sensor2_list,
                        result_path):

    with open(result_path, 'w') as f:
        describe_str0 = "# s1Y_s2Y: 传感器1,传感器2同时被触发的次数\n"
        describe_str1 = "# s1Y_s2N: 传感器1被触发,但是传感器2没有被触发的次数\n"
        describe_str2 = "# s1N_s2Y: 传感器1没有被触发,但是传感器2被触发的次数\n"
        describe_str3 = "# s1N_s2N: 传感器1,传感器2同时没有被触发的次数\n"
        head = "行为总次数 s1Y_s2Y s1Y_s2N s1N_s2Y s1N_s2N\n"


        f.write(describe_str0)
        f.write(describe_str1)
        f.write(describe_str2)
        f.write(describe_str3)
        f.write('\n')
        # rollback
        f.write("#行为1: 没成功进入电梯, rollback\n")
        f.write(head)
        f.write(get_all_str(rollback_t_list, rollback_sensor1_list, rollback_sensor2_list))
        f.write("\n")

        # goin
        f.write('\n')
        f.write("#行为2: 进入电梯\n")
        f.write(head)
        f.write(get_all_str(goin_t_list, goin_sensor1_list, goin_sensor2_list))
        f.write("\n")

        # goout
        f.write('\n')
        f.write("#行为3: 出梯\n")
        f.write(head)
        f.write(get_all_str(goout_t_list, goout_sensor1_list, goout_sensor2_list))
        f.write("\n")


def parse_args():
    """
    parse arguments
    """
    parse = argparse.ArgumentParser(description = "Give a name!")
    parse.add_argument("--csv_path", metavar="csv_path", nargs="?",
                       help= "csv file path", required=True)
    parse.add_argument("--txt_path", metavar="txt_path", nargs="?",
                       help="txt file path", required=True)
    parse.add_argument("--robot_ID", metavar="robot_ID", nargs="?",
                       help="robot_ID", required=True)
    parse.add_argument("--t_threshold", metavar="t_threshold", nargs="?",
                       help="t_threshold", required=True)
    parse.add_argument("--rollback_html_path", metavar="rollback_html_path", nargs="?", default="rollback.html",
                       help="rollback_html_path", required=False)
    parse.add_argument("--goin_html_path", metavar="goin_html_path", nargs="?", default="goin.html",
                       help="goin_html_path", required=False)
    parse.add_argument("--goout_html_path", metavar="goout_html_path", nargs="?", default="goout.html",
                       help="goout_html_path", required=False)
    parse.add_argument("--statistic_path", metavar="statistic_path", nargs="?", default="statistics.txt",
                       help="statistic_path", required=False)

    if len(sys.argv) < 2:
        parse.print_help()
        sys.exit(1)

    parsed = parse.parse_args()
    return parsed




if __name__ == '__main__':
    curr_proj_dir = os.path.dirname(os.path.realpath(__file__))

    args = parse_args()
    # input
    input_csv = args.csv_path
    input_txt = args.txt_path
    robot_ID = args.robot_ID  #'EVT6-2-16'
    t_threshold = int(args.t_threshold) # 1s

    # output
    rollback_html_path  = os.path.join(curr_proj_dir, args.rollback_html_path)
    goin_html_path = os.path.join(curr_proj_dir, args.goin_html_path)
    goout_html_path = os.path.join(curr_proj_dir, args.goout_html_path)
    statistic_path = os.path.join(curr_proj_dir, args.statistic_path)

    BIG_LIST = readTXT(input_txt)

    # filter given robot_ID, save to temp.csv
    temp_file_path = os.path.join(curr_proj_dir, 'temp.csv')
    filter_robot_ID(input_csv, robot_ID, temp_file_path)

    # read temp.csv and extract useful time
    diagnoseCSV(temp_file_path)

    print(">>> Runing, this maybe take a long time...")
    getSensorStatus(rollback_t_list, rollback_sensor1_list, rollback_sensor2_list, t_threshold)
    getSensorStatus(goin_t_list, goin_sensor1_list, goin_sensor2_list, t_threshold)
    getSensorStatus(goout_t_list, goout_sensor1_list, goout_sensor2_list, t_threshold)

    print(">>> Generating rollback html...")
    plot(rollback_t_list, rollback_sensor1_list, rollback_sensor2_list, 'rollback', rollback_html_path)
    print(">>> Generating goin html...")
    plot(goin_t_list, goin_sensor1_list, goin_sensor2_list, 'goin', goin_html_path)
    print(">>> Generating goout html...")
    plot(goout_t_list, goout_sensor1_list, goout_sensor2_list, 'goout', goout_html_path)
    print(">>> Done!")

    statistic_3_actions(rollback_t_list, rollback_sensor1_list, rollback_sensor2_list,
                        goin_t_list, goin_sensor1_list, goin_sensor2_list,
                        goout_t_list, goout_sensor1_list, goout_sensor2_list,
                        statistic_path)

    # remove temp.csv
    os.remove(temp_file_path)

