import time
from datetime import datetime
timestr = '2020-01-19 17:21:52.141'

# timestr = '2020-01-19 17:22:37.101'
datetime_obj = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")
obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)
print(time.mktime(datetime_obj.timetuple()) * 1000.0)
print(datetime_obj.microsecond / 1000.0)
print(obj_stamp)



input = '44.96'
import math

integer = math.modf(float(input))[1]
decimal = math.modf(float(input))[0]
obj_stamp = int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0 + float(input)* 1000.0)
print(obj_stamp)


# 1579425712141
# 1579469713101


# 1579425757101
# 1579425757101

