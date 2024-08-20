from fondi import *
#--------------------------------------------------------------------------
#   FUNC7
#--------------------------------------------------------------------------
FUNC7_1     = 32 << FUNCT7_SHIFT
FUNC7_0     = 0  << FUNCT7_SHIFT

#--------------------------------------------------------------------------
#   R - TYPE
#--------------------------------------------------------------------------
I_TYPE_ALU  = 19

FUNC3_ADD   = 0 << FUNCT3_SHIFT
FUNC3_SLL   = 1 << FUNCT3_SHIFT
FUNC3_SLT   = 2 << FUNCT3_SHIFT
FUNC3_SLTU  = 3 << FUNCT3_SHIFT
FUNC3_XOR   = 4 << FUNCT3_SHIFT
FUNC3_SRL   = 5 << FUNCT3_SHIFT
FUNC3_OR    = 6 << FUNCT3_SHIFT
FUNC3_AND   = 7 << FUNCT3_SHIFT

#--------------------------------------------------------------------------
#   I - TYPE - loads
#--------------------------------------------------------------------------
I_TYPE_LOAD = 3

FUNC3_LB    = 0 << FUNCT3_SHIFT
FUNC3_LH    = 1 << FUNCT3_SHIFT
FUNC3_LW    = 2 << FUNCT3_SHIFT
FUNC3_LBU   = 4 << FUNCT3_SHIFT
FUNC3_LHU   = 5 << FUNCT3_SHIFT

#--------------------------------------------------------------------------
#   S - TYPE
#--------------------------------------------------------------------------

FUNC3_SB    = 0 << FUNCT3_SHIFT
FUNC3_SH    = 1 << FUNCT3_SHIFT
FUNC3_SW    = 2 << FUNCT3_SHIFT

S_IM_MASK1  = WORD(0x0000001f)
S_IM_SHIFT1 = 0
S_IM_MASK2  = WORD(0x00000fe0)
S_IM_SHIFT2 = 5

#--------------------------------------------------------------------------
#   U - TYPE
#--------------------------------------------------------------------------

U_TYPE_LUI  = 55
U_TYPE_AUI  = 23

U_MASK      = WORD(0xfffff000)

#--------------------------------------------------------------------------
#   J - TYPE
#--------------------------------------------------------------------------

FUNC3_JALR = 0 << FUNCT3_SHIFT

JMP_MASK    = WORD(0x001ffffe)

JALR_MASK   = WORD(0x00000fff)

J_IM_MASK1  = WORD(0x000ff000)
J_IM_SHIFT1 = 12
J_IM_MASK2  = WORD(0x00000800)
J_IM_SHIFT2 = 11
J_IM_MASK3  = WORD(0x000007fe)
J_IM_SHIFT3 = 1
J_IM_MASK4  = WORD(0x00100000)
J_IM_SHIFT4 = 20

#--------------------------------------------------------------------------
#   J - TYPE
#--------------------------------------------------------------------------

FUNC3_BEQ    = 0 << FUNCT3_SHIFT
FUNC3_BNE    = 1 << FUNCT3_SHIFT
FUNC3_BLT    = 4 << FUNCT3_SHIFT
FUNC3_BGE    = 5 << FUNCT3_SHIFT
FUNC3_BLTU   = 6 << FUNCT3_SHIFT
FUNC3_BGEU   = 7 << FUNCT3_SHIFT

BRC_MASK     = WORD(0x00000fff)

B_IM_MASK1   = WORD(0x00000800)
B_IM_SHIFT1  = 11
B_IM_MASK2   = WORD(0x0000001e)
B_IM_SHIFT2  = 1
B_IM_MASK3   = WORD(0x000007e0)
B_IM_SHIFT3  = 5
B_IM_MASK4   = WORD(0x00001000)
B_IM_SHIFT4  = 12