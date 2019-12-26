import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from day11 import execute


def input_provider(queue):
    yield queue.get()
    while True:
        if SHOULD_STOP:
            return -1
        if queue.empty():
            yield -1
            time.sleep(1e-2)
        else:
            x, y = queue.get()
            yield x
            yield y


def machine(program, egress):
    def instance(idx, ingress):
        program_instance = program[:]
        ingress.put(idx)
        provider = input_provider(ingress)
        pc = rb = 0
        while True:
            d, pc, rb = execute(program_instance, provider, pc, rb)
            x, pc, rb = execute(program_instance, provider, pc, rb)
            y, pc, rb = execute(program_instance, provider, pc, rb)
            if SHOULD_STOP:
                return
            egress.put((d, (x, y)))
    return instance


if __name__ == "__main__":
    with open("../input/day23.txt") as f:
        program_text = f.readline()
    p = [int(val) for val in program_text.split(",")]
    egress_queue = Queue()
    ingress_queues = [Queue() for _ in range(50)]
    SHOULD_STOP = False
    with ThreadPoolExecutor(max_workers=50) as executer:
        executer.map(machine(p, egress_queue), range(50), ingress_queues)
        last_sent = nat = (None, None)
        while True:
            if egress_queue.empty() and all(q.empty() for q in ingress_queues):
                if last_sent[1] == nat[1]:
                    print(nat[1])  # Part 2
                    SHOULD_STOP = True
                    break
                ingress_queues[0].put(nat)
                last_sent = nat
            else:
                addr, payload = egress_queue.get()
                if addr == 255:
                    if nat == (None, None):
                        print(payload[1])  # Part 1
                    nat = payload
                else:
                    ingress_queues[addr].put(payload)
