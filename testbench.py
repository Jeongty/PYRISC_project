import os
import sys

from fondi import *
from testprogram import *

from pyriscv import *

class test(object):
    def __init__(self):
        self.cpu = pyriscv()
        self.cnt = 0
        pass

    def run(self):
        r = 0
        ia = 0
        il = 0
        s = 0
        u = 0
        j = 0
        ij = 0
        b = 0

        if(1):
            print('-----------------------------------------------------------------------')
            print('R_TYPE\n')
            self.r_type()
            r = 1
        if(1):
            print('-----------------------------------------------------------------------')
            print('I_TYPE(ALU)\n')
            self.i_type_alu()
            ia = 1
        if(1):
            print('-----------------------------------------------------------------------')
            print('I_TYPE(LOADS)\n')
            self.i_type_load()
            il = 1
        if(1):
            print('-----------------------------------------------------------------------')
            print('S_TYPE\n')
            self.s_type()
            s = 1
        if(1):
            print('-----------------------------------------------------------------------')
            print('U_TYPE\n')
            self.u_type()
            u = 1
        if(1):
            print('-----------------------------------------------------------------------')
            print('J_TYPE\n')
            self.j_type()
            j = 1
        if(1):
            print('-----------------------------------------------------------------------')
            print('I_TYPE(JALR)\n')
            self.i_type_jalr()
            ij = 1
        if(1):
            print('-----------------------------------------------------------------------')
            print('B_TYPE\n')
            self.b_type()
            b = 1

        print('-----------------------------------------------------------------------')
        print('TEST RESULT')
        if r == 1:
            print('R_TYPE \t\tPASSED')
        else:
            print('R_TYPE \t\tFAILED')
        if ia == 1:
            print('I_TYPE(ALU) \tPASSED')
        else:
            print('I_TYPE(ALU) \tFAILED')
        if il == 1:
            print('I_TYPE(LOADS) \tPASSED')
        else:
            print('I_TYPE(LOADS) \tFAILED')
        if s == 1:
            print('S_TYPE \t\tPASSED')
        else:
            print('S_TYPE \t\tFAILED')
        if u == 1:
            print('U_TYPE \t\tPASSED')
        else:
            print('U_TYPE \t\tFAILED')
        if j == 1:
            print('J_TYPE \t\tPASSED')
        else:
            print('J_TYPE \t\tFAILED')
        if ij == 1:
            print('I_TYPE(JALR) \tPASSED')
        else:
            print('I_TYPE(JALR) \tFAILED')
        if b == 1:
            print('B_TYPE \t\tPASSED')
        else:
            print('B_TYPE \t\tFAILED')
        
        print('-----------------------------------------------------------------------')
        if r and ia and il and s and u and j and ij and b == 1:
            print('########################## All Test Passed!! ##########################')


    def reset_pc(self):
        return WORD(0x10000000), 0
    
    def check_result_rf(self, rd, value, tpe):    
        if self.cpu.dp.rf.read(rd) == value:
            self.cnt = self.cnt + 1
            print('[#',self.cnt,']TEST \t' , tpe, 'passed!')
        else:
            print('[#',self.cnt,']TEST \t' , tpe, 'failed! expect: 0x%08x got: 0x%08x' %(value, self.cpu.dp.rf.read(rd)))
            print('\tTEST FAILED')
            sys.exit()

    def check_result_mem(self, addr, value, tpe):
        data, dump = self.cpu.dp.DMEM.access(1, WORD(addr), 0, 0)
        
        if data == value:
            self.cnt = self.cnt + 1
            print('[#',self.cnt,']TEST \t' , tpe, 'passed!')
        else:
            print('[#',self.cnt,']TEST \t' , tpe, 'failed! expect: 0x%08x got: 0x%08x' %(value, data))
            print('\tTEST FAILED')
            sys.exit()

    def r_type(self):
        reg_pc, i = self.reset_pc()
        op = R_TYPE

        rs1 = 1
        rd1 = -100
        rs2 = 2
        rd2 = 200

        self.cpu.dp.rf.write(rs1, WORD(rd1))
        self.cpu.dp.rf.write(rs2, WORD(rd2))

        pyrs1   = rs1 << RS1_SHIFT
        pyrs2   = rs2 << RS2_SHIFT

        in_add  = op + (3 << RD_SHIFT) + FUNC3_ADD  + pyrs1 + pyrs2 + FUNC7_0
        in_sub  = op + (4 << RD_SHIFT) + FUNC3_ADD  + pyrs1 + pyrs2 + FUNC7_1
        in_xor  = op + (5 << RD_SHIFT) + FUNC3_XOR  + pyrs1 + pyrs2 + FUNC7_0
        in_or   = op + (6 << RD_SHIFT) + FUNC3_OR   + pyrs1 + pyrs2 + FUNC7_0
        in_and  = op + (7 << RD_SHIFT) + FUNC3_AND  + pyrs1 + pyrs2 + FUNC7_0
        in_sll  = op + (8 << RD_SHIFT) + FUNC3_SLL  + pyrs1 + pyrs2 + FUNC7_0
        in_srl  = op + (9 << RD_SHIFT) + FUNC3_SRL  + pyrs1 + pyrs2 + FUNC7_0
        in_sra  = op + (10 << RD_SHIFT) + FUNC3_SRL  + pyrs1 + pyrs2 + FUNC7_1
        in_slt  = op + (11 << RD_SHIFT) + FUNC3_SLT  + pyrs1 + pyrs2 + FUNC7_0
        in_sltu = op + (12 << RD_SHIFT) + FUNC3_SLTU + pyrs1 + pyrs2 + FUNC7_0

        self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_add), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_sub), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 8), WORD(in_xor), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 12), WORD(in_or) , 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 16), WORD(in_and), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 20), WORD(in_sll), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 24), WORD(in_srl), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 28), WORD(in_sra), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 32), WORD(in_slt), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 36), WORD(in_sltu), 1)

        for i in range (3,13):
            next_pc= self.cpu.run(reg_pc) 
            
            if i == 3:
                self.check_result_rf(i, WORD(0x64), "R-Type ADD")
            elif i == 4:
                self.check_result_rf(i, WORD(0xfffffed4), "R-Type SUB")
            elif i == 5:
                self.check_result_rf(i, WORD(0xffffff54), "R-Type XOR")
            elif i == 6:
                self.check_result_rf(i, WORD(0xffffffdc), "R-Type OR")
            elif i == 7:
                self.check_result_rf(i, WORD(0x00000088), "R-Type AND")
            elif i == 8:
                self.check_result_rf(i, WORD(0xffff9c00), "R-Type SLL")
            elif i == 9:
                self.check_result_rf(i, WORD(0x00ffffff), "R-Type SRL")
            elif i == 10:
                self.check_result_rf(i, WORD(0xffffffff), "R-Type SLA")
            elif i == 11:
                self.check_result_rf(i, WORD(0x1), "R-Type SLT")
            elif i == 12:
                self.check_result_rf(i, WORD(0x0), "R-Type SLTU")
            reg_pc = next_pc
        
        dump = self.cpu.run(reg_pc)

    def i_type_alu(self):
        reg_pc, i = self.reset_pc()
        op = I_TYPE_ALU

        rs1 = 1
        rd1 = -100
        imm = 200
        sht = 20

        self.cpu.dp.rf.write(rs1, WORD(rd1))

        pyrs1   = rs1 << RS1_SHIFT
        pyimm   = imm << RS2_SHIFT
        pysht   = sht << RS2_SHIFT

        in_addi  = op + (3 << RD_SHIFT) + FUNC3_ADD  + pyrs1 + pyimm
        in_xori  = op + (4 << RD_SHIFT) + FUNC3_XOR  + pyrs1 + pyimm
        in_ori   = op + (5 << RD_SHIFT) + FUNC3_OR   + pyrs1 + pyimm
        in_andi  = op + (6 << RD_SHIFT) + FUNC3_AND  + pyrs1 + pyimm
        in_slli  = op + (7 << RD_SHIFT) + FUNC3_SLL  + pyrs1 + pysht + FUNC7_0
        in_srli  = op + (8 << RD_SHIFT) + FUNC3_SRL  + pyrs1 + pysht + FUNC7_0
        in_srai  = op + (9 << RD_SHIFT) + FUNC3_SRL  + pyrs1 + pysht + FUNC7_1
        in_slti  = op + (10 << RD_SHIFT) + FUNC3_SLT  + pyrs1 + pyimm
        in_sltiu = op + (11 << RD_SHIFT) + FUNC3_SLTU + pyrs1 + pyimm

        self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_addi), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_xori), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 8), WORD(in_ori) , 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 12), WORD(in_andi), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 16), WORD(in_slli), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 20), WORD(in_srli), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 24), WORD(in_srai), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 28), WORD(in_slti), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 32), WORD(in_sltiu), 1)
        
        for i in range (3,12):
            next_pc = self.cpu.run(reg_pc) 
            
            if i == 3:
                self.check_result_rf(i, WORD(0x64), "I-Type ADDI")
            elif i == 4:
                self.check_result_rf(i, WORD(0xffffff54), "I-Type XORI")
            elif i == 5:
                self.check_result_rf(i, WORD(0xffffffdc), "I-Type ORI")              
            elif i == 6:
                self.check_result_rf(i, WORD(0x00000088), "I-Type ANDI")
            elif i == 7:
                self.check_result_rf(i, WORD(0xf9c00000), "I-Type SLLI")
            elif i == 8:
                self.check_result_rf(i, WORD(0x00000fff), "I-Type SRLI")
            elif i == 9:
                self.check_result_rf(i, WORD(0xffffffff), "I-Type SLAI")
            elif i == 10:
                self.check_result_rf(i, WORD(0x1), "I-Type SLTI")
            elif i == 11:
                self.check_result_rf(i, WORD(0x0), "I-Type SLTIU")

            reg_pc = next_pc

        dump = self.cpu.run(reg_pc)

    def i_type_load(self):
        reg_pc, i = self.reset_pc()
    
        op = I_TYPE_LOAD
        rs1 = 1
        rd1 = WORD(0x80000000)

        IMM0 = WORD(0x0) << 20
        IMM1 = WORD(0x1) << 20
        IMM2 = WORD(0x2) << 20
        IMM3 = WORD(0x3) << 20

        self.cpu.dp.rf.write(rs1, rd1)

        addr = WORD(0x80000000)
        self.cpu.dp.DMEM.access(1, addr, WORD(0xdeadbeef), 1)

        pyrs1 = rs1 << RS1_SHIFT

        in_lb1  = op + (2 << RD_SHIFT) + FUNC3_LB + pyrs1 + IMM0
        in_lb2  = op + (3 << RD_SHIFT) + FUNC3_LB + pyrs1 + IMM1
        in_lb3  = op + (4 << RD_SHIFT) + FUNC3_LB + pyrs1 + IMM2
        in_lb4  = op + (5 << RD_SHIFT) + FUNC3_LB + pyrs1 + IMM3
        in_lh1  = op + (6 << RD_SHIFT) + FUNC3_LH + pyrs1 + IMM0
        in_lh2  = op + (7 << RD_SHIFT) + FUNC3_LH + pyrs1 + IMM2
        in_lw   = op + (8 << RD_SHIFT) + FUNC3_LW + pyrs1 + IMM0
        in_lbu1  = op + (9 << RD_SHIFT) + FUNC3_LBU + pyrs1 + IMM0
        in_lbu2  = op + (10 << RD_SHIFT) + FUNC3_LBU + pyrs1 + IMM1
        in_lbu3  = op + (11 << RD_SHIFT) + FUNC3_LBU + pyrs1 + IMM2
        in_lbu4  = op + (12 << RD_SHIFT) + FUNC3_LBU + pyrs1 + IMM3
        in_lhu1  = op + (13 << RD_SHIFT) + FUNC3_LHU + pyrs1 + IMM0
        in_lhu2  = op + (14 << RD_SHIFT) + FUNC3_LHU + pyrs1 + IMM2

        self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_lb1), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_lb2), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 8), WORD(in_lb3), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 12), WORD(in_lb4), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 16), WORD(in_lh1), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 20), WORD(in_lh2), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 24), WORD(in_lw), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 28), WORD(in_lbu1), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 32), WORD(in_lbu2), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 36), WORD(in_lbu3), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 40), WORD(in_lbu4), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 44), WORD(in_lhu1), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 48), WORD(in_lhu2), 1)
        
        for i in range (2,15):
            next_pc = self.cpu.run(reg_pc) 
            
            if i == 2:
                self.check_result_rf(i, WORD(0xffffffef), "I-Type LB_1")
            elif i == 3:
                self.check_result_rf(i, WORD(0xffffffbe), "I-Type LB_2")
            elif i == 4:
                self.check_result_rf(i, WORD(0xffffffad), "I-Type LB_3")
            elif i == 5:
                self.check_result_rf(i, WORD(0xffffffde), "I-Type LB_4")    
            elif i == 6:
                self.check_result_rf(i, WORD(0xffffbeef), "I-Type LH_1")  
            elif i == 7:
                self.check_result_rf(i, WORD(0xffffdead), "I-Type LH_2")  
            elif i == 8:
                self.check_result_rf(i, WORD(0xdeadbeef), "I-Type LW") 
            elif i == 9:
                self.check_result_rf(i, WORD(0x000000ef), "I-Type LBU_1")
            elif i == 10:
                self.check_result_rf(i, WORD(0x000000be), "I-Type LBU_2")
            elif i == 11:
                self.check_result_rf(i, WORD(0x000000ad), "I-Type LBU_3")
            elif i == 12:
                self.check_result_rf(i, WORD(0x000000de), "I-Type LBU_4")
            elif i == 13:
                self.check_result_rf(i, WORD(0x0000beef), "I-Type LHU_1")
            elif i == 14:
                self.check_result_rf(i, WORD(0x0000dead), "I-Type LHU_2")

            reg_pc = next_pc

        dump = self.cpu.run(reg_pc)

    def s_type(self):
        reg_pc, i = self.reset_pc()
        
        rs1 = 1
        rd1 = WORD(0x12345678)
        self.cpu.dp.rf.write(rs1, rd1)

        rs2 = 2
        rd2 = WORD(0x80000000)
        self.cpu.dp.rf.write(rs2, rd2)

        IMM0 = WORD(0x00000000)
        IMM1 = WORD(0x00000005)
        IMM2 = WORD(0x0000000a)
        IMM3 = WORD(0x0000000f)

        IMM4 = WORD(0x00000010)
        IMM5 = WORD(0x0000001a)
        IMM6 = WORD(0x00000020)

        DATA_ADDR0 = (rd2 + IMM0& ADDR_MASK)          
        DATA_ADDR1 = (rd2 + IMM1& ADDR_MASK)
        DATA_ADDR2 = (rd2 + IMM2& ADDR_MASK)
        DATA_ADDR3 = (rd2 + IMM3& ADDR_MASK)

        DATA_ADDR4 = (rd2 + IMM4& ADDR_MASK)
        DATA_ADDR5 = (rd2 + IMM5& ADDR_MASK)

        DATA_ADDR6 = (rd2 + IMM6& ADDR_MASK)

        pyrs1 = rs1 << RS2_SHIFT
        pyrs2 = rs2 << RS1_SHIFT

        in_sb1 = S_TYPE + (((IMM0 & S_IM_MASK1) >> S_IM_SHIFT1) << RD_SHIFT) + FUNC3_SB + pyrs2 + pyrs1 + (((IMM0 & S_IM_MASK2) >> S_IM_SHIFT2) << 25)
        in_sb2 = S_TYPE + (((IMM1 & S_IM_MASK1) >> S_IM_SHIFT1) << RD_SHIFT) + FUNC3_SB + pyrs2 + pyrs1 + (((IMM1 & S_IM_MASK2) >> S_IM_SHIFT2) << 25)
        in_sb3 = S_TYPE + (((IMM2 & S_IM_MASK1) >> S_IM_SHIFT1) << RD_SHIFT) + FUNC3_SB + pyrs2 + pyrs1 + (((IMM2 & S_IM_MASK2) >> S_IM_SHIFT2) << 25)
        in_sb4 = S_TYPE + (((IMM3 & S_IM_MASK1) >> S_IM_SHIFT1) << RD_SHIFT) + FUNC3_SB + pyrs2 + pyrs1 + (((IMM3 & S_IM_MASK2) >> S_IM_SHIFT2) << 25)

        in_sh1 = S_TYPE + (((IMM4 & S_IM_MASK1) >> S_IM_SHIFT1) << RD_SHIFT) + FUNC3_SH + pyrs2 + pyrs1 + (((IMM4 & S_IM_MASK2) >> S_IM_SHIFT2) << 25)
        in_sh2 = S_TYPE + (((IMM5 & S_IM_MASK1) >> S_IM_SHIFT1) << RD_SHIFT) + FUNC3_SH + pyrs2 + pyrs1 + (((IMM5 & S_IM_MASK2) >> S_IM_SHIFT2) << 25)

        in_sw = S_TYPE + (((IMM6 & S_IM_MASK1) >> S_IM_SHIFT1) << RD_SHIFT) + FUNC3_SW + pyrs2 + pyrs1 + (((IMM6 & S_IM_MASK2) >> S_IM_SHIFT2) << 25)
        
        self.cpu.pci.IMEM.access(1, reg_pc, WORD(in_sb1), 1)
        self.cpu.pci.IMEM.access(1, reg_pc + 4, WORD(in_sb2), 1)
        self.cpu.pci.IMEM.access(1, reg_pc + 8, WORD(in_sb3), 1)
        self.cpu.pci.IMEM.access(1, reg_pc + 12, WORD(in_sb4), 1)
        self.cpu.pci.IMEM.access(1, reg_pc + 16, WORD(in_sh1), 1)
        self.cpu.pci.IMEM.access(1, reg_pc + 20, WORD(in_sh2), 1)
        self.cpu.pci.IMEM.access(1, reg_pc + 24, WORD(in_sw), 1)
        
        for i in range (2,9):
            next_pc = self.cpu.run(reg_pc) 

            if i == 2:
                self.check_result_mem(DATA_ADDR0, WORD(0x00000078), "S-Type SB_1")
            elif i == 3:
                self.check_result_mem(DATA_ADDR1, WORD(0x00007800), "S-Type SB_2")
            elif i == 4:
                self.check_result_mem(DATA_ADDR2, WORD(0x00780000), "S-Type SB_3")
            elif i == 5:
                self.check_result_mem(DATA_ADDR3, WORD(0x78000000), "S-Type SB_4")
            elif i == 6:
                self.check_result_mem(DATA_ADDR4, WORD(0x00005678), "S-Type SH_1")
            elif i == 7:
                self.check_result_mem(DATA_ADDR5, WORD(0x56780000), "S-Type SH_2")
            elif i == 8:
                self.check_result_mem(DATA_ADDR6, WORD(0x12345678), "S-Type SW")
            

            reg_pc = next_pc

        dump = self.cpu.run(reg_pc)

    def u_type(self):
        reg_pc, i = self.reset_pc()

        IMM = WORD(0x7fff0123)

        in_lui  = U_TYPE_LUI + (2 << RD_SHIFT) + (IMM & U_MASK)
        in_aui  = U_TYPE_AUI + (3 << RD_SHIFT) + (IMM & U_MASK)

        self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_lui), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_aui), 1)

        for i in range (2,4):
            next_pc = self.cpu.run(reg_pc) 
            if i == 2:
                self.check_result_rf(i, WORD(0x7fff0000), "U-Type LUI")
            elif i == 3:
                self.check_result_rf(i, WORD(0x8fff0004), "U-Type AUIPC")
            reg_pc = next_pc

        dump = self.cpu.run(reg_pc)

    def j_type(self):
        self.cpu.reset_cpu()
        reg_pc, i = self.reset_pc()
        
        rs1 = 1
        rd1 = 100
        self.cpu.dp.rf.write(rs1, rd1)
        rs2 = 2
        rd2 = 200
        self.cpu.dp.rf.write(rs2, rd2)
        rs3 = 3
        rd3 = 300
        self.cpu.dp.rf.write(rs3, rd3)
        rs4 = 4
        rd4 = 400
        self.cpu.dp.rf.write(rs4, rd4)

        IMM = WORD(0x00000ff0)
        JUMP_ADDR = IMEM_START + (IMM & JMP_MASK)
        #7 5 8 1 10 1
        in_jmp  = J_TYPE + (5 << RD_SHIFT) + (((IMM & J_IM_MASK1) >> J_IM_SHIFT1) << 12) + (((IMM & J_IM_MASK2) >> J_IM_SHIFT2)  << 20) + (((IMM & J_IM_MASK3) >> J_IM_SHIFT3) << 21) + (((IMM & J_IM_MASK4) >> J_IM_SHIFT4) << 31)
        in_jf   = R_TYPE + (6 << RD_SHIFT) + FUNC3_ADD  + (1 << RS1_SHIFT) + (2 << RS2_SHIFT) + FUNC7_0
        in_js   = R_TYPE + (7 << RD_SHIFT) + FUNC3_ADD  + (3 << RS1_SHIFT) + (4 << RS2_SHIFT) + FUNC7_0   

        self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_jmp), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_jf), 1)
        self.cpu.pci.IMEM.access(1, WORD(JUMP_ADDR), WORD(in_js), 1)
        
        for i in range (5,8):
            next_pc = self.cpu.run(reg_pc) 
            if i == 5:
                self.check_result_rf(i, WORD(0x10000004), "J-Type JAL")
            elif i == 6:
                self.check_result_rf(i, WORD(0x0), "J-Type JAL")
            elif i == 7:
                self.check_result_rf(i, WORD(700), "J-Type JAL")
            
            reg_pc = next_pc

        dump = self.cpu.run(reg_pc)

    def i_type_jalr(self):
        self.cpu.reset_cpu()
        reg_pc, i = self.reset_pc()

        rs1 = 1
        rd1 = WORD(0x10000100)
        self.cpu.dp.rf.write(rs1, rd1)
        rs2 = 2
        rd2 = 400
        self.cpu.dp.rf.write(rs2, rd2)
        rs3 = 3
        rd3 = 100
        self.cpu.dp.rf.write(rs3, rd3)
        rs4 = 4
        rd4 = 200
        self.cpu.dp.rf.write(rs4, rd4)

        IMM = WORD(0xfffffff0)
        JUMP_ADDR = WORD(rd1 + IMM)
        #7 5 8 1 10 1
        in_jlp  = 103 + (5 << RD_SHIFT) + FUNC3_JALR + (rs1 << 15) + ((IMM & JALR_MASK) << 20)
        in_jlf   = R_TYPE + (6 << RD_SHIFT) + FUNC3_ADD  + (1 << RS1_SHIFT) + (2 << RS2_SHIFT) + FUNC7_0
        in_jls   = R_TYPE + (7 << RD_SHIFT) + FUNC3_ADD  + (3 << RS1_SHIFT) + (4 << RS2_SHIFT) + FUNC7_0   

        self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_jlp), 1)
        self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_jlf), 1)
        self.cpu.pci.IMEM.access(1, WORD(JUMP_ADDR), WORD(in_jls), 1)
        for i in range (5,8):
            next_pc = self.cpu.run(reg_pc) 
            if i == 5:
                self.check_result_rf(i, WORD(0x10000004), "I-Type JALR")
            elif i == 6:
                self.check_result_rf(i, WORD(0x0), "I-Type JALR")
            elif i == 7:
                self.check_result_rf(i, WORD(300), "I-Type JALR")
            
            reg_pc = next_pc

        dump = self.cpu.run(reg_pc)

    def b_type(self):

        be_fn3      = np.zeros(7)
        be_td1      = np.zeros(7)
        be_td2      = np.zeros(7)
        be_tn1      = np.zeros(7)
        be_tn2      = np.zeros(7)
        
        be_fn3[0]       = FUNC3_BEQ
        be_td1[0]       = 100
        be_td2[0]       = 100
        be_tn1[0]       = 100
        be_tn2[0]       = 200

        be_fn3[1]       = FUNC3_BNE
        be_td1[1]       = 100
        be_td2[1]       = 200
        be_tn1[1]       = 100
        be_tn2[1]       = 100

        be_fn3[2]       = FUNC3_BLT
        be_td1[2]       = 100
        be_td2[2]       = 200
        be_tn1[2]       = 200
        be_tn2[2]       = 100

        be_fn3[3]       = FUNC3_BGE
        be_td1[3]       = 3
        be_td2[3]       = 2
        be_tn1[3]       = 2
        be_tn2[3]       = 3

        be_fn3[4]       = FUNC3_BLTU
        be_td1[4]       = 1
        be_td2[4]       = -1
        be_tn1[4]       = -1
        be_tn2[4]       = 1

        be_fn3[5]       = FUNC3_BGEU
        be_td1[5]       = -1
        be_td2[5]       = 1
        be_tn1[5]       = 2
        be_tn2[5]       = -2

        pyrs1 = 1 << RS1_SHIFT
        pyrs2 = 2 << RS2_SHIFT
        pyrs3 = 3 << RS1_SHIFT
        pyrs4 = 4 << RS2_SHIFT

        IMM  = WORD(0x00000ff0)
        BDDR = IMEM_START + (IMM & BRC_MASK)

        IMM1 = ((IMM & B_IM_MASK1) >> B_IM_SHIFT1)
        IMM2 = ((IMM & B_IM_MASK2) >> B_IM_SHIFT2)
        IMM3 = ((IMM & B_IM_MASK3) >> B_IM_SHIFT3)
        IMM4 = ((IMM & B_IM_MASK4) >> B_IM_SHIFT4)

        test_type = 0

        for i in range(0,6):         
            self.cpu.reset_cpu()
            reg_pc, i = self.reset_pc()
            #Jumped
            self.cpu.dp.rf.write(1,be_td1[i])
            self.cpu.dp.rf.write(2,be_td2[i])
            self.cpu.dp.rf.write(3,3)
            self.cpu.dp.rf.write(4,4)

            in_bf = B_TYPE + (IMM1 << 7) + (IMM2 << 8) + be_fn3[i] + pyrs1 + pyrs2 + (IMM3 << 25) + (IMM4 << 31)
            in_bp = R_TYPE + (5 << RD_SHIFT) + FUNC3_ADD  + pyrs3 + pyrs4 + FUNC7_0
            in_bs = R_TYPE + (6 << RD_SHIFT) + FUNC3_ADD  + pyrs3 + pyrs4 + FUNC7_0
            
            self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_bf), 1)
            self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_bp), 1)
            self.cpu.pci.IMEM.access(1, WORD(BDDR), WORD(in_bs), 1)

            if test_type == 0:
                tpe = 'B-Type BEQ'
            elif test_type == 1:
                tpe = 'B-Type BNE'
            elif test_type == 2:
                tpe = 'B-Type BLT'
            elif test_type == 3:
                tpe = 'B-Type BGE'
            elif test_type == 4:
                tpe = 'B-Type BLTU'
            elif test_type == 5:
                tpe = 'B-Type BGEU'
            
            for j in range (5,7):
                next_pc = self.cpu.run(reg_pc)
                if j == 5:
                    self.check_result_rf(j, 0, tpe)
                elif j == 6:
                    self.check_result_rf(j, 7, tpe)
            
                reg_pc = next_pc

            dump = self.cpu.run(reg_pc)

            self.cpu.reset_cpu()
            reg_pc, i = self.reset_pc()
            #Not Jumped
            self.cpu.dp.rf.write(1,be_tn1[i])
            self.cpu.dp.rf.write(2,be_tn2[i])
            self.cpu.dp.rf.write(3,5)
            self.cpu.dp.rf.write(4,6)

            in_bf = B_TYPE + (IMM1 << 7) + (IMM2 << 8) + be_fn3[i] + pyrs1 + pyrs2 + (IMM3 << 25) + (IMM4 << 31)
            in_bp = R_TYPE + (5 << RD_SHIFT) + FUNC3_ADD  + pyrs3 + pyrs4 + FUNC7_0
            
            self.cpu.pci.IMEM.access(1, WORD(reg_pc), WORD(in_bf), 1)
            self.cpu.pci.IMEM.access(1, WORD(reg_pc + 4), WORD(in_bp), 1)

            next_pc = self.cpu.run(reg_pc)
            dump_pc = self.cpu.run(next_pc)
            self.check_result_rf(5, 11, tpe)
            

            test_type = test_type + 1
        dump = self.cpu.run(reg_pc)

def main():
    os.system("cls")
    progrm = test()

    progrm.run()

if __name__ == "__main__":
    main()