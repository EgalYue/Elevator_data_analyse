# 分析 elevator_data   


## 使用说明  
直接运行 `run_plot_main.sh` 即可, 运行结果默认保存在当前目录. 也可以指定输出名录, 具体参数自行查看 `plot_main.py`  


### 生成三段图表  
1. 没成功进电梯,rollback.html     
2. 进梯, goin.html  
3. 出梯, goout.html    
横轴为某一行为的时间段, 纵轴为传感器的响应次数  



### 查看某一时间段内, 传感器的状态  
`python3 ./time_interval_zoomin.py --txt_path ./example_data/Air_log2.txt --begin_realtime '2020-01-20 17:13:11.200' --end_realtime '2020-01-20 17:13:21.965' --res_path ./result.html`

