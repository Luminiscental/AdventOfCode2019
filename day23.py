"""AdventOfCode2019 - Day 23"""
from multiprocessing import Queue, Process, Event
import queue
import time
import intcode
from day02 import parse


class NATDevice:
    """Class for a NAT device. Receives packets."""

    def __init__(self, nics, idle_flags):
        self.received = Queue()
        self.nics = nics
        self.idle_flags = idle_flags

    def first_received(self):
        """Return the first received packet."""
        return self.received.get()

    def first_repeated(self):
        """Run the network until the NAT repeats itself, returning the repeated value."""
        seen = set()
        prev = None
        while True:
            # Get packets
            while True:
                try:
                    prev = self.received.get_nowait()
                except queue.Empty:
                    break
            # Check if the network is idle
            if all(flag.is_set() for flag in self.idle_flags):
                if prev in seen:
                    return prev
                seen.add(prev)
                for flag in self.idle_flags:
                    flag.clear()
                self.nics[0].received.put(prev)


class NIController:
    """Class for a Network Interface Controller. Sends and receives packets."""

    def __init__(self, program, address, idle_flag):
        self.program = program
        self.address = address
        self.received = Queue()
        self.next_input = None
        self.idle_flag = idle_flag
        self.input_cum = 0

    def _get_input(self):
        if self.next_input is not None:
            result, self.next_input = self.next_input, None
            return result
        try:
            result, self.next_input = self.received.get_nowait()
            return result
        except queue.Empty:
            self.input_cum += 1
            if self.input_cum > 2:
                self.idle_flag.set()
                self.input_cum = 0
            time.sleep(0.005)
            return -1

    def run(self, nat, nics):
        """Run the controller in an infinite loop."""
        machine = intcode.Interpretor(input_from=self._get_input)
        machine.queue_input(self.address)
        for dest, packet_x, packet_y in machine.run(self.program, group=3):
            self.input_cum = 0
            self.idle_flag.clear()
            packet = packet_x, packet_y
            if dest == 255:
                nat.received.put(packet)
            else:
                nics[dest].received.put(packet)


def run_network(program, nat_user):
    """Run a network, calling nat_user on the NAT once the network is set up."""
    idle_flags = [Event() for _ in range(50)]
    nics = [NIController(program, addr, idle_flags[addr]) for addr in range(50)]
    nat = NATDevice(nics, idle_flags)
    processes = [Process(target=nic.run, args=(nat, nics)) for nic in nics]
    for process in processes:
        process.start()
    result = nat_user(nat)
    for process in processes:
        process.kill()
    return result


def part1(program):
    """Solve for the answer to part 1."""
    packet = run_network(program, lambda nat: nat.first_received())
    return packet[1]


def part2(program):
    """Solve for the answer to part 2."""
    packet = run_network(program, lambda nat: nat.first_repeated())
    return packet[1]
