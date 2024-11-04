from typing import List
import queue
import copy

class Process:
    def __init__(self, name, arrival_time, burst_time):
        self.name = name
        self.arrival_time = int(arrival_time)
        self.burst_time = int(burst_time)
        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
        self.remaining_time = int(burst_time)  # For SRT
        self.response_ratio = 0  # For HRN

def load_processes(filename: str) -> List[Process]:
    processes = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            name, arrival, burst = [v.strip() for v in line.strip().split(',')]
            processes.append(Process(name, arrival, burst))
    return processes

def print_gantt_chart(current_time: int, process_name: str, is_final: bool = False):
    
    if not is_final:
        print(f"{current_time:3d}\t{process_name}")
        print(f"...\t{process_name}")
    else:
        print(f"{current_time:3d}\t{process_name}")

def print_results(processes: List[Process]):
    print("\n{:<15}{:<15}{:<15}".format("Process", "Waiting Time", "Turnaround Time"))
    
    total_waiting = 0
    total_turnaround = 0
    
    for proc in processes:
        print("{:<15}{:<15d}{:<15d}".format(
            proc.name, 
            proc.waiting_time, 
            proc.turnaround_time
        ))
        total_waiting += proc.waiting_time
        total_turnaround += proc.turnaround_time
    
    n = len(processes)
    print("{:<15}{:<15.3f}{:<15.3f}".format(
        "Average", 
        total_waiting / n, 
        total_turnaround / n
    ))

def fcfs(processes: List[Process]):
    current_time = processes[0].arrival_time
    
    for i, proc in enumerate(processes):
        print("간트차트\nTime\tProcess")
        print_gantt_chart(current_time, proc.name)
        
        proc.waiting_time = current_time - proc.arrival_time
        proc.turnaround_time = proc.waiting_time + proc.burst_time
        current_time += proc.burst_time
        proc.completion_time = current_time
        
        if i == len(processes) - 1:
            print_gantt_chart(current_time, proc.name, True)
    
    print_results(processes)

def sjf(processes: List[Process]):
    ready_queue = []
    completed_processes = []
    current_time = 0
    processes = copy.deepcopy(processes)
    
    while len(completed_processes) < len(processes):
        # 현재 시간에 도착한 프로세스들을 ready queue에 추가
        for proc in processes:
            if proc.arrival_time <= current_time and proc not in completed_processes and proc not in ready_queue:
                ready_queue.append(proc)
        
        if not ready_queue:
            current_time += 1
            continue
        
        # burst time이 가장 짧은 프로세스 선택
        next_process = min(ready_queue, key=lambda x: x.burst_time)
        ready_queue.remove(next_process)
        
        print("간트차트\nTime\tProcess")
        print_gantt_chart(current_time, next_process.name)
        
        # 프로세스 실행
        next_process.waiting_time = current_time - next_process.arrival_time
        next_process.turnaround_time = next_process.waiting_time + next_process.burst_time
        current_time += next_process.burst_time
        next_process.completion_time = current_time
        
        completed_processes.append(next_process)
        
        if len(completed_processes) == len(processes):
            print_gantt_chart(current_time, next_process.name, True)
    
    print_results(completed_processes)
    
def calculate_response_ratio(process: Process, current_time: int) -> float:
    waiting_time = current_time - process.arrival_time
    return (waiting_time + process.burst_time) / process.burst_time

def hrn(processes: List[Process]):
    ready_queue = []
    completed_processes = []
    current_time = 0
    processes = copy.deepcopy(processes)
    
    while len(completed_processes) < len(processes):
        # 현재 시간에 도착한 프로세스들을 ready queue에 추가
        for proc in processes:
            if proc.arrival_time <= current_time and proc not in completed_processes and proc not in ready_queue:
                ready_queue.append(proc)
        
        if not ready_queue:
            current_time += 1
            continue
        
        # 각 프로세스의 응답률 계산
        for proc in ready_queue:
            proc.response_ratio = calculate_response_ratio(proc, current_time)
        
        # 응답률이 가장 높은 프로세스 선택
        next_process = max(ready_queue, key=lambda x: x.response_ratio)
        ready_queue.remove(next_process)
        
        print("간트차트\nTime\tProcess")
        print_gantt_chart(current_time, next_process.name)
        
        # 프로세스 실행
        next_process.waiting_time = current_time - next_process.arrival_time
        next_process.turnaround_time = next_process.waiting_time + next_process.burst_time
        current_time += next_process.burst_time
        next_process.completion_time = current_time
        
        completed_processes.append(next_process)
        
        if len(completed_processes) == len(processes):
            print_gantt_chart(current_time, next_process.name, True)
    
    print_results(completed_processes)
    
def rr(processes: List[Process], time_quantum: int = 4):
    processes = copy.deepcopy(processes)
    ready_queue = []
    current_time = 0
    completed_processes = []
    
    # 각 프로세스의 남은 시간 초기화
    for proc in processes:
        proc.remaining_time = proc.burst_time
    
    print("간트차트\nTime\tProcess")
    
    while len(completed_processes) < len(processes):
        # 새로 도착한 프로세스들을 ready queue에 추가
        for proc in processes:
            if proc.arrival_time <= current_time and proc not in completed_processes and proc not in ready_queue:
                ready_queue.append(proc)
        
        if not ready_queue:
            current_time += 1
            continue
        
        # 현재 프로세스 선택
        current_process = ready_queue.pop(0)
        
        # time quantum만큼 실행
        execution_time = min(time_quantum, current_process.remaining_time)
        print_gantt_chart(current_time, current_process.name)
        
        current_process.remaining_time -= execution_time
        current_time += execution_time
        
        # 프로세스가 완료되었는지 확인
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed_processes.append(current_process)
            if len(completed_processes) == len(processes):
                print_gantt_chart(current_time, current_process.name, True)
        else:
            # 아직 실행이 남은 프로세스는 다시 ready queue에 추가
            ready_queue.append(current_process)
    
    print_results(completed_processes)

def srt(processes: List[Process]):
    processes = copy.deepcopy(processes)
    ready_queue = []
    current_time = 0
    completed_processes = []
    current_process = None
    
    # 각 프로세스의 남은 시간 초기화
    for proc in processes:
        proc.remaining_time = proc.burst_time
    
    print("간트차트\nTime\tProcess")
    
    while len(completed_processes) < len(processes):
        # 새로 도착한 프로세스들을 ready queue에 추가
        for proc in processes:
            if proc.arrival_time <= current_time and proc not in completed_processes and proc not in ready_queue:
                ready_queue.append(proc)
        
        if not ready_queue:
            current_time += 1
            continue
        
        # remaining time이 가장 짧은 프로세스 선택
        next_process = min(ready_queue, key=lambda x: x.remaining_time)
        
        if current_process != next_process:
            if current_process is not None:
                print_gantt_chart(current_time, current_process.name)
            current_process = next_process
        
        # 1단위 시간만큼 실행
        current_process.remaining_time -= 1
        current_time += 1
        
        # 프로세스가 완료되었는지 확인
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            completed_processes.append(current_process)
            ready_queue.remove(current_process)
            if len(completed_processes) == len(processes):
                print_gantt_chart(current_time, current_process.name, True)
    
    print_results(completed_processes)

def main():
    processes = load_processes('Input.txt')
    processes.sort(key=lambda x: x.arrival_time)  # 도착 시간 기준 정렬
    
    while True:
        answer = input("\nSelect Scheduling Algorithm (1. FCFS, 2. SJF, 3. HRN, 4. RR, 5. SRT, 6. exit) ? ")
        
        if answer == '6':
            break
        elif answer == '1':
            fcfs(copy.deepcopy(processes))
        elif answer == '2':
            sjf(copy.deepcopy(processes))
        elif answer == '3':
            hrn(copy.deepcopy(processes))
        elif answer == '4':
            rr(copy.deepcopy(processes))
        elif answer == '5':
            srt(copy.deepcopy(processes))
        # 나머지 알고리즘들은 추후 구현 가능
        else:
            print("아직 구현되지 않은 알고리즘입니다.")

if __name__ == "__main__":
    main()