from fondi import *
from alu import *

class datapath(object):
    def __init__(self):
        self.DMEM       = Memory(DMEM_START, DMEM_SIZE, WORD_SIZE)
        self.rf         = RegisterFile()
        self.alu        = alu()
        self.pc_adder   = adder()
        self.pc_plus4   = WORD(0x10000004)
        self.rs1 = 0
        self.rs2 = 0
        self.immsrc = 0
        self.instr = 0
        self.pc = WORD(0x10000000)
        self.alusrca = 0
        self.alusrcb = 0
        self.alusrc = 0
        self.func3 = 0
        self.memwrite = 0
        self.resultsrc = 0
        self.rd = 0
        self.branch = 0
        self.jump = 0
        pass

    def input(self, pc, instr, op, f3, rs1, rs2, rd, regs, imms, alua, alub, mems, res, br, alus, jump):
        self.pc         = pc
        self.instr      = instr
        self.op         = op
        self.func3      = f3
        self.rs1        = rs1
        self.rs2        = rs2
        self.rd         = rd
        
        self.alusrc     = alus
        self.regwrite   = regs
        self.immsrc     = imms
        self.alusrca    = alua
        self.alusrcb    = alub
        self.memwrite   = mems
        self.resultsrc  = res
        self.branch     = br
        self.jump       = jump

    def update(self):
        self.ex()
        self.mem()
        self.wb()
        self.pcs = self.pc_src()
        self.pc_next = self.branch_logic(self.pcs)

    def pc_src(self):
        if self.branch == 1:
            if self.func3 == 0: #beq
                pcsrc = 1 if(self.srca == self.srcb) else 0
            elif self.func3 == 1: #bne
                pcsrc = 1 if(self.srca != self.srcb) else 0
            elif self.func3 == 4: #blt
                pcsrc = 1 if(SWORD(self.srca) < SWORD(self.srcb)) else 0
            elif self.func3 == 5: #bge
                pcsrc = 1 if(SWORD(self.srca) >= SWORD(self.srcb)) else 0
            elif self.func3 == 6: #bltu
                pcsrc = 1 if(WORD(self.srca) < WORD(self.srcb)) else 0
            elif self.func3 == 7: #bgeu
                pcsrc = 1 if(WORD(self.srca) >= WORD(self.srcb)) else 0    
        elif self.jump == 1:
            if self.op == 111: #JAL
                pcsrc = 1
            elif self.op == 103: #JALR
                pcsrc = 2
            else:
                pcsrc = 0
        else:
            pcsrc = 0

        return pcsrc

    def branch_logic(self, pcsrc):
        
        self.pc_plus4 = self.pc_adder.op(self.pc, 4)
        self.pc_target = WORD(self.pc + self.imm)
        
        next_pc = datapath.mux3(self.pc_plus4, self.pc_target, WORD(self.aluresult), pcsrc)

        return next_pc
    
    def ex(self):
        #-Register File---------------------------------------------------------
        #Read
        self.rd1 = self.rf.read(self.rs1)
        self.rd2 = self.rf.read(self.rs2)
        #extend-----------------------------------------------------------------
        self.imm = datapath.extend(self.immsrc, self.instr)
        #srca-------------------------------------------------------------------
        self.srca = datapath.mux3(self.rd1, self.pc, 0, self.alusrca)
        #srcb-------------------------------------------------------------------
        self.srcb = datapath.mux2(self.rd2, self.imm, self.alusrcb)
        #ALU--------------------------------------------------------------------
        self.aluresult = self.alu.op(self.srca, self.srcb, self.alusrc)


    def mem(self): #be_logic
        self.wdata  = self.rd2
        daddr       = self.aluresult & ADDR_MASK
        add_last    = self.aluresult & ADDL_MASK

        if self.func3 == 0: #sb
            if add_last == 0:
                self.be_wd = (self.wdata & BYTE0_MASK)
            elif add_last == 1:
                self.be_wd = (self.wdata & BYTE0_MASK) << 8
            elif add_last == 2:
                self.be_wd = (self.wdata & BYTE0_MASK) << 16
            elif add_last == 3:
                self.be_wd = (self.wdata & BYTE0_MASK) << 24
        elif self.func3 == 1: #sh
            if add_last == 0 or add_last == 1:
                self.be_wd = (self.wdata & HALF0_MASK)
            elif add_last == 2 or add_last == 3:
                self.be_wd = (self.wdata & HALF0_MASK) << 16
        elif self.func3 == 2:
            self.be_wd = self.wdata
        else:
            self.be_wd = 0

        self.DMEM.access(self.memwrite, daddr, self.be_wd, 1)

    def wb(self): #be_logic
        add_last = self.aluresult & ADDL_MASK
        daddr    = self.aluresult & ADDR_MASK
        #load
        self.rdata, dump = self.DMEM.access(1, daddr, 0, 0)
        if self.func3 == 0: #lb
            if add_last == 0:
                self.be_rd = (self.rdata & BYTE0_MASK)
                self.be_rd = datapath.sign_extend(self.be_rd, 8)
            elif add_last == 1:
                self.be_rd = (self.rdata & BYTE1_MASK) >> 8
                self.be_rd = datapath.sign_extend(self.be_rd, 8)
            elif add_last == 2:
                self.be_rd = (self.rdata & BYTE2_MASK) >> 16
                self.be_rd = datapath.sign_extend(self.be_rd, 8)
            elif add_last == 3:
                self.be_rd = (self.rdata & BYTE3_MASK) >> 24
                self.be_rd = datapath.sign_extend(self.be_rd, 8)
        elif self.func3 == 1: #lh
            if (add_last == 0) or (add_last == 1):
                self.be_rd = (self.rdata & HALF0_MASK)
                self.be_rd = datapath.sign_extend(self.be_rd, 16)
            elif (add_last == 2) or (add_last == 3):
                self.be_rd = (self.rdata & HALF1_MASK) >> 16
                self.be_rd = datapath.sign_extend(self.be_rd, 16)
        elif self.func3 == 2: #lw
            self.be_rd = self.rdata
        elif self.func3 == 4: #lbu
            if add_last == 0:
                self.be_rd = (self.rdata & BYTE0_MASK) >> 0
            elif add_last == 1:
                self.be_rd = (self.rdata & BYTE1_MASK) >> 8
            elif add_last == 2:
                self.be_rd = (self.rdata & BYTE2_MASK) >> 16
            elif add_last == 3:
                self.be_rd = (self.rdata & BYTE3_MASK) >> 24
        elif self.func3 == 5: #lhu
            if (add_last == 0) or (add_last == 1):
                self.be_rd = (self.rdata & HALF0_MASK)
            elif (add_last == 2) or (add_last == 3):
                self.be_rd = (self.rdata & HALF1_MASK) >> 16

        self.result = datapath.mux3(self.aluresult, self.be_rd, self.pc_plus4, self.resultsrc)

        self.rf.write(self.rd, self.result)
        
    @staticmethod
    def mux3(in0, in1, in2, sel):
        if sel == 0:
            out = in0
        elif sel == 1:
            out = in1
        elif sel == 2:
            out = in2
        else:
            pass
        
        return out
    
    @staticmethod
    def mux2(in0, in1, sel):
        return in0 if sel == 0 else in1
    
    @staticmethod
    def sign_extend(v, n):
        if v >> (n - 1):
            return ((1 << (32 - n)) - 1) << n | v
        else:
            return v
        
    @staticmethod
    def extend(immsrc, instr):
        if immsrc == 0:
            output = datapath.imm_i(instr)
        elif immsrc == 1:
            output = datapath.imm_s(instr)
        elif immsrc == 2:
            output = datapath.imm_b(instr)
        elif immsrc == 3:
            output = datapath.imm_j(instr)
        elif immsrc == 4:
            output  = datapath.imm_u(instr)
        return output
    
    @staticmethod
    def imm_i(inst):
        imm     = (inst >> 20) & 0xfff
        return datapath.sign_extend(imm, 12)

    @staticmethod
    def imm_u(inst):
        return inst & 0xfffff000

    @staticmethod
    def imm_s(inst):
        imm     = ((inst >> 25) & 0x7f) << 5
        imm     |= ((inst >> 7) & 0x1f)
        return datapath.sign_extend(imm, 12) 

    @staticmethod
    def imm_b(inst):
        imm     = (inst >> 31) << 11
        imm     |= ((inst >> 7) & 1) << 10
        imm     |= ((inst >> 25) & 0x3f) << 4
        imm     |= (inst >> 8) & 0xf 
        imm     = imm << 1
        return datapath.sign_extend(imm, 13)

    @staticmethod
    def imm_j(inst):
        imm     = (inst >> 31) << 19
        imm     |= ((inst >> 12) & 0xff) << 11
        imm     |= ((inst >> 20) & 1) << 10
        imm     |= (inst >> 21) & 0x3ff
        imm     = imm << 1
        return datapath.sign_extend(imm, 21)