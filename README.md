# 分析 elevator_data   


## 使用说明  
`python3 diagnose.py --csv_path ./example_data/elevator_data.csv --txt_path ./example_data/Air_log2.txt`  

or  

`python3 diagnose.py --csv_path ./example_data/elevator_data.csv --txt_path ./example_data/Air_log2.txt --res_path ./result.txt`  

不符合的结果写入`result.txt`  



### 生成三段图表(1. 没成功进电梯,rollback 2. 进梯 3. 出梯)  
横轴为某一行为的时间段, 纵轴为传感器的响应次数  



### 查看某一时间段内, 传感器的状态  
`python3 ./time_interval_zoomin.py --txt_path ./example_data/Air_log2.txt --begin_realtime '2020-01-20 17:13:11.200' --end_realtime '2020-01-20 17:13:21.965' --res_path ./result.html`

