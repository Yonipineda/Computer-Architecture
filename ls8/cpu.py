"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.address = [0] * 256 # where an 8-bit is stored 
        self.reg = [0b0] * 8 # 8-bit register 
        self.ir = None # `IR`: Instruction Register, contains a copy of the currently executing instruction
        self.mar = None  # `MAR`: Memory Address Register, holds the memory address we're reading or writing
        self.mdr = None # `MDR`: Memory Data Register, holds the value to write or the value just read
        self.fl = None # `FL`: Flags, see below
        self.pc = 0 # program counter: address of current executing counter 
        self.spl = None # stack pointer location 
        self.ram = [0b0] * 0xF4

    def load(self, filename: str):
        """Load a program into memory."""

        

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        try:
            with open(filename, 'r') as file:
                lines = (line for line in file.readlines() if not (line[0]=='#' or line[0]=='\n'))
                program = [int(line.split('#')[0].strip(), 2) for line in lines]

            address = 0


            for instruction in program:
                self.ram[address] = instruction
                address += 1

        except FileNotFoundError as error:
            print(error)
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        pass

    
    def ram_read(self, mar):
        return self.ram[mar] 

    def ram_write(self, mar, mdr):
        self.ram[mar] = self.mdr