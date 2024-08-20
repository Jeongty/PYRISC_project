from fondi import *

class alu(object):
    def __init__(self):
        pass

    def op(self, alua, alub, alusrc):
        
        np.seterr(all='ignore')
        if alusrc == ALU_ADD:
            output = WORD(alua + alub)
        elif alusrc == ALU_SUB:
            output = WORD(alua - alub)
        elif alusrc == ALU_SLL:
            output = WORD(alua << (alub & WORD(0x1f)))
        elif alusrc == ALU_SRL:
            output = WORD(alua >> (alub & WORD(0x1f)))
        elif alusrc == ALU_SRA:
            output = WORD(SWORD(alua) >> (alub & WORD(0x1f)))
        elif alusrc == ALU_XOR:
            output = WORD(alua ^ alub)
        elif alusrc == ALU_OR:
            output = WORD(alua | alub)
        elif alusrc == ALU_AND:
            output = WORD(alua & alub)
        elif alusrc == ALU_SLT:
            output = WORD(1) if SWORD(alua) < SWORD(alub) else WORD(0)
        elif alusrc == ALU_SLTU:
            output = WORD(1) if alua < alub else WORD(0)
        else:
            output = WORD(0)

        return output

class adder(object):

    def __init__(self):
        pass

    def op(self, add1, add2 = 4):
        return WORD(add1 + add2)