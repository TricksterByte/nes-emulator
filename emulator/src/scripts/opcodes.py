from enum import Enum

class A(Enum):
    IMP = 0
    ACC = 0
    IMM = 1
    ZPG = 2
    ZPX = 3
    ZPY = 4
    REL = 5
    ABS = 6
    ABXRD = 7
    ABXWR = 8
    ABYRD = 9
    ABYWR = 10
    IND = 11
    IZX = 12
    IZYRD = 13
    IZYWR = 14

class I(Enum):
    ADC = 0
    AND = 1
    ASL = 2
    BCC = 3
    BCS = 4
    BEQ = 5
    BIT = 6
    BMI = 7
    BNE = 8
    BPL = 9
    BRK = 10
    BVC = 11
    BVS = 12
    CLC = 13
    CLD = 14
    CLI = 15
    CLV = 16
    CMP = 17
    CPX = 18
    CPY = 19
    DEC = 20
    DEX = 21
    DEY = 22
    EOR = 23
    INC = 24
    INX = 25
    INY = 26
    JMP = 27
    JSR = 28
    LDA = 29
    LDX = 30
    LDY = 31
    LSR = 32
    NOP = 33
    ORA = 34
    PHA = 35
    PHP = 36
    PLA = 37
    PLP = 38
    ROL = 39
    ROR = 40
    RTI = 41
    RTS = 42
    SBC = 43
    SEC = 44
    SED = 45
    SEI = 46
    STA = 47
    STX = 48
    STY = 49
    TAX = 50
    TAY = 51
    TSX = 52
    TXA = 53
    TXS = 54
    TYA = 55

from dataclasses import dataclass

@dataclass
class Op:
    instruction : I
    addressingMode : A

    def __repr__(self):
        return "Instr: {}, Addr: {}".format(self.instruction, self.addressingMode)

ops = { 0x00 : Op(I.BRK, A.IMP), 0x01 : Op(I.ORA, A.IZX), 0x02 : Op(I.NOP, A.IMP), 0x03 : Op(I.NOP, A.IMP), 0x04 : Op(I.NOP, A.IMP), 0x05 : Op(I.ORA, A.ZPG), 0x06 : Op(I.ASL, A.ZPG), 0x07 : Op(I.NOP, A.IMP), 0x08 : Op(I.PHP, A.IMP), 0x09 : Op(I.ORA, A.IMM), 0x0A : Op(I.ASL, A.ACC), 0x0B : Op(I.NOP, A.IMP), 0x0C : Op(I.NOP, A.IMP), 0x0D : Op(I.ORA, A.ABS), 0x0E : Op(I.ASL, A.ABS), 0x0F : Op(I.NOP, A.IMP),
        0x10 : Op(I.BPL, A.REL), 0x11 : Op(I.ORA, A.IZYRD), 0x12 : Op(I.NOP, A.IMP), 0x13 : Op(I.NOP, A.IMP), 0x14 : Op(I.NOP, A.IMP), 0x15 : Op(I.ORA, A.ZPX), 0x16 : Op(I.ASL, A.ZPX), 0x17 : Op(I.NOP, A.IMP), 0x18 : Op(I.CLC, A.IMP), 0x19 : Op(I.ORA, A.ABYRD), 0x1A : Op(I.NOP, A.IMP), 0x1B : Op(I.NOP, A.IMP), 0x1C : Op(I.NOP, A.IMP), 0x1D : Op(I.ORA, A.ABXRD), 0x1E : Op(I.ASL, A.ABXWR), 0x1F : Op(I.NOP, A.IMP),
        0x20 : Op(I.JSR, A.ABS), 0x21 : Op(I.AND, A.IZX), 0x22 : Op(I.NOP, A.IMP), 0x23 : Op(I.NOP, A.IMP), 0x24 : Op(I.BIT, A.ZPG), 0x25 : Op(I.AND, A.ZPG), 0x26 : Op(I.ROL, A.ZPG), 0x27 : Op(I.NOP, A.IMP), 0x28 : Op(I.PLP, A.IMP), 0x29 : Op(I.AND, A.IMM), 0x2A : Op(I.ROL, A.ACC), 0x2B : Op(I.NOP, A.IMP), 0x2C : Op(I.BIT, A.ABS), 0x2D : Op(I.AND, A.ABS), 0x2E : Op(I.ROL, A.ABS), 0x2F : Op(I.NOP, A.IMP),
        0x30 : Op(I.BMI, A.REL), 0x31 : Op(I.AND, A.IZYRD), 0x32 : Op(I.NOP, A.IMP), 0x33 : Op(I.NOP, A.IMP), 0x34 : Op(I.NOP, A.IMP), 0x35 : Op(I.AND, A.ZPX), 0x36 : Op(I.ROL, A.ZPX), 0x37 : Op(I.NOP, A.IMP), 0x38 : Op(I.SEC, A.IMP), 0x39 : Op(I.AND, A.ABYRD), 0x3A : Op(I.NOP, A.IMP), 0x3B : Op(I.NOP, A.IMP), 0x3C : Op(I.NOP, A.IMP), 0x3D : Op(I.AND, A.ABXRD), 0x3E : Op(I.ROL, A.ABXWR), 0x3F : Op(I.NOP, A.IMP),
        0x40 : Op(I.RTI, A.IMP), 0x41 : Op(I.EOR, A.IZX), 0x42 : Op(I.NOP, A.IMP), 0x43 : Op(I.NOP, A.IMP), 0x44 : Op(I.NOP, A.IMP), 0x45 : Op(I.EOR, A.ZPG), 0x46 : Op(I.LSR, A.ZPG), 0x47 : Op(I.NOP, A.IMP), 0x48 : Op(I.PHA, A.IMP), 0x49 : Op(I.EOR, A.IMM), 0x4A : Op(I.LSR, A.ACC), 0x4B : Op(I.NOP, A.IMP), 0x4C : Op(I.JMP, A.ABS), 0x4D : Op(I.EOR, A.ABS), 0x4E : Op(I.LSR, A.ABS), 0x4F : Op(I.NOP, A.IMP),
        0x50 : Op(I.BVC, A.REL), 0x51 : Op(I.EOR, A.IZYRD), 0x52 : Op(I.NOP, A.IMP), 0x53 : Op(I.NOP, A.IMP), 0x54 : Op(I.NOP, A.IMP), 0x55 : Op(I.EOR, A.ZPX), 0x56 : Op(I.LSR, A.ZPX), 0x57 : Op(I.NOP, A.IMP), 0x58 : Op(I.CLI, A.IMP), 0x59 : Op(I.EOR, A.ABYRD), 0x5A : Op(I.NOP, A.IMP), 0x5B : Op(I.NOP, A.IMP), 0x5C : Op(I.NOP, A.IMP), 0x5D : Op(I.EOR, A.ABXRD), 0x5E : Op(I.LSR, A.ABXWR), 0x5F : Op(I.NOP, A.IMP),
        0x60 : Op(I.RTS, A.IMP), 0x61 : Op(I.ADC, A.IZX), 0x62 : Op(I.NOP, A.IMP), 0x63 : Op(I.NOP, A.IMP), 0x64 : Op(I.NOP, A.IMP), 0x65 : Op(I.ADC, A.ZPG), 0x66 : Op(I.ROR, A.ZPG), 0x67 : Op(I.NOP, A.IMP), 0x68 : Op(I.PLA, A.IMP), 0x69 : Op(I.ADC, A.IMM), 0x6A : Op(I.ROR, A.ACC), 0x6B : Op(I.NOP, A.IMP), 0x6C : Op(I.JMP, A.IND), 0x6D : Op(I.ADC, A.ABS), 0x6E : Op(I.ROR, A.ABS), 0x6F : Op(I.NOP, A.IMP),
        0x70 : Op(I.BVS, A.REL), 0x71 : Op(I.ADC, A.IZYRD), 0x72 : Op(I.NOP, A.IMP), 0x73 : Op(I.NOP, A.IMP), 0x74 : Op(I.NOP, A.IMP), 0x75 : Op(I.ADC, A.ZPX), 0x76 : Op(I.ROR, A.ZPX), 0x77 : Op(I.NOP, A.IMP), 0x78 : Op(I.SEI, A.IMP), 0x79 : Op(I.ADC, A.ABYRD), 0x7A : Op(I.NOP, A.IMP), 0x7B : Op(I.NOP, A.IMP), 0x7C : Op(I.NOP, A.IMP), 0x7D : Op(I.ADC, A.ABXRD), 0x7E : Op(I.ROR, A.ABXWR), 0x7F : Op(I.NOP, A.IMP),
        0x80 : Op(I.NOP, A.IMP), 0x81 : Op(I.STA, A.IZX), 0x82 : Op(I.NOP, A.IMP), 0x83 : Op(I.NOP, A.IMP), 0x84 : Op(I.STY, A.ZPG), 0x85 : Op(I.STA, A.ZPG), 0x86 : Op(I.STX, A.ZPG), 0x87 : Op(I.NOP, A.IMP), 0x88 : Op(I.DEY, A.IMP), 0x89 : Op(I.NOP, A.IMP), 0x8A : Op(I.TXA, A.IMP), 0x8B : Op(I.NOP, A.IMP), 0x8C : Op(I.STY, A.ABS), 0x8D : Op(I.STA, A.ABS), 0x8E : Op(I.STX, A.ABS), 0x8F : Op(I.NOP, A.IMP),
        0x90 : Op(I.BCC, A.REL), 0x91 : Op(I.STA, A.IZYWR), 0x92 : Op(I.NOP, A.IMP), 0x93 : Op(I.NOP, A.IMP), 0x94 : Op(I.STY, A.ZPX), 0x95 : Op(I.STA, A.ZPX), 0x96 : Op(I.STX, A.ZPY), 0x97 : Op(I.NOP, A.IMP), 0x98 : Op(I.TYA, A.IMP), 0x99 : Op(I.STA, A.ABYWR), 0x9A : Op(I.TXS, A.IMP), 0x9B : Op(I.NOP, A.IMP), 0x9C : Op(I.NOP, A.IMP), 0x9D : Op(I.STA, A.ABXWR), 0x9E : Op(I.NOP, A.IMP), 0x9F : Op(I.NOP, A.IMP),
        0xA0 : Op(I.LDY, A.IMM), 0xA1 : Op(I.LDA, A.IZX), 0xA2 : Op(I.LDX, A.IMM), 0xA3 : Op(I.NOP, A.IMP), 0xA4 : Op(I.LDY, A.ZPG), 0xA5 : Op(I.LDA, A.ZPG), 0xA6 : Op(I.LDX, A.ZPG), 0xA7 : Op(I.NOP, A.IMP), 0xA8 : Op(I.TAY, A.IMP), 0xA9 : Op(I.LDA, A.IMM), 0xAA : Op(I.TAX, A.IMP), 0xAB : Op(I.NOP, A.IMP), 0xAC : Op(I.LDY, A.ABS), 0xAD : Op(I.LDA, A.ABS), 0xAE : Op(I.LDX, A.ABS), 0xAF : Op(I.NOP, A.IMP),
        0xB0 : Op(I.BCS, A.REL), 0xB1 : Op(I.LDA, A.IZYRD), 0xB2 : Op(I.NOP, A.IMP), 0xB3 : Op(I.NOP, A.IMP), 0xB4 : Op(I.LDY, A.ZPX), 0xB5 : Op(I.LDA, A.ZPX), 0xB6 : Op(I.LDX, A.ZPY), 0xB7 : Op(I.NOP, A.IMP), 0xB8 : Op(I.CLV, A.IMP), 0xB9 : Op(I.LDA, A.ABYRD), 0xBA : Op(I.TSX, A.IMP), 0xBB : Op(I.NOP, A.IMP), 0xBC : Op(I.LDY, A.ABXRD), 0xBD : Op(I.LDA, A.ABXRD), 0xBE : Op(I.LDX, A.ABYRD), 0xBF : Op(I.NOP, A.IMP),
        0xC0 : Op(I.CPY, A.IMM), 0xC1 : Op(I.CMP, A.IZX), 0xC2 : Op(I.NOP, A.IMP), 0xC3 : Op(I.NOP, A.IMP), 0xC4 : Op(I.CPY, A.ZPG), 0xC5 : Op(I.CMP, A.ZPG), 0xC6 : Op(I.DEC, A.ZPG), 0xC7 : Op(I.NOP, A.IMP), 0xC8 : Op(I.INY, A.IMP), 0xC9 : Op(I.CMP, A.IMM), 0xCA : Op(I.DEX, A.IMP), 0xCB : Op(I.NOP, A.IMP), 0xCC : Op(I.CPY, A.ABS), 0xCD : Op(I.CMP, A.ABS), 0xCE : Op(I.DEC, A.ABS), 0xCF : Op(I.NOP, A.IMP),
        0xD0 : Op(I.BNE, A.REL), 0xD1 : Op(I.CMP, A.IZYRD), 0xD2 : Op(I.NOP, A.IMP), 0xD3 : Op(I.NOP, A.IMP), 0xD4 : Op(I.NOP, A.IMP), 0xD5 : Op(I.CMP, A.ZPX), 0xD6 : Op(I.DEC, A.ZPX), 0xD7 : Op(I.NOP, A.IMP), 0xD8 : Op(I.CLD, A.IMP), 0xD9 : Op(I.CMP, A.ABYRD), 0xDA : Op(I.NOP, A.IMP), 0xDB : Op(I.NOP, A.IMP), 0xDC : Op(I.NOP, A.IMP), 0xDD : Op(I.CMP, A.ABXRD), 0xDE : Op(I.DEC, A.ABXWR), 0xDF : Op(I.NOP, A.IMP),
        0xE0 : Op(I.CPX, A.IMM), 0xE1 : Op(I.SBC, A.IZX), 0xE2 : Op(I.NOP, A.IMP), 0xE3 : Op(I.NOP, A.IMP), 0xE4 : Op(I.CPX, A.ZPG), 0xE5 : Op(I.SBC, A.ZPG), 0xE6 : Op(I.INC, A.ZPG), 0xE7 : Op(I.NOP, A.IMP), 0xE8 : Op(I.INX, A.IMP), 0xE9 : Op(I.SBC, A.IMM), 0xEA : Op(I.NOP, A.IMP), 0xEB : Op(I.NOP, A.IMP), 0xEC : Op(I.CPX, A.ABS), 0xED : Op(I.SBC, A.ABS), 0xEE : Op(I.INC, A.ABS), 0xEF : Op(I.NOP, A.IMP),
        0xF0 : Op(I.BEQ, A.REL), 0xF1 : Op(I.SBC, A.IZYRD), 0xF2 : Op(I.NOP, A.IMP), 0xF3 : Op(I.NOP, A.IMP), 0xF4 : Op(I.NOP, A.IMP), 0xF5 : Op(I.SBC, A.ZPX), 0xF6 : Op(I.INC, A.ZPX), 0xF7 : Op(I.NOP, A.IMP), 0xF8 : Op(I.SED, A.IMP), 0xF9 : Op(I.SBC, A.ABYRD), 0xFA : Op(I.NOP, A.IMP), 0xFB : Op(I.NOP, A.IMP), 0xFC : Op(I.NOP, A.IMP), 0xFD : Op(I.SBC, A.ABXRD), 0xFE : Op(I.INC, A.ABXWR), 0xFF : Op(I.NOP, A.IMP) }

"""
micro-code op : [addressing modes..., instructions...]

for each micro-code
    for each op in opcodes
        return 1 if op.addr in micro-code.opts or op.instr in micro-code.opts else 0
"""
