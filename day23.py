"""AdventOfCode2019 - Day 23"""
from multiprocessing import Queue, Process
import queue
import intcode
from day02 import parse


class NATDevice:
    """Class for a NAT device. Receives packets."""

    def __init__(self):
        self.received = Queue()

    def first_received(self):
        """Return the first received packet."""
        return self.received.get()


class NIController:
    """Class for a Network Interface Controller. Sends and receives packets."""

    def __init__(self, program, address):
        self.program = program
        self.address = address
        self.received = Queue()
        self.next_input = None

    def _get_input(self):
        if self.next_input is not None:
            result, self.next_input = self.next_input, None
            return result
        try:
            result, self.next_input = self.received.get_nowait()
            return result
        except queue.Empty:
            return -1

    def run(self, nat, nics):
        """Run the controller in an infinite loop."""
        machine = intcode.Interpretor(input_from=self._get_input)
        machine.queue_input(self.address)
        for dest, packet_x, packet_y in machine.run(self.program, group=3):
            packet = packet_x, packet_y
            if dest == 255:
                nat.received.put(packet)
            else:
                nics[dest].received.put(packet)


def run_network(program, nat_user):
    """Run a network, calling nat_user on the NAT once the network is set up."""
    nat = NATDevice()
    nics = [NIController(program, address) for address in range(50)]
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
    # return run_network(program, lambda nat: nat.first_repeated())
