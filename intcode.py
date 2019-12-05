"""
Modulee for the Intcode interpretor.
"""

from collections import namedtuple

# action is a function which takes the arguments and returns whether a jump occured
Opcode = namedtuple("Opcode", "arg_count action")


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
            1: Opcode(arg_count=3, action=self.add),
            2: Opcode(arg_count=3, action=self.mul),
            3: Opcode(arg_count=1, action=self.get_input),
            4: Opcode(arg_count=1, action=self.put_output),
            5: Opcode(arg_count=2, action=self.jump_if_true),
            6: Opcode(arg_count=2, action=self.jump_if_false),
            7: Opcode(arg_count=3, action=self.less),
            8: Opcode(arg_count=3, action=self.equals),
        }

    def add(self, arg1, arg2, arg3):
        """
        Add two numbers and store in an output.
        """
        self.set(arg3, self.get(arg1) + self.get(arg2))
        return False

    def mul(self, arg1, arg2, arg3):
        """
        Multiply two numbers and store in an output.
        """
        self.set(arg3, self.get(arg1) * self.get(arg2))
        return False

    def get_input(self, arg1):
        """
        Store an input value.
        """
        if self.inputter is None:
            raise ValueError("This program requires an inputter")
        self.set(arg1, self.inputter())
        return False

    def put_output(self, arg1):
        """
        Output a value.
        """
        if self.outputter is None:
            raise ValueError("This program requires an outputter")
        self.outputter(self.get(arg1))
        return False

    def jump_if_true(self, arg1, arg2):
        """
        Jump based on the value of an argument.
        """
        if self.get(arg1) != 0:
            self.ipointer = self.get(arg2)
            return True
        return False

    def jump_if_false(self, arg1, arg2):
        """
        Jump based on the value of an argument.
        """
        if self.get(arg1) == 0:
            self.ipointer = self.get(arg2)
            return True
        return False

    def less(self, arg1, arg2, arg3):
        """
        Compare two numbers and store in an output.
        """
        self.set(arg3, int(self.get(arg1) < self.get(arg2)))
        return False

    def equals(self, arg1, arg2, arg3):
        """
        Compare two numbers and store in an output.
        """
        self.set(arg3, int(self.get(arg1) == self.get(arg2)))
        return False

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
        Execute the current instruction. Returns whether to coninute executing or not.
        """
        instruction = str(self.memory[self.ipointer])
        args = self.memory[self.ipointer + 1 :]
        opcode_value = int(instruction[-2:])
        param_modes = list(reversed([int(mode) for mode in instruction[:-2]]))
        if opcode_value == 99:
            return False
        opcode = self.opcodes[opcode_value]
        param_modes = param_modes + [0] * (opcode.arg_count - len(param_modes))
        if not opcode.action(*list(zip(param_modes, args))):
            self.ipointer = self.ipointer + opcode.arg_count + 1
        return True

    def run(self, opcodes):
        """
        Run a list of opcodes.
        """
        self.memory = opcodes.copy()
        while self.step():
            pass
        return self.memory[0]
