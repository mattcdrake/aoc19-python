class IntcodeComputer:
    def __init__(self, program):
        self.program = program
        self.pc = 0
        self.relative_base = 0

    def get_opcode(self, value):
        return value % 100

    # Chop off the opcode and return a list of the parameter mode values. Pads the
    # list with 0 for parameter modes.
    def get_param_modes(self, value, opcode):
        value = value // 100
        param_modes = [int(i) for i in str(value)]
        while len(param_modes) < 3:
            param_modes.insert(0, 0)
        if opcode == 3:
            param_modes[2] = 1
        if opcode in (1, 2, 7, 8):
            param_modes[0] = 1
        return param_modes

    def get_arg(self, mode, pc_offset):
        if mode == 0:
            return self.program[self.program[self.pc+pc_offset]]
        elif mode == 1:
            return self.program[self.pc+pc_offset]
        elif mode == 2:
            return self.program[self.pc+self.relative_base+pc_offset]

    # Returns a list of 3 arguments that have been processed according to parameter
    # mode rules.
    def parse_args(self, opcode, param_modes):
        args = [0, 0, 0]

        # Opcodes w/ 1 arg
        if opcode == 3:
            args[0] = self.get_arg(param_modes[2], 1)
        elif opcode == 4:
            args[0] = self.get_arg(param_modes[2], 1)
        # Opcodes w/ 2 or 3 args
        elif opcode in (1, 2, 5, 6, 7, 8):
            args[0] = self.get_arg(param_modes[2], 1)
            args[1] = self.get_arg(param_modes[1], 2)
            # Opcodes w/ 3 args
            if opcode in (1, 2, 7, 8):
                args[2] = self.get_arg(param_modes[0], 3)

        return args

    """
    compute(self, inputs)

    @arg inputs - list of inputs that will be polled sequentially
    @return tuple of (output, stopping code)

    Stopping codes are "halt" for final computation, "output" for TTY output
    TODO put opcode calls into their own functions
    """

    def compute(self, inputs):
        cur_input = 0
        opcode_raw = self.program[self.pc]
        opcode = self.get_opcode(opcode_raw)
        param_modes = self.get_param_modes(opcode_raw, opcode)

        while opcode != 99:
            args = self.parse_args(opcode, param_modes)
            # Execute opcode
            if opcode == 1:
                self.program[args[2]] = args[0] + args[1]
                self.pc += 4
            elif opcode == 2:
                self.program[args[2]] = args[0] * args[1]
                self.pc += 4
            # Input instruction
            elif opcode == 3:
                self.program[args[0]] = inputs[cur_input]
                cur_input += 1
                self.pc += 2
            # Output instruction
            elif opcode == 4:
                self.pc += 2
                return(args[0], "output")
            elif opcode == 5:
                if args[0] != 0:
                    self.pc = args[1]
                else:
                    self.pc += 3
            elif opcode == 6:
                if args[0] == 0:
                    self.pc = args[1]
                else:
                    self.pc += 3
            elif opcode == 7:
                if args[0] < args[1]:
                    self.program[args[2]] = 1
                else:
                    self.program[args[2]] = 0
                self.pc += 4
            elif opcode == 8:
                if args[0] == args[1]:
                    self.program[args[2]] = 1
                else:
                    self.program[args[2]] = 0
                self.pc += 4
            elif opcode == 9:
                self.relative_base += args[0]

            # Get new opcodes
            opcode_raw = self.program[self.pc]
            opcode = self.get_opcode(opcode_raw)
            param_modes = self.get_param_modes(opcode_raw, opcode)

        return (self.program[0], "halt")
