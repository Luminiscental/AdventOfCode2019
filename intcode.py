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

    def __init__(self, collect_outputs=False):
        self.memory = []
        self.ipointer = 0
        self.rel_base = 0
        self.state = RunState.IDLE

        self.outputs = []
        self.collect_outputs = collect_outputs

        self.input_queue = []
        self.input_loc = None
        self.output_loc = None

        self.opcodes = {
            1: Opcode(arg_count=3, action=self._add),
            2: Opcode(arg_count=3, action=self._mul),
            3: Opcode(arg_count=1, action=self._get_input),
            4: Opcode(arg_count=1, action=self._put_output),
            5: Opcode(arg_count=2, action=self._jump_if_true),
            6: Opcode(arg_count=2, action=self._jump_if_false),
            7: Opcode(arg_count=3, action=self._less),
            8: Opcode(arg_count=3, action=self._equals),
            9: Opcode(arg_count=1, action=self._shift_rel_base),
        }

    def _add(self, arg1, arg2, arg3):
        self._set(arg3, self._get(arg1) + self._get(arg2))
        return NO_JUMP

    def _mul(self, arg1, arg2, arg3):
        self._set(arg3, self._get(arg1) * self._get(arg2))
        return NO_JUMP

    def _get_input(self, arg1):
        self.state = RunState.WAITING_INPUT
        self.input_loc = arg1
        if self.input_queue:
            self.receive_input(self.input_queue.pop(0))
        return NO_JUMP

    def _put_output(self, arg1):
        self.state = RunState.GIVING_OUTPUT
        self.output_loc = arg1
        if self.collect_outputs:
            self.outputs.append(self.query_output())
        return NO_JUMP

    def _jump_if_true(self, arg1, arg2):
        if self._get(arg1) != 0:
            self.ipointer = self._get(arg2)
            return JUMP
        return NO_JUMP

    def _jump_if_false(self, arg1, arg2):
        if self._get(arg1) == 0:
            self.ipointer = self._get(arg2)
            return JUMP
        return NO_JUMP

    def _less(self, arg1, arg2, arg3):
        self._set(arg3, int(self._get(arg1) < self._get(arg2)))
        return NO_JUMP

    def _equals(self, arg1, arg2, arg3):
        self._set(arg3, int(self._get(arg1) == self._get(arg2)))
        return NO_JUMP

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

    def query_output(self):
        """
        Extract the output from the interpretor when it is in the relevant state.
        """
        assert self.state == RunState.GIVING_OUTPUT
        assert self.output_loc is not None

        result = self._get(self.output_loc)

        self.output_loc = None
        self.state = RunState.RUNNING
        return result

    def queue_input(self, value):
        """
        Queue a value to give as input automatically.
        """
        self.input_queue.append(value)

    def receive_input(self, input_value):
        """
        Send input to the interpretor when it is in the relevant state.
        """
        assert self.state == RunState.WAITING_INPUT
        assert self.input_loc is not None

        self._set(self.input_loc, input_value)

        self.input_loc = None
        self.state = RunState.RUNNING

    def _step(self):
        instruction = str(self.memory[self.ipointer])
        args = self.memory[self.ipointer + 1 :]
        opcode_value = int(instruction[-2:])
        param_modes = list(reversed([int(mode) for mode in instruction[:-2]]))
        if opcode_value == 99:
            return HALT
        opcode = self.opcodes[opcode_value]
        param_modes = param_modes + [0] * (opcode.arg_count - len(param_modes))
        if opcode.action(*list(zip(param_modes, args))) == NO_JUMP:
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
        if self.state == RunState.IDLE:
            self.ipointer = 0
            self.memory = opcodes.copy()
            self.memory += [0] * len(opcodes) * 10
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
        self.memory = []
