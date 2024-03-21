#!usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from os import system

# Creation of command line arguments
parser = argparse.ArgumentParser(description='Scheduler simulation.')
# parser.add_argument('quantum', type=int, help='Time window that each process has in turn to execute.')
parser.add_argument('file', type=str, help='Name of the file containing the process descriptions.')
args = parser.parse_args()

# Variables used to color the text output
GREEN, RED, WHITE, BLUE, YELLOW = '\033[1;32m', '\033[91m', '\033[0m', '\33[94m', '\33[93m'

# Reads the process file and puts all of them into a list
def read(file):
    processes = list()
    with open(file) as f:
        for line in f.readlines():
            processes.append(line.strip('\n').split())

    for i in range(len(processes)): # Converts numbers to integer types
        processes[i][1] = int(processes[i][1])
        processes[i][2] = int(processes[i][2])

    processes.sort(key=lambda x: x[1]) # Sorts the processes by order of arrival
    return processes

def sjf(processes, execution_list): # Shortest Job First
    print("{}[+]{} Using Shortest Job First".format(GREEN, YELLOW))
    # print("\n{}[+]{} Execution: \n".format(GREEN, WHITE))
    round_num = 0
    processes.sort(key=lambda x: (x[2], x[1])) # Sorts the process queue by duration and then by arrival
    while processes: # While there are still processes waiting in the queue
        if processes[0][1] <= round_num: # If the first process in the queue has already arrived
            execute(processes[0], round_num, execution_list) # Displays the execution
            print(processes)
            processes[0][2] -= 1 # Executes one round of the process
            round_num += 1
            if processes[0][2] == 0: # If the process has finished execution
                del processes[0]

            # Checks if a shorter process arrived at this moment
            for i in range(len(processes)):
                # If the process in question has already arrived and is shorter than the current one
                if processes[i][1] <= round_num and processes[i][2] < processes[0][2]:
                    processes.insert(0, processes.pop(i)) # Moves the process to the beginning of the list
                    break

        else: # If the first process has not yet arrived
            # Looks in the queue to see if any process has already arrived
            for i in range(len(processes)):
                if processes[i][1] <= round_num: # If the process in question has arrived
                    processes.insert(0, processes.pop(i)) # Moves the process to the beginning of the list
                    break
            else: # If no process can execute at this moment
                execute("wait", round_num, execution_list)
                print(processes)
                round_num += 1
    return


def round_robin(processes, execution_list):
    print(f"{GREEN}[+]{YELLOW} Using Round-Robin")
    while True:
        try:
            quantum = int(input(f"{GREEN}[+]{WHITE} Enter the quantum size (time window) dedicated to each process at a time: "))
            break
        except ValueError:
            print(f"{RED}[-]{WHITE} Please, only enter integer numbers.")
    print("\\n{}[+]{} Execution: \\n".format(GREEN, WHITE))
    round_num = 0
    while processes: # While there are still processes waiting for execution
        if processes[0][1] <= round_num: # If the process at the start of the queue has already arrived
            if processes[0][2] >= quantum: # If the quantum size is smaller than the number of rounds remaining
                execute(processes[0], round_num, execution_list, quantum) # Executes the process, quantum times
                print(processes)
                processes[0][2] -= quantum # Subtracts the executed rounds from the total
                round_num += quantum
                if processes[0][2] == 0: # If the process has finished execution
                    processes.pop(0) # Removes it from the queue
                    continue

                elif len(processes) > 1:
                    for i in range(1, len(processes)): # Checks if another process has arrived and can be executed
                        if processes[i][1] <= round_num: # If the process has arrived in this round
                            aux = processes.pop(i) # Saves it under an auxiliary name
                            processes.append(processes.pop(0)) # Moves the current process from the start to the end of the queue
                            processes.insert(0, aux) # Inserts the auxiliary at the start of the queue
                            break

                else: # If the next process can be executed
                    processes.append(processes.pop(0)) # Moves the current process from the start to the end of the queue

            else: # If the quantum size is larger than the number of rounds remaining
                execute(processes[0], round_num, execution_list, processes[0][2]) # Executes only the number of remaining rounds
                print(processes)
                round_num += processes[0][2] # Increments the round by the number of rounds executed
                processes.pop(0) # Removes the process from the queue, as it has finished executing
        else: # If the process at the start of the queue has not yet arrived
            execute('wait', round_num, execution_list)
            print(processes)
            round_num += 1
            continue

def fcfs(processes, execution_list):
    print(f"{GREEN}[+]{YELLOW} Using First-come, First-served")
    print(f"\n{GREEN}[+]{WHITE} Execution:\n")
    # In this case, the processes are sorted by order of arrival
    round_num = 0
    while processes:  # While there are processes in the execution queue
        if processes[0][1] <= round_num:  # If the process that is first in the queue has already arrived at the current round
            execute(processes[0], round_num, execution_list)  # Executes a round of the process
            print(processes)
            processes[0][2] -= 1  # Reduces a round from the remaining rounds for the completion of the process
            round_num += 1  # Increments the number of executed rounds
            if processes[0][2] == 0:  # If the execution of the process is finished
                processes.pop(0)  # Removes the process from the execution queue
        else:  # If the first process in the queue has not arrived yet
            execute('wait', round_num, execution_list)
            print(processes)
            round_num += 1

def execute(p, round_num, execution_list, quantum=1):  # Keeps the quantum as 1 by default, for strategies different from round_robin
    if p == 'wait':
        execution_list.append(['wait'])
    else:
        for i in range(quantum):
            execution_list.append([p[0].upper(), p[2] - (i + 1)])

def display(execution_list):
    position = 1  # Starts with 1 instead of 0, because range(0) does not generate any iteration
    while True:
        system('clear')
        print(f"{GREEN}[+]{YELLOW} Execution:\n")
        for i in range(position):
            if execution_list[i][0] == 'wait':
                print(f"{GREEN}[WAIT]")
            elif i > 0 and execution_list[i - 1][0] != execution_list[i][0]:
                print(f"{GREEN}[+]{YELLOW} Process {execution_list[i][0]}:")
                print(f"{GREEN}[{execution_list[i][0]}]{WHITE} Remaining: {execution_list[i][1]}")
            else:
                print(f"{GREEN}[{execution_list[i][0]}]{WHITE} Remaining: {execution_list[i][1]}")

        opt = input(f"\n{GREEN}[+]{WHITE} Press 'n' to advance, 'b' to go back, or 'q' to exit: ")

        if opt == 'n' and position < len(execution_list):
            position += 1
        elif opt == 'n' and position == len(execution_list):
            print(f"\n{GREEN}[+]{WHITE} Completed.\n")
            break
        elif opt == 'b' and position > 1:
            position -= 1
        elif opt == 'q':
            raise SystemExit

def header(processes, execution_list):
    modes = [fcfs, sjf, round_robin]
    while True:
        opt = input("\n{}-> Choose the scheduling algorithm to be executed:\n\n".format(GREEN)
        + "{}[0]{} First-come, First-served\n".format(BLUE, WHITE)
        + "{}[1]{} Shortest Job First\n".format(BLUE, WHITE)
        + "{}[2]{} Round-Robin\n".format(BLUE, WHITE)
        + "{}[3]{} Exit the program\n".format(BLUE, WHITE)
        + "\n{}[+]{} Your option: ".format(GREEN, WHITE))

        if opt in ['0', '1', '2']:
            modes[int(opt)](processes, execution_list)
            display(execution_list)
        elif opt == '3':
            return opt
            break
        else:
            print("\n{}[-]{} Please choose a valid option.\n".format(RED, WHITE))

def main(file, out=True):
    GREEN, RED, WHITE, BLUE = '\\033[1;32m', '\\033[91m', '\\033[0m', '\\033[94m'
    processes = read(file)
    execution_list = list()
    opt = header(processes, execution_list)
    if opt == '3':
        print("\n{}[-]{} Shutting down...".format(RED, WHITE))
    else:
        display(execution_list)
        main(args.file)

print("""{}
  ______               _                       _
 |  ____|             | |                     | |
 | |__   ___  ___ __ _| | ___  _ __   __ _  __| | ___  _ __
 |  __| / __|/ __/ _` | |/ _ \| '_ \\ / _` |/ _` |/ _ \\| '__|
 | |____\\__ \\ (_| (_| | | (_) | | | | (_| | (_| | (_) | |
 |______|___/\\___\\__,_|_|\\___/|_| |_|\\__,_|\\__,_|\\___/|_|
     """.format(GREEN))
main(args.file)
