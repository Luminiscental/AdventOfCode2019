"""Module for the Intcode interpretor."""
import collections

OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LESS = 7
OP_EQ = 8
OP_SHIFT = 9
OP_HALT = 99

REFERENCE_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2


class Interpretor:
    """Class for intcode interpretors."""

    def __init__(self, input_from=None):
        self.memory = collections.defaultdict(int)
        self.relative_base = 0
        self.input_queue = collections.deque()
        self.input_func = input_from
        self.instr_idx = 0

    def reset(self):
        """Reset memory and state."""
        self.memory.clear()
        self.relative_base = 0
        self.input_queue.clear()
        self.instr_idx = 0

    def load_program(self, program):
        """Load a program into the start of memory."""
        for idx, val in enumerate(program):
            self.memory[idx] = val

    def queue_input(self, value):
        """Queue a value to give as input."""
        self.input_queue.append(value)

    def queue_inputs(self, iterable):
        """Queue an iterable sequence of values to give as input."""
        self.input_queue.extend(iterable)

    def run(self, program, group=1):
        """Run a program, returns a generator which yields output values."""
        output_queue = []
        self.load_program(program)
        while True:
            instr = self.memory[self.instr_idx]
            operation = instr % 100
            parameter_modes = instr // 100
            if operation == OP_ADD:
                self._add(parameter_modes)
            elif operation == OP_MUL:
                self._mul(parameter_modes)
            elif operation == OP_INPUT:
                self._load_input(parameter_modes)
            elif operation == OP_OUTPUT:
                yield from self._get_output(parameter_modes, output_queue, group)
            elif operation == OP_JUMP_IF_TRUE:
                self._jump_if_true(parameter_modes)
            elif operation == OP_JUMP_IF_FALSE:
                self._jump_if_false(parameter_modes)
            elif operation == OP_LESS:
                self._less(parameter_modes)
            elif operation == OP_EQ:
                self._eq(parameter_modes)
            elif operation == OP_SHIFT:
                self._shift(parameter_modes)
            elif operation == OP_HALT:
                break
            else:
                raise ValueError(f"Unknown opcode {operation}")

    def _set(self, loc, val):
        idx, mode = loc
        if mode == REFERENCE_MODE:
            self.memory[idx] = val
        elif mode == IMMEDIATE_MODE:
            raise ValueError("Cannot write in immediate mode")
        elif mode == RELATIVE_MODE:
            self.memory[self.relative_base + idx] = val
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def _get(self, loc):
        idx, mode = loc
        if mode == REFERENCE_MODE:
            return self.memory[idx]
        if mode == IMMEDIATE_MODE:
            return idx
        if mode == RELATIVE_MODE:
            return self.memory[self.relative_base + idx]
        raise ValueError(f"Unknown parameter mode {mode}")

    def _add(self, parameter_modes):
        in1 = self.memory[self.instr_idx + 1], parameter_modes % 10
        in2 = self.memory[self.instr_idx + 2], parameter_modes // 10 % 10
        out = self.memory[self.instr_idx + 3], parameter_modes // 100 % 10
        self.instr_idx += 4
        self._set(out, self._get(in1) + self._get(in2))

    def _mul(self, parameter_modes):
        in1 = self.memory[self.instr_idx + 1], parameter_modes % 10
        in2 = self.memory[self.instr_idx + 2], parameter_modes // 10 % 10
        out = self.memory[self.instr_idx + 3], parameter_modes // 100 % 10
        self.instr_idx += 4
        self._set(out, self._get(in1) * self._get(in2))

    def _load_input(self, parameter_modes):
        out = self.memory[self.instr_idx + 1], parameter_modes % 10
        self.instr_idx += 2
        val = self.input_queue.popleft() if self.input_queue else self.input_func()
        self._set(out, val)

    def _get_output(self, parameter_modes, output_queue, group):
        out = self.memory[self.instr_idx + 1], parameter_modes % 10
        self.instr_idx += 2
        output = self._get(out)
        if group == 1:
            yield output
        else:
            output_queue.append(output)
            if len(output_queue) == group:
                yield tuple(output_queue)
                output_queue.clear()

    def _jump_if_true(self, parameter_modes):
        cond = self.memory[self.instr_idx + 1], parameter_modes % 10
        targ = self.memory[self.instr_idx + 2], parameter_modes // 10 % 10
        self.instr_idx += 3
        if self._get(cond) != 0:
            self.instr_idx = self._get(targ)

    def _jump_if_false(self, parameter_modes):
        cond = self.memory[self.instr_idx + 1], parameter_modes % 10
        targ = self.memory[self.instr_idx + 2], parameter_modes // 10 % 10
        self.instr_idx += 3
        if self._get(cond) == 0:
            self.instr_idx = self._get(targ)

    def _less(self, parameter_modes):
        in1 = self.memory[self.instr_idx + 1], parameter_modes % 10
        in2 = self.memory[self.instr_idx + 2], parameter_modes // 10 % 10
        out = self.memory[self.instr_idx + 3], parameter_modes // 100 % 10
        self.instr_idx += 4
        self._set(out, int(self._get(in1) < self._get(in2)))

    def _eq(self, parameter_modes):
        in1 = self.memory[self.instr_idx + 1], parameter_modes % 10
        in2 = self.memory[self.instr_idx + 2], parameter_modes // 10 % 10
        out = self.memory[self.instr_idx + 3], parameter_modes // 100 % 10
        self.instr_idx += 4
        self._set(out, int(self._get(in1) == self._get(in2)))

    def _shift(self, parameter_modes):
        offset = self.memory[self.instr_idx + 1], parameter_modes % 10
        self.instr_idx += 2
        self.relative_base += self._get(offset)
