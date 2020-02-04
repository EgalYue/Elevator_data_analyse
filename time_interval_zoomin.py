import time
import datetime
from datetime import datetime
import argparse
import sys


def readTXT(file_path): # this file can be very big!!!
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines


def convert_ts_to_realTime(timeNum): # us
    timeStamp = float(timeNum/1000000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    # print(type( otherStyleTime))
    return otherStyleTime # str


def realTime_to_timeStamp(rt_str):
    datetime_obj = datetime.strptime(rt_str, "%Y-%m-%d %H:%M:%S.%f")
    obj_stamp = int((time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0) * 1000.0)
    return obj_stamp # us


def get_required_data(begin_ts, end_ts):
    """

    :param begin_ts:  str us
    :param end_ts:  str us
    :return:
    """
    d_sensor1 = dict()
    d_sensor2 = dict()

    for line in BIG_LIST:
        line = line.strip('\n')
        if not line:
            continue

        this_ts = line.split(',')[1] # str us
        this_rt = convert_ts_to_realTime(int(this_ts)) # str
        inf_event = line.split(',')[-2]

        if begin_ts <= int(this_ts) and int(this_ts) <= end_ts:
            if this_rt in d_sensor1.keys():
                if inf_event == '1':
                    d_sensor1[this_rt] = d_sensor1[this_rt] + 1
            else:
                if inf_event == '1':
                    d_sensor1[this_rt] = 1
                else:
                    d_sensor1[this_rt] = 0

            if this_rt in d_sensor2.keys():
                if inf_event == '2':
                    d_sensor2[this_rt] = d_sensor2[this_rt] + 1
            else:
                if inf_event == '2':
                    d_sensor2[this_rt] = 1
                else:
                    d_sensor2[this_rt] = 0
        elif int(this_ts) > end_ts:
            break

    return list(d_sensor1.keys()), list(d_sensor1.values()), list(d_sensor2.values())


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


def parse_args():
    """
    parse arguments
    """
    parse = argparse.ArgumentParser(description = "Give a name!")
    parse.add_argument("--txt_path", metavar="txt_path", nargs="?",
                       help="txt file path", required=True)
    parse.add_argument("--begin_realtime", metavar="begin_realtime", nargs="?",
                       help= "begin realtime", required=True)
    parse.add_argument("--end_realtime", metavar="end_realtime", nargs="?",
                       help= "end realtime", required=True)
    parse.add_argument("--res_path", metavar="res_path", nargs="?", default="time_interval_detail.html",
                       help="figure result path(html)", required=False)

    if len(sys.argv) < 2:
        parse.print_help()
        sys.exit(1)

    parsed = parse.parse_args()
    return parsed


if __name__ == '__main__':
    args = parse_args()
    txt_path = args.txt_path
    begin_realtime = args.begin_realtime
    end_realtime = args.end_realtime
    res_path = args.res_path

    print(">>> Generating html figure... ")
    BIG_LIST = readTXT(txt_path)
    # begin_ts = realTime_to_timeStamp('2020-01-20 17:13:11.200')
    # end_ts = realTime_to_timeStamp('2020-01-20 17:13:21.965')
    begin_ts = realTime_to_timeStamp(begin_realtime)
    end_ts = realTime_to_timeStamp(end_realtime)
    rt_list, sensor1_list, sensor2_list = get_required_data(begin_ts, end_ts)
    plot(rt_list, sensor1_list, sensor2_list, 'detail', res_path)
    print(">>> Done!")