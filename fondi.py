import numpy as np

#--------------------------------------------------------------------------
#   Data types & basic constants
#--------------------------------------------------------------------------

WORD                = np.uint32
SWORD               = np.int32

Y                   = True
N                   = False

#--------------------------------------------------------------------------
#   RISC-V constants
#--------------------------------------------------------------------------

WORD_SIZE           = 4
NUM_REGS            = 32

OP_MASK             = WORD(0x0000007f)
OP_SHIFT            = 0
RD_MASK             = WORD(0x00000f80)
RD_SHIFT            = 7
FUNCT3_MASK         = WORD(0x00007000)
FUNCT3_SHIFT        = 12
RS1_MASK            = WORD(0x000f8000)
RS1_SHIFT           = 15
RS2_MASK            = WORD(0x01f00000)
RS2_SHIFT           = 20
FUNCT7_MASK         = WORD(0xfe000000)
FUNCT7_SHIFT        = 25

#--------------------------------------------------------------------------
#   Type constants
#--------------------------------------------------------------------------

S_TYPE  = 35
R_TYPE  = 51
B_TYPE  = 99
J_TYPE  = 111
I_TYPE  = 3 | 19 | 103 # load | alu | jalr
U_TYPE  = 23 | 55 #auipc | lui

#--------------------------------------------------------------------------
#   ALU constants
#--------------------------------------------------------------------------

ALU_ADD     = 0
ALU_SUB     = 1
ALU_SLL     = 2
ALU_SRL     = 3
ALU_SRA     = 4
ALU_XOR     = 5
ALU_OR      = 6
ALU_AND     = 7
ALU_SLT     = 8
ALU_SLTU    = 9

#--------------------------------------------------------------------------
#   Memory constrants
#--------------------------------------------------------------------------

IMEM_START  = WORD(0x10000000) #Instruction Mem
IMEM_SIZE   = WORD(64 * 1024)

DMEM_START  = WORD(0x80000000) #Data Mem
DMEM_SIZE   = WORD(64 * 1024)

BYTE0_MASK  = WORD(0x000000ff)
BYTE1_MASK  = WORD(0x0000ff00)
BYTE2_MASK  = WORD(0x00ff0000)
BYTE3_MASK  = WORD(0xff000000)

HALF0_MASK  = WORD(0x0000ffff)
HALF1_MASK  = WORD(0xffff0000)

ADDL_MASK    = WORD(0x00000003)
ADDR_MASK   = WORD(0xfffffffc)

#--------------------------------------------------------------------------
#   csignal[CS_MEM_FCN]: Memory function type signal
#--------------------------------------------------------------------------

M_XRD               = 0         # load
M_XWR               = 1         # store
M_X                 = 0

#--------------------------------------------------------------------------
#   Constants
#--------------------------------------------------------------------------

# Symbolic register names
rname =  [ 
            'zero', 'ra',  'sp',  'gp',  'tp',  't0',  't1',  't2',
            's0',   's1',  'a0',  'a1',  'a2',  'a3',  'a4',  'a5',
            'a6',   'a7',  's2',  's3',  's4',  's5',  's6',  's7',
            's8',   's9',  's10', 's11', 't3',  't4',  't5',  't6' 
        ]


#--------------------------------------------------------------------------
#   RegisterFile: models 32-bit RISC-V register file
#--------------------------------------------------------------------------

class RegisterFile(object):

    def __init__(self):
        self.reg = WORD([0] * NUM_REGS)

    def read(self, regno):

        if regno == 0:
            return 0
        elif regno > 0 and regno < NUM_REGS:
            return self.reg[regno]
        else:
            raise ValueError

    def write(self, regno, value):

        if regno == 0:
            return
        elif regno > 0 and regno < NUM_REGS:
            self.reg[regno] = WORD(value)
        else:
            raise ValueError

    def dump(self, columns = 4):

        print("Registers")
        print("=" * 9)
        for c in range (0, NUM_REGS, columns):
            str = ""
            for r in range (c, min(NUM_REGS, c + columns)):
                name = rname[r]
                val = self.reg[r]
                str += "%-11s0x%08x    " % ("%s ($%d):" % (name, r), val)
            print(str)


#--------------------------------------------------------------------------
#   Register: models a single 32-bit register
#--------------------------------------------------------------------------

class Register(object):

    def __init__(self, initval = 0):
        self.r = WORD(initval)

    def read(self):
        return self.r

    def write(self, val):
        self.r = WORD(val)



#--------------------------------------------------------------------------
#   Memory: models a memory
#--------------------------------------------------------------------------

class Memory(object):

    def __init__(self, mem_start, mem_size, word_size):
        self.word_size  = word_size
        self.mem_words  = mem_size // word_size
        self.mem_start  = mem_start
        self.mem_end    = mem_start + mem_size
        self.mem        = WORD([0] * self.mem_words)

    def access(self, valid, addr, data, fcn):

        if (not valid):                    
            res = ( WORD(0), True )
        elif (addr < self.mem_start) or (addr >= self.mem_end) or \
            addr % self.word_size != 0:
            res = ( WORD(0) , False )
        elif fcn == M_XRD:
            val = self.mem[(addr - self.mem_start) // self.word_size]
            res = ( val, True )
        elif fcn == M_XWR:
            self.mem[(addr - self.mem_start) // self.word_size] = WORD(data) 
            res = ( WORD(0), True )
        else:
            res = ( WORD(0), False )

        return res

    def dump(self, skipzero = False):

        print("Memory 0x%08x - 0x%08x" % (self.mem_start, self.mem_end - 1))
        print("=" * 30)
        for a in range(self.mem_start, self.mem_end, self.word_size):
            val, status = self.access(True, a, 0, M_XRD)
            if not status:
                continue
            if (not skipzero) or (val != 0):
                print("0x%08x: " % a, ' '.join("%02x" % ((val >> i) & 0xff) for i in [0, 8, 16, 24]), " (0x%08x)" % val)
