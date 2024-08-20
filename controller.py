from fondi import *

class controller(object):

    def __init__(self):
        self.aluop = 0
        self.alusrc = 0
        self.regwirte   = 1
        self.immsrc     = 0
        self.alusrca    = 0
        self.alusrcb    = 1
        self.memwirte   = 0
        self.resultsrc  = 1
        self.branch     = 0
        self.aluop      = 0
        self.jump       = 0
        pass
    
    def input(self, op, func3, func7):
        self.op = op
        self.func3 = func3
        self.func7 = func7

    def update(self):
        self.maindec()
        self.aludec()

    def maindec(self): 
        if self.op == 3: #Loads
            self.regwirte   = 1
            self.immsrc     = 0
            self.alusrca    = 0
            self.alusrcb    = 1
            self.memwirte   = 0
            self.resultsrc  = 1
            self.branch     = 0
            self.aluop      = 0
            self.jump       = 0
        elif self.op == 35: #Stores
            self.regwirte   = 0
            self.immsrc     = 1
            self.alusrca    = 0
            self.alusrcb    = 1
            self.memwirte   = 1
            self.resultsrc  = 0
            self.branch     = 0
            self.aluop      = 0
            self.jump       = 0
        elif self.op == 51: #R-type
            self.regwirte   = 1
            self.immsrc     = 0
            self.alusrca    = 0
            self.alusrcb    = 0
            self.memwirte   = 0
            self.resultsrc  = 0
            self.branch     = 0
            self.aluop      = 2
            self.jump       = 0
        elif self.op == 19: #I-type ALU
            self.regwirte   = 1
            self.immsrc     = 0
            self.alusrca    = 0
            self.alusrcb    = 1
            self.memwirte   = 0
            self.resultsrc  = 0
            self.branch     = 0
            self.aluop      = 2
            self.jump       = 0
        elif self.op == 23: #AUIPC
            self.regwirte   = 1
            self.immsrc     = 4
            self.alusrca    = 1
            self.alusrcb    = 1
            self.memwirte   = 0
            self.resultsrc  = 0
            self.branch     = 0
            self.aluop      = 0
            self.jump       = 0
        elif self.op == 55: #LUI
            self.regwirte   = 1
            self.immsrc     = 4
            self.alusrca    = 2
            self.alusrcb    = 1
            self.memwirte   = 0
            self.resultsrc  = 0
            self.branch     = 0 
            self.aluop      = 0
            self.jump       = 0
        elif self.op == 99: #B-type
            self.regwirte   = 0
            self.immsrc     = 2
            self.alusrca    = 0
            self.alusrcb    = 0
            self.memwirte   = 0
            self.resultsrc  = 0
            self.branch     = 1
            self.aluop      = 1
            self.jump       = 0
        elif self.op == 103: #JALR
            self.regwirte   = 1
            self.immsrc     = 0
            self.alusrca    = 0
            self.alusrcb    = 1
            self.memwirte   = 0
            self.resultsrc  = 2
            self.branch     = 0
            self.aluop      = 0
            self.jump       = 1
        elif self.op == 111: #JAL
            self.regwirte   = 1
            self.immsrc     = 3
            self.alusrca    = 0
            self.alusrcb    = 0
            self.memwirte   = 0
            self.resultsrc  = 2
            self.branch     = 0
            self.aluop      = 0
            self.jump       = 1
    
    def aludec(self):
        if self.aluop == 0:
            self.alusrc = 0
        elif self.aluop == 1:
            self.alusrc = 1
        elif self.aluop == 2:
            if self.func3 == 0 and self.func7 == 0: #add
                self.alusrc = ALU_ADD
            elif self.func3 == 0 and self.func7 == 32: #sub
                self.alusrc = ALU_SUB
            elif self.func3 == 1: # sll
                self.alusrc = ALU_SLL
            elif self.func3 == 5 and self.func7 == 0: #srl
                self.alusrc = ALU_SRL
            elif self.func3 == 5 and self.func7 == 32: #sra
                self.alusrc = ALU_SRA
            elif self.func3 == 4: #xor
                self.alusrc = ALU_XOR
            elif self.func3 == 6: #or
                self.alusrc = ALU_OR
            elif self.func3 == 7: #and
                self.alusrc = ALU_AND
            elif self.func3 == 2: #slt
                self.alusrc = ALU_SLT
            elif self.func3 == 3: #sltu
                self.alusrc = ALU_SLTU
