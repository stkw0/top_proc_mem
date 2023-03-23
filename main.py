import matplotlib.pyplot as plt
import itertools
import os

PAGE_SIZE = 4 * 1024

all_procs = {}
def update():
    curr_proc = []
    for f in os.listdir("/proc"):
        if f.isnumeric():
            try:
                p = "/proc/{}/statm".format(f)
                rss_pages = int(open(p, "r").read().split()[1])
                if rss_pages == 0:
                    continue

                mem_mbytes = (rss_pages * PAGE_SIZE) / 1024 / 1024

                # discard small process
                if mem_mbytes < 100:
                    continue

                p = "/proc/{}/comm".format(f)
                comm = open(p, "r").read().strip()[0:8] + "_" + f

                if comm not in all_procs:
                    all_procs[comm] = []

                all_procs[comm].append(mem_mbytes)
                curr_proc.append(comm)
            except FileNotFoundError:
                continue

    to_be_removed = []
    for i in all_procs.keys():
        if i not in curr_proc:
            to_be_removed.append(i)

    for i in to_be_removed:
        del all_procs[i]

plt.ion()
while True:
    update()
    keys = list(dict(sorted(all_procs.items(), key=lambda item: item[-1][-1] or 0)).keys())[-10:]

    max_len = -1
    for i in keys:
        if len(all_procs[i]) > max_len:
            max_len = len(all_procs[i])

    for i in keys:
        while len(all_procs[i]) < max_len:
            all_procs[i].insert(0, None)

    ls = itertools.cycle(('-', '--', '-.', ':'))
    marker = itertools.cycle((',', '+', '.'))
    for k in keys:
        plt.plot(all_procs[k], label=k, marker=next(marker), linestyle=next(ls))
        plt.gcf().autofmt_xdate()
    plt.ylabel("MB")
    plt.legend()
    plt.draw()
    plt.pause(15)
    plt.clf()
