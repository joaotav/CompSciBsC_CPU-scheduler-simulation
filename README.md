# CPU Scheduling Visualization

This project provides a visualization tool for understanding how different CPU scheduling algorithms operate. It simulates the behavior of a CPU scheduler using three widely studied strategies:
- First-Come, First-Served (FCFS)
- Preemptive Shortest Job First (SJF)
- Round-Robin (RR)


## Getting Started

### Prerequisites
To run this project, ensure you have Python 3 installed on your machine. 

### Usage
To run the scheduler simulation, execute the following command in your terminal application:

```python3 scheduler.py processes.txt```

Where `processes.txt` is a required file that specifies the processes for the scheduler. 

#### Input File Format

The `processes.txt` file should contain one process per line, formatted as follows:

- **ID**: A unique identifier for the process.
- **Arrival Time**: The time at which the process arrives in the scheduling queue.
- **Length**: The total execution time required by the process.

**Example:**

A 0 4 \
B 1 3 \
C 2 4 \
D 3 3 \
E 3 1 \
F 7 3 \
G 8 2







