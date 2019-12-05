"""
Modulee for the Intcode interpretor.
"""

from collections import namedtuple

# action returns non-none value if a jump occurred
Opcode = namedtuple("Opcode", "arg_count action jumps")


class Interpretor:
    """
    An intcode interpretor.
    """

    def __init__(self, inputter=None, outputter=None):
        self.memory = []
        self.ipointer = 0
        self.inputter = inputter
        self.outputter = outputter

        self.opcodes = {
            1: Opcode(3, self.add, False),
            2: Opcode(3, self.mul, False),
            3: Opcode(1, self.get_input, False),
            4: Opcode(1, self.put_output, False),
            5: Opcode(2, self.jump_if_true, True),
            6: Opcode(2, self.jump_if_false, True),
            7: Opcode(3, self.less, False),
            8: Opcode(3, self.equals, False),
        }

    def add(self, arg1, arg2, arg3):
        """
        Add two numbers and store in an output.
        """
        self.set(arg3, self.get(arg1) + self.get(arg2))

    def mul(self, arg1, arg2, arg3):
        """
        Multiply two numbers and store in an output.
        """
        self.set(arg3, self.get(arg1) * self.get(arg2))

    def get_input(self, arg1):
        """
        Store an input value.
        """
        if self.inputter is None:
            raise ValueError("This program requires an inputter")
        self.set(arg1, self.inputter())

    def put_output(self, arg1):
        """
        Output a value.
        """
        if self.outputter is None:
            raise ValueError("This program requires an outputter")
        self.outputter(self.get(arg1))

    def jump_if_true(self, arg1, arg2):
        """
        Jump based on the value of an argument.
        """
        if self.get(arg1) != 0:
            self.ipointer = self.get(arg2)
            return ()

    def jump_if_false(self, arg1, arg2):
        """
        Jump based on the value of an argument.
        """
        if self.get(arg1) == 0:
            self.ipointer = self.get(arg2)
            return ()

    def less(self, arg1, arg2, arg3):
        """
        Compare two numbers and store in an output.
        """
        self.set(arg3, int(self.get(arg1) < self.get(arg2)))

    def equals(self, arg1, arg2, arg3):
        """
        Compare two numbers and store in an output.
        """
        self.set(arg3, int(self.get(arg1) == self.get(arg2)))

    def get(self, arg):
        """
        Get a value from its parameter mode and index.
        """
        mode, idx = arg
        if mode == 0:
            return self.memory[idx]
        if mode == 1:
            return idx
        raise ValueError("Unknown parameter mode " + str(mode))

    def set(self, arg, value):
        """
        Set a value from its parameter mode and index.
        """
        mode, idx = arg
        if mode == 0:
            self.memory[idx] = value
        elif mode == 1:
            raise ValueError("Cannot write in immediate mode")
        else:
            raise ValueError("Unknown parameter mode " + str(mode))

    def step(self):
        """
        Execute the current instruction.
        """
        instruction = str(self.memory[self.ipointer])
        args = self.memory[self.ipointer + 1 :]
        opcode_value = int(instruction[-2:])
        param_modes = list(reversed([int(mode) for mode in instruction[:-2]]))
        if opcode_value == 99:
            return False
        opcode = self.opcodes[opcode_value]
        param_modes = param_modes + [0] * (opcode.arg_count - len(param_modes))
        if opcode.action(*list(zip(param_modes, args))) is None:
            self.ipointer = self.ipointer + opcode.arg_count + 1
        return True

    def run(self, opcodes, noun=None, verb=None):
        """
        Run a list of opcodes.
        """
        self.memory = opcodes.copy()
        if noun is not None:
            self.memory[1] = noun
        if verb is not None:
            self.memory[2] = verb
        while self.step():
            pass
        return self.memory[0]
