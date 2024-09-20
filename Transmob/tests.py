from random import randint

def vidduration():
    return randint(10,1000)

def sort_files():
    durations = {f: int(vidduration()) for f in range(10)}
    cores = [[(0, 0, 0)] for _ in range(3)]
    while durations:
        longest_vid = max(zip(durations.values(), durations.keys()))[1]
        shortest_core = min(cores, key=lambda x: x[-1][-1])
        d = durations.pop(longest_vid)
        shortest_core.append((longest_vid, d, shortest_core[-1][-1] + d))

    for core in cores:
        core.pop(0)
        print(core)
    final_order = []
    while any([len(c)>0 for c in cores]):
        earliest = min(cores, key=lambda x: x[0][-1]-x[0][-2])
        final_order.append(earliest.pop(0))
        if len(earliest) == 0:
            cores.remove(earliest)

    return final_order

if __name__ == '__main__':
    tasks = sort_files()
    print(tasks)