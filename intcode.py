"""
Module for the Intcode interpretor.
"""

from collections import namedtuple
from enum import Enum

# action is a function which takes the arguments and returns whether a jump occured
Opcode = namedtuple("Opcode", "arg_count action")

JUMP = True
NO_JUMP = not JUMP

REFERENCE_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

CONTINUE = True
HALT = not CONTINUE


class Memory:
    """
    Memory for an intcode interpretor.
    """

    def __init__(self):
        self.arr = []

    def _extend(self, idx):
        if isinstance(idx, slice):
            end = idx.stop
        else:
            end = idx + 1
        self.arr += [0] * (end - len(self.arr))

    def _validate_idx(self, idx):
        non_negative = idx.start >= 0 if isinstance(idx, slice) else idx >= 0
        assert non_negative, "negative indices not supported for memory access"
        self._extend(idx)

    def __getitem__(self, idx):
        self._validate_idx(idx)
        return self.arr.__getitem__(idx)

    def __setitem__(self, idx, value):
        self._validate_idx(idx)
        return self.arr.__setitem__(idx, value)

    def load(self, opcodes):
        """
        Load a program into memory, discarding any current data.
        """
        self.arr = opcodes.copy()

    def reset(self):
        """
        Reset memory to default state.
        """
        self.arr = []


class RunState(Enum):
    """
    State enum for the interpretor.
    """

    IDLE = 0
    RUNNING = 1
    WAITING_INPUT = 2
    GIVING_OUTPUT = 3


class Interpretor:
    """
    An intcode interpretor.
    """

    def __init__(self):
        self.memory = Memory()
        self.ipointer = 0
        self.rel_base = 0
        self.state = RunState.IDLE
        self.input_queue = []
        self.input_loc = None
        self.output_loc = None

        self.opcodes = {
            1: Opcode(arg_count=3, action=self._calculate(lambda x, y: x + y)),
            2: Opcode(arg_count=3, action=self._calculate(lambda x, y: x * y)),
            3: Opcode(arg_count=1, action=self._get_input),
            4: Opcode(arg_count=1, action=self._put_output),
            5: Opcode(arg_count=2, action=self._jump_if(lambda x: x != 0)),
            6: Opcode(arg_count=2, action=self._jump_if(lambda x: x == 0)),
            7: Opcode(arg_count=3, action=self._calculate(lambda x, y: x < y)),
            8: Opcode(arg_count=3, action=self._calculate(lambda x, y: x == y)),
            9: Opcode(arg_count=1, action=self._shift_rel_base),
        }

    def _calculate(self, func):
        def action(*args):
            self._set(args[-1], func(*map(self._get, args[:-1])))
            return NO_JUMP

        return action

    def _get_input(self, arg1):
        self.state = RunState.WAITING_INPUT
        self.input_loc = arg1
        if self.input_queue:
            self.receive_input(self.input_queue.pop(0))
        return NO_JUMP

    def _put_output(self, arg1):
        self.state = RunState.GIVING_OUTPUT
        self.output_loc = arg1
        return NO_JUMP

    def _jump_if(self, func):
        def action(*args):
            if func(*map(self._get, args[:-1])):
                self.ipointer = self._get(args[-1])
                return JUMP
            return NO_JUMP

        return action

    def _shift_rel_base(self, arg1):
        self.rel_base += self._get(arg1)
        return NO_JUMP

    def _get(self, arg):
        mode, idx = arg
        if mode == REFERENCE_MODE:
            return self.memory[idx]
        if mode == IMMEDIATE_MODE:
            return idx
        if mode == RELATIVE_MODE:
            return self.memory[self.rel_base + idx]
        raise ValueError("Unknown parameter mode " + str(mode))

    def _set(self, arg, value):
        mode, idx = arg
        if mode == REFERENCE_MODE:
            self.memory[idx] = value
        elif mode == IMMEDIATE_MODE:
            raise ValueError("Cannot write in immediate mode")
        elif mode == RELATIVE_MODE:
            self.memory[self.rel_base + idx] = value
        else:
            raise ValueError("Unknown parameter mode " + str(mode))

    def giving_output(self):
        """
        Check if the interpretor is giving output.
        """
        return self.state == RunState.GIVING_OUTPUT

    def query_output(self):
        """
        Extract the output from the interpretor when it is in the relevant state.
        """
        assert self.state == RunState.GIVING_OUTPUT, "no output to give"
        assert self.output_loc is not None

        result = self._get(self.output_loc)

        self.output_loc = None
        self.state = RunState.RUNNING
        return result

    def waiting_input(self):
        """
        Check if the interpretor is waiting for input.
        """
        return self.state == RunState.WAITING_INPUT

    def queue_input(self, value):
        """
        Queue a value to give as input automatically.
        """
        self.input_queue.append(value)

    def receive_input(self, input_value):
        """
        Send input to the interpretor when it is in the relevant state.
        """
        assert self.state == RunState.WAITING_INPUT, "unexpected input"
        assert self.input_loc is not None

        self._set(self.input_loc, input_value)

        self.input_loc = None
        self.state = RunState.RUNNING

    def _step(self):
        instruction = self.memory[self.ipointer]

        opcode_idx = instruction % 100
        mode_section = instruction // 100

        if opcode_idx == 99:
            return HALT

        if opcode_idx not in self.opcodes:
            raise ValueError(f"Unknown opcode {opcode_idx}")
        opcode = self.opcodes[opcode_idx]

        arg_start = self.ipointer + 1
        args = self.memory[arg_start : arg_start + opcode.arg_count + 1]
        param_modes = [(mode_section // 10 ** n) % 10 for n in range(opcode.arg_count)]

        if opcode.action(*zip(param_modes, args)) == NO_JUMP:
            self.ipointer = self.ipointer + opcode.arg_count + 1

        return CONTINUE

    def run(self, opcodes):
        """
        Run a list of opcodes, returning False after halting.

        usage looks like:

        ```
        while interpretor.run(program):
            if interpretor.state == RunState.WAITING_INPUT:
                interpretor.receive_input(my_input)
            elif interpretor.state == RunState.GIVING_OUTPUT:
                my_output = interpretor.query_output()

        # program halted
        ```
        """
        if self.waiting_input() or self.giving_output():
            return CONTINUE

        if self.state == RunState.IDLE:
            self.ipointer = 0
            self.memory.load(opcodes)

        self.state = RunState.RUNNING
        while self._step():
            if self.state != RunState.RUNNING:
                return CONTINUE

        self.state = RunState.IDLE
        return HALT

    def reset(self):
        """
        Reset the interpretor to an idle state.
        """
        self.state = RunState.IDLE
        self.ipointer = 0
        self.memory.reset()
