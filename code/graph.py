from functools import reduce
import matplotlib.pyplot as plot
import csv

def readCsv(filename):
    burstlist = []
    first_var = 2
    with open(filename) as csv_file:
        csv_r = csv.reader(csv_file, delimiter=",")
        for row in csv_r:
            burstlist.append((first_var, float(row[0]) * 1000 - first_var))
            first_var = float(row[1]) * 1000
        burstlist.append((first_var, 3 - first_var))
    return burstlist


# https://www.geeksforgeeks.org/python-basic-gantt-chart-using-matplotlib/
def plotBurstsGraph(cpu_list, io_list, cpuio_list):
    fig, gnt = plot.subplots()
    # Setting Y-axis limits
    gnt.set_ylim(0, 50)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time (in ms)')
    gnt.set_ylabel('Process')

    # Setting ticks on y-axis
    gnt.set_yticks([15, 25, 35])
    gnt.set_yticklabels(['CPU & IO driven', 'IO driven', 'CPU driven'])
    gnt.grid(True)

    # CPU
    gnt.broken_barh(cpu_list, (30, 9), facecolors =('tab:orange'))

    # IO
    gnt.broken_barh(io_list, (20, 9), facecolors =('tab:red'))

    # CPU & IO
    gnt.broken_barh(cpuio_list, (10, 9), facecolors ='tab:blue')

    plot.show()

def scheduleProcess(p1_list, p2_list, p3_list):
    fig, gnt = plot.subplots()
    # Setting Y-axis limits
    gnt.set_ylim(0, 60)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Time (in ms)')
    gnt.set_ylabel('Process')

    # Setting ticks on y-axis
    gnt.set_yticks([15, 25, 35, 45])
    gnt.set_yticklabels(['Schedule', 'CPU driven', 'IO driven', 'CPU & IO driven'])
    gnt.grid(True)

    gnt.broken_barh(p1_list, (40, 9), facecolors=('tab:orange'))
    gnt.broken_barh(p2_list, (30, 9), facecolors=('tab:red'))
    gnt.broken_barh(p3_list, (20, 9), facecolors=('tab:blue'))

    # Schedule
    tba = []
    sched = [p1_list.pop(0),
             p2_list.pop(0),
             p3_list.pop(0),
             p1_list.pop(0),
             p2_list.pop(0),
             p1_list.pop(0),
             p2_list.pop(0),
             p1_list.pop(0),
             p2_list.pop(0),
             p1_list.pop(0)
             ]
    sched = [x[1] for x in sched]
    val = 2
    for i in range(len(sched)):
        tba.append((val, sched[i]))
        val += sched[i]
    print(tba)
    gnt.broken_barh(
        tba,
        (10, 9),
        facecolors=('tab:orange', 'tab:red', 'tab:blue')
    )
    # gnt.broken_barh([p1_list[0]], (10, 9), facecolors=('tab:blue'))
    # gnt.broken_barh([p2_list[0]], (10, 9), facecolors=('tab:red'))

    """
    # Is not exact because doesn't handle burst bigger than 100ms like they should be
    # is fcfs
    processes = [(p1_list, 0, 'tab:orange'), (p2_list, 0, 'tab:red'), (p3_list, 0, 'tab:blue')]
    bursts = []
    color = ()
    totaltime = 0
    for i in range(10):
        processes = [x for x in processes if len(x[0]) != 0]
        wait_times = [x[1] for x in processes]
        print(wait_times)

        # if the wait time is not zero for atleast one of the processes then wait for the shortest amount of time needed to
        # w1 < 0 || w2 || w3
        if(reduce(lambda x, y: x < 0 or y < 0, wait_times)):
            gnt.broken_barh([min(wait_times)], (10, 9), facecolors=('tab:white'))
            processes = map(lambda process: (process[0], process[1] - min(wait_times), process[2]),processes)
            totaltime += min(wait_times)

        wtime = 0
        for process_list, wait_time, color in processes:
            # if wait time is not 0
            if(wait_time > 0):
                break
            p_tba = process_list.pop(0)
            wtime = p_tba[1]
            totaltime += wtime
            gnt.broken_barh([(p_tba[0] + totaltime, p_tba[1])], (10, 9), facecolors=(color))
            break
        processes = map(lambda process: (process[0], process[1] - wtime, process[2]),processes)
    """

    plot.show()

def plotPieChart(io_time, total_time, explode, save_loc):
    #plot.pie([50, 50])
    labels = ["CPU Time", "I/O Time"]
    plot.pie([(total_time - io_time) / total_time, io_time/total_time], labels = labels, explode = explode)
    plot.savefig(save_loc)
    plot.clf()

# Create pie chart
"""
# CPU
# total : 3.176224
# syscalls: 0.000680
plotPieChart(0.000680, 3.176224, [0.2, 0], "../report/CPUTimeDist.png")

# IO
# total : 1.844660
# syscalls: 1.045286
plotPieChart(1.045286, 1.844660, None, "../report/IOTimeDist.png")

# CPU & IO
# total : 4.093908
# syscalls: 1.838494
plotPieChart(1.838494, 4.093908, None, "../report/CPU&IOTimeDist.png")
"""

# Create gantt chart
cpu_burst = readCsv('cpudriven/bursts.csv')
io_burst = readCsv('iodriven/bursts.csv')
cpuio_burst = readCsv('cpu&iodriven/bursts.csv')

# print(cpu_burst)
# print('\n')
# print(io_burst)
# print('\n')
# print(cpuio_burst)
# print('\n')

scheduleProcess(cpuio_burst, io_burst, cpu_burst)
"""
"""

"""
def readCsv(filename):
    burstlist = []
    first_var = 2
    with open(filename) as csv_file:
        csv_r = csv.reader(csv_file, delimiter=",")
        for row in csv_r:
            burstlist.append((first_var, float(row[0]) * 1000 - first_var))
            first_var = float(row[1]) * 1000#- float(row[0]) * 1000
            # burstlist.append(
            #     (float(row[0]) * 1000,
            #      float(row[1]) * 1000 - float(row[0]) * 1000))
        # if len(burstlist) == 0:
        #     burstlist.append((2, 1))
        burstlist.append((first_var, 3 - first_var))
    return burstlist
"""
