from typing import List

each_arrival_time = []
each_burst_time = []
# waiting_time = 0
# turnaround_time = 0
remaining_time = 0 # SRT and RR
completed_time = 0 # HRN
response_ratio = 0 # HRN
gantt_chart_format = "%3d\t%s"

# load a file
read_file = []
with open('Input.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    
    for line in lines:
        values = [v.strip() for v in line.strip().split(',')]
        read_file.append(values)

read_file.sort(key=lambda x: int(x[1]))

def fcfs(f_data: List[List[int]]):
    for i in range(len(f_data)):
        each_arrival_time.append(f_data[i][1])
        each_burst_time.append(f_data[i][2])
    
    # 간트차트 출력
    print("간트차트\nTime\tProcess")
    exec_time = int(each_arrival_time[0])
    
    for i in range(len(f_data)):
        print(gantt_chart_format % (exec_time, f_data[i][0]))
        exec_time += int(each_burst_time[i])
        print("...\t" + f_data[i][0])
        
        if (i == len(f_data) - 1):
            print(gantt_chart_format % (exec_time, f_data[i][0]))
    
    print()
            
    # 나머지 정보 출력
    waiting_time = 0
    turnaround_time = 0
    ave_waiting = ave_turnaround = 0
    exec_time = int(each_arrival_time[0])
    
    print("{:<15}{:<15}{:<15}".format("Process", "Waiting Time", "Turnaround Time"))
    
    for i in range(len(f_data) + 1):
        if(i == len(f_data)):
            print("{:<15}{:<15.3f}{:<15.3f}".format("Average", ave_waiting / len(f_data), ave_turnaround / len(f_data)))
        
        else:
            waiting_time = exec_time - int(each_arrival_time[i])
            turnaround_time = waiting_time + int(each_burst_time[i])
            exec_time += int(each_burst_time[i])
            
            print("{:<15}{:<15d}{:<15d}".format(f_data[i][0], waiting_time, turnaround_time))
            
            ave_waiting += waiting_time
            ave_turnaround += turnaround_time
    
# def sjf(f_data: List[List[int]]):
    
    
    


# print("Select Scheduling Algorithm (1. FCFS, 2. SJF, 3. HRN, 4. RR, 5. SRT) ?")

# print("간트차트\nTime\tProcess")
# print("Process\tWaiting Time\tTurnaround Tine")

fcfs(read_file)