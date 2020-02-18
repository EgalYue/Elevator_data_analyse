import argparse
import sys
import os
import datetime
import csv
import time
from datetime import datetime

ERROR_LOG = []

def write_result_to_txt(file_path, write_content):
    with open(file_path, 'w') as f:
        for each in write_content:
            f.write(','.join(each))
            f.write('\n')

def readTXT(file_path): # this file can be very big!!!
    with open(file_path, 'r') as f:
        lines = f.readlines()
        return lines

def realTime_to_timeStamp(rt_str):
    datetime_obj = datetime.strptime(rt_str, "%Y-%m-%d %H:%M:%S.%f")
    obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
    return obj_stamp # ms


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
        elif fix_ts > end_ts:
            break
    return res


def analyse_Inf_Event_list(inf_event_list, desired_status):
    # desired_status: 0 1 2
    if not inf_event_list:
        return False

    if desired_status == 0: # not see the gap
        for each in inf_event_list:
            if '1' in each or '2' in each:
                return False
        return True
    else: # see the gap
        for each in inf_event_list:
            if '1' in each or '2' in each:
                return True
        return False


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

                inf_event_list = findMatchedTS(begin_ts, end_ts)
                if not analyse_Inf_Event_list(inf_event_list, 0):
                     ERROR_LOG.append(line)


            elif line[1] == 'go out elevator': # succ, Inf_Event != 0. twice: in and out.
                # 1. go in
                go_in_elevator_time = line[2]
                goin_duration = float(line[4]) if line[4] != '' else 0
                begin_in_ts = realTime_to_timeStamp(go_in_elevator_time)
                end_in_ts = int(begin_in_ts + goin_duration * 1000.0)

                inf_event_list = findMatchedTS(begin_in_ts, end_in_ts)
                if not analyse_Inf_Event_list(inf_event_list, 1):
                    ERROR_LOG.append(line)

                # 2. go out
                go_out_elevator_time = line[3]
                goout_duration = float(line[6]) if line[6] != '' else 0
                begin_out_ts = realTime_to_timeStamp(go_out_elevator_time)
                end_out_ts = int(begin_out_ts + goout_duration * 1000.0)

                inf_event_list = findMatchedTS(begin_out_ts, end_out_ts)
                if not analyse_Inf_Event_list(inf_event_list, 1):
                    ERROR_LOG.append(line)


def parse_args():
    """
    parse arguments
    """
    parse = argparse.ArgumentParser(description = "Give a name!")
    parse.add_argument("--csv_path", metavar="csv_path", nargs="?",
                       help= "csv file path", required=True)
    parse.add_argument("--txt_path", metavar="txt_path", nargs="?",
                       help="txt file path", required=True)
    parse.add_argument("--res_path", metavar="res_path", nargs="?", default="result.txt",
                       help="result file path", required=False)

    if len(sys.argv) < 2:
        parse.print_help()
        sys.exit(1)

    parsed = parse.parse_args()
    return parsed


if __name__ == '__main__':
    print ('...')
    args = parse_args()
    input_csv = args.csv_path
    input_txt = args.txt_path
    output = args.res_path

    BIG_LIST = readTXT(input_txt)  # TODO read big file only once
    diagnoseCSV(input_csv)
    write_result_to_txt(output, ERROR_LOG)


