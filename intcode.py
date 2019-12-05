"""
Modulee for the Intcode interpretor.
"""


class Interpretor:
    """
    An intcode interpretor.
    """

    def __init__(self, inputter=None, outputter=None):
        self.memory = []
        self.ipointer = 0
        self.inputter = inputter
        self.outputter = outputter

    def get(self, mode, idx):
        """
        Get a value from its parameter mode and index.
        """
        if mode == 0:
            return self.memory[idx]
        if mode == 1:
            return idx
        raise ValueError("Unknown parameter mode " + str(mode))

    def set(self, mode, idx, value):
        """
        Set a value from its parameter mode and index.
        """
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
        opcode = int(instruction[-2:])
        param_modes = list(reversed([int(mode) for mode in instruction[:-2]]))
        if opcode == 1:
            param_modes = param_modes + [0] * (3 - len(param_modes))
            lhs = self.get(param_modes[0], args[0])
            rhs = self.get(param_modes[1], args[1])
            self.set(param_modes[2], args[2], lhs + rhs)
            self.ipointer = self.ipointer + 4
        elif opcode == 2:
            param_modes = param_modes + [0] * (3 - len(param_modes))
            lhs = self.get(param_modes[0], args[0])
            rhs = self.get(param_modes[1], args[1])
            self.set(param_modes[2], args[2], lhs * rhs)
            self.ipointer = self.ipointer + 4
        elif opcode == 3:
            param_modes = param_modes + [0] * (1 - len(param_modes))
            if self.inputter is None:
                raise ValueError("Interpretor requires an inputter to run this code")
            self.set(param_modes[0], args[0], self.inputter())
            self.ipointer = self.ipointer + 2
        elif opcode == 4:
            param_modes = param_modes + [0] * (1 - len(param_modes))
            if self.outputter is None:
                raise ValueError("Interpretor requires an outputter to run this code")
            self.outputter(self.get(param_modes[0], args[0]))
            self.ipointer = self.ipointer + 2
        elif opcode == 99:
            return False
        else:
            raise ValueError("Unknown opcode " + str(opcode))
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
