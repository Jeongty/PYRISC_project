from fondi import *

from fecth import *
from controller import *
from datapath import *

class pyriscv(object):
    def __init__(self):
        self.pci = fecth()
        self.con = controller()
        self.dp = datapath()
        pass

    def run(self, pc):
        #-----------------------------------------------------------------------
        #PC_DECODER
        instr, dum = self.pci.pc_2_instr(pc)

        self.op = fecth.opcode(instr)
        self.f3 = fecth.func3(instr)
        self.f7 = fecth.func7(instr)
        self.rs1 = fecth.rs1(instr)
        self.rs2 = fecth.rs2(instr)
        self.rd = fecth.rd(instr)
        #-----------------------------------------------------------------------
        # Controller        
        self.con.input(self.op, self.f3, self.f7) 
        self.con.update()
        #-----------------------------------------------------------------------
        # Datapath
        self.dp.input(pc, instr, self.op, self.f3, self.rs1, self.rs2, self.rd, self.con.regwirte, self.con.immsrc, 
                      self.con.alusrca, self.con.alusrcb, self.con.memwirte, self.con.resultsrc, self.con.branch, self.con.alusrc, self.con.jump)
        self.dp.update()

        next_pc = self.dp.pc_next

        return next_pc

    def reset_cpu(self):
        pc = WORD(0x10000000)
        instr = WORD(0x00000033)

        self.op = fecth.opcode(instr)
        self.f3 = fecth.func3(instr)
        self.f7 = fecth.func7(instr)
        self.rs1 = fecth.rs1(instr)
        self.rs2 = fecth.rs2(instr)
        self.rd = fecth.rd(instr)
        #-----------------------------------------------------------------------
        # Controller        
        self.con.input(self.op, self.f3, self.f7) 
        self.con.update()
        #-----------------------------------------------------------------------
        # Datapath
        for i in range(0,31):
            self.dp.rf.write(i,0)

        self.dp.input(pc, instr, self.op, self.f3, self.rs1, self.rs2, self.rd, self.con.regwirte, self.con.immsrc, 
                      self.con.alusrca, self.con.alusrcb, self.con.memwirte, self.con.resultsrc, self.con.branch, self.con.alusrc, self.con.jump)
        self.dp.update()

