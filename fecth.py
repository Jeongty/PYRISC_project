from fondi import *


class fecth(object):

    def __init__(self):
        self.IMEM = Memory(IMEM_START, IMEM_SIZE, WORD_SIZE)
        pass

    def pc_2_instr(self, pc):
        instr = self.IMEM.access(1, pc, 0, 0)

        return instr
    
    def risc_log(self, instr):
        op = fecth.opcode(instr)
        if op == 3:
            tpe = 'I'
        elif op == 35:
            tpe = 'S'
        elif op == 51:
            tpe = 'R'
        elif op == 19:
            tpe = 'I'
        elif op == 23:
            tpe = 'U'
        elif op == 55:
            tpe = 'U'
        elif op == 99:
            tpe = 'B'
        elif op == 103:
            tpe = 'J'
        elif op == 111:
            tpe = 'I'
        else:
            tpe = 'E'
        return tpe
    
    @staticmethod
    def opcode(instr):
        return (instr & OP_MASK) >> OP_SHIFT
    
    @staticmethod
    def func3(instr):
        return (instr & FUNCT3_MASK) >> FUNCT3_SHIFT
    
    @staticmethod
    def func7(instr):
        return (instr & FUNCT7_MASK) >> FUNCT7_SHIFT
    
    @staticmethod
    def rs1(instr):
        return (instr & RS1_MASK) >> RS1_SHIFT
    
    @staticmethod
    def rs2(instr):
        return (instr & RS2_MASK) >> RS2_SHIFT
    
    @staticmethod
    def rd(instr):
        return (instr & RD_MASK) >> RD_SHIFT