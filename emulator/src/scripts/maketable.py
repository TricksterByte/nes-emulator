from opcodes import A
from opcodes import I
from opcodes import ops

# TODO Interrupts missing proper addresses

microcode = { # Decode address operand
              "addr = read(PC++)" : [A.ZPG, A.ZPX, A.ZPY, A.REL, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IND, A.IZX, A.IZYRD, A.IZYWR, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "d = X" : [A.ZPX, A.ABXRD, A.ABXWR, A.IZX, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "d = Y" : [A.ZPY, A.ABYRD, A.ABYWR, A.IZYRD, A.IZYWR, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "addr = u8(addr + d); d = 0; tick()" : [A.ZPX, A.ZPY, A.IZX, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "addr = u8(addr); addr += 256 * read(PC++)" : [A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IND, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "addr = read(c = addr); addr += 256 * read(wrap(c, c + 1))" : [A.IND, A.IZX, A.IZYRD, A.IZYWR, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "misfire(addr, addr + d)" : [A.ABXRD, A.ABYRD, A.IZYRD, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "read(wrap(addr, addr + d))" : [A.ABXWR, A.ABYWR, A.IZYWR, I.ADC, I.AND, I.ASL, I.BCC, I.BCS, I.BEQ, I.BIT, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.JMP, I.JSR, I.LDA, I.LDX, I.LDY, I.LSR, I.NOP, I.ORA, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTI, I.RTS, I.SBC, I.SEC, I.SED, I.SEI, I.STA, I.STX, I.STY, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],

              # Load source operand
              "t &= A" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IZX, A.IZYRD, A.IZYWR, I.AND, I.BIT, I.CMP, I.EOR, I.ORA, I.PLA, I.STA, I.TAX, I.TAY],
              "t &=  A" : [A.ACC, I.ASL, I.LSR, I.ROL, I.ROR],
              "t &= X" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, I.CPX, I.DEX, I.INX, I.STX, I.TXA, I.TXS],
              "t &= Y" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, I.CPY, I.DEY, I.INY, I.STY, I.TYA],
              "t &= S" : [A.IMP, I.TSX],
              "t &= P | pbits; c = t" : [A.IMP, A.REL, I.BCC, I.BCS, I.BEQ, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.PHP, I.SEC, I.SED, I.SEI],
              "c = t; t = 0xFF" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABYRD, A.IZX, A.IZYRD, I.AND, I.BIT, I.CLC, I.CLD, I.CLI, I.CLV, I.CMP, I.CPX, I.CPY, I.EOR, I.ORA, I.SEC, I.SED, I.SEI],
              "t &= read(addr + d)" : [A.ZPG, A.ZPX, A.ZPY, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IND, A.IZX, A.IZYRD, A.IZYWR, I.ADC, I.AND, I.ASL, I.BIT, I.CMP, I.CPX, I.CPY, I.DEC, I.EOR, I.INC, I.LDA, I.LDX, I.LDY, I.LSR, I.ORA, I.ROL, I.ROR, I.SBC],
              "t &= read(PC++)" : [A.IMM, I.ADC, I.AND, I.CMP, I.CPX, I.CPY, I.EOR, I.LDA, I.LDX, I.LDY, I.ORA, I.SBC],

              # Operations that modify memory operands directly
              "V = t & 0x40; N = t &= 0x80" : [A.ZPG, A.ABS, I.BIT],
              "sb = C" : [A.ACC, A.ZPG, A.ZPX, A.ABS, A.ABXWR, I.ROL, I.ROR],
              "C = t & 0x80" : [A.ACC, A.ZPG, A.ZPX, A.ABS, A.ABXWR, I.ASL, I.ROL],
              "C = t & 0x01" : [A.ACC, A.ZPG, A.ZPX, A.ABS, A.ABXWR, I.LSR, I.ROR],
              "t = (t << 1) | (sb * 0x01)" : [A.ACC, A.ZPG, A.ZPX, A.ABS, A.ABXWR, I.ASL, I.ROL],
              "t = (t >> 1) | (sb * 0x80)" : [A.ACC, A.ZPG, A.ZPX, A.ABS, A.ABXWR, I.LSR, I.ROR],
              "t = u8(t - 1)" : [A.IMP, A.ZPG, A.ZPX, A.ABS, A.ABXWR, I.DEC, I.DEX, I.DEY],
              "t = u8(t + 1)" : [A.IMP, A.ZPG, A.ZPX, A.ABS, A.ABXWR, I.INC, I.INX, I.INY],

              # Store modified value in memory
              "write(addr + d, t)" : [A.ZPG, A.ZPX, A.ZPY, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IZX, A.IZYRD, A.IZYWR, I.ASL, I.DEC, I.INC, I.LSR, I.ROL, I.ROR, I.STA, I.STX, I.STY],

              # For operations that used up one unaccounted clock cycle
              "tick()" : [A.IMP, A.ACC, A.IMM, A.ZPG, A.ZPX, A.ZPY, A.REL, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IND, A.IZX, A.IZYRD, A.IZYWR, I.ASL, I.BCC, I.BCS, I.BEQ, I.BMI, I.BNE, I.BPL, I.BRK, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.DEC, I.DEX, I.DEY, I.INC, I.INX, I.INY, I.JSR, I.LSR, I.NOP, I.PHA, I.PHP, I.PLA, I.PLP, I.ROL, I.ROR, I.RTS, I.SEC, I.SED, I.SEI, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],

              # Stack operations and unconditional jumps
              "tick(); t = pop()" : [A.IMP, I.PLA, I.PLP, I.RTI],
              "read(PC++); PC = pop(); PC |= (pop() << 8)" : [A.IMP, I.RTI, I.RTS],
              "read(PC++)" : [A.IMP, I.RTS],
              "d = PC + (op ? -1 : 1); push(d >> 8); push(d)" : [A.IMP, A.ABS, I.BRK, I.JSR],
              "PC = addr" : [A.IMP, A.ABS, A.IND, I.BRK, I.JMP, I.JSR],
              "push(t)" : [A.IMP, I.BRK, I.PHA, I.PHP],
 
              # Bitmasks
              "t = 1" : [A.IMP, A.REL, I.BCC, I.BCS, I.BEQ, I.BMI, I.BNE, I.BPL, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV, I.SEC, I.SED, I.SEI],
              "t <<= 1" : [A.IMP, A.REL, I.BEQ, I.BMI, I.BNE, I.BPL, I.CLD, I.CLV, I.SED],
              "t <<= 2" : [A.IMP, A.REL, I.BMI, I.BPL, I.BVC, I.BVS, I.CLD, I.CLI, I.CLV, I.SED, I.SEI],
              "t <<= 4" : [A.IMP, A.REL, I.BMI, I.BPL, I.BVC, I.BVS, I.CLV],
              "t = u8(~t)" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABYRD, A.IZX, A.IZYRD, I.CLC, I.CLD, I.CLI, I.CLV, I.SBC],
              "t = c | t" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABYRD, A.IZX, A.IZYRD, I.ORA, I.SEC, I.SED, I.SEI],
              "t = c & t" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.REL, A.ABS, A.ABXRD, A.ABYRD, A.IZX, A.IZYRD, I.AND, I.BIT, I.BCC, I.BCS, I.BEQ, I.BMI, I.BNE, I.BPL, I.BVC, I.BVS, I.CLC, I.CLD, I.CLI, I.CLV],
              "t = c ^ t" : [A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABYRD, A.IZX, A.IZYRD, I.EOR],

              # Conditional branches
              "if (t) { tick(); misfire(PC, addr = s8(addr) + PC); PC = addr; }" : [A.REL, I.BCS, I.BEQ, I.BMI, I.BVS],
              "if (!t) { tick(); misfire(PC, addr = s8(addr) + PC); PC = addr; }" : [A.REL, I.BCC, I.BNE, I.BPL, I.BVC],

              # Addition and subtraction
              "c = t; t += A + C; V = (c ^ t) & (A ^ t) & 0x80; C = t & 0x100" : [A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABYRD, A.IND, A.IZX, A.IZYRD, I.ADC, I.SBC],
              "t = c - t; C = ~t & 0x100" : [A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABYRD, A.IZX, A.IZYRD, I.CMP, I.CPX, I.CPY],
 
              # Store modified value in a register
              "A = t" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, A.ABYRD, A.IZX, A.IZYRD, I.AND, I.ADC, I.EOR, I.LDA, I.ORA, I.PLA, I.SBC, I.TXA, I.TYA],
              "A =  t" : [A.ACC, I.ASL, I.LSR, I.ROL, I.ROR],
              "X = t" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, I.DEX, I.INX, I.LDX, I.TAX, I.TSX],
              "Y = t" : [A.IMP, A.IMM, A.ZPG, A.ZPX, A.ABS, A.ABXRD, I.DEY, I.INY, I.LDY, I.TAY],
              "S = t" : [A.IMP, I.TXS],

              # Flag updates
              "P = t & ~0x30" : [A.IMP, A.ACC, A.IMM, A.ZPG, A.ZPX, A.ZPY, A.REL, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IND, A.IZX, A.IZYRD, A.IZYWR, I.CLC, I.CLD, I.CLI, I.CLV, I.PLP, I.RTI, I.SEC, I.SED, I.SEI],
              "N = t & 0x80" : [A.IMP, A.ACC, A.IMM, A.ZPG, A.ZPX, A.ZPY, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IND, A.IZX, A.IZYRD, A.IZYWR, I.ADC, I.AND, I.ASL, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.LDA, I.LDX, I.LDY, I.LSR, I.ORA, I.PLA, I.ROL, I.ROR, I.SBC, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA],
              "Z = u8(t) == 0" : [A.IMP, A.ACC, A.IMM, A.ZPG, A.ZPX, A.ZPY, A.ABS, A.ABXRD, A.ABXWR, A.ABYRD, A.ABYWR, A.IND, A.IZX, A.IZYRD, A.IZYWR, I.ADC, I.AND, I.ASL, I.BIT, I.CMP, I.CPX, I.CPY, I.DEC, I.DEX, I.DEY, I.EOR, I.INC, I.INX, I.INY, I.LDA, I.LDX, I.LDY, I.LSR, I.ORA, I.PLA, I.ROL, I.ROR, I.SBC, I.TAX, I.TAY, I.TSX, I.TXA, I.TXS, I.TYA] }

b64decode = { "000000" : 'A', "000001" : 'B', "000010" : 'C', "000011" : 'D', "000100" : 'E',
              "000101" : 'F', "000110" : 'G', "000111" : 'H', "001000" : 'I', "001001" : 'J',
              "001010" : 'K', "001011" : 'L', "001100" : 'M', "001101" : 'N', "001110" : 'O',
              "001111" : 'P', "010000" : 'Q', "010001" : 'R', "010010" : 'S', "010011" : 'T',
              "010100" : 'U', "010101" : 'V', "010110" : 'W', "010111" : 'X', "011000" : 'Y',
              "011001" : 'Z', "011010" : 'a', "011011" : 'b', "011100" : 'c', "011101" : 'd',
              "011110" : 'e', "011111" : 'f', "100000" : 'g', "100001" : 'h', "100010" : 'i', 
              "100011" : 'j', "100100" : 'k', "100101" : 'l', "100110" : 'm', "100111" : 'n',
              "101000" : 'o', "101001" : 'p', "101010" : 'q', "101011" : 'r', "101100" : 's',
              "101101" : 't', "101110" : 'u', "101111" : 'v', "110000" : 'w', "110001" : 'x',
              "110010" : 'y', "110011" : 'z', "110100" : '0', "110101" : '1', "110110" : '2',
              "110111" : '3', "111000" : '4', "111001" : '5', "111010" : '6', "111011" : '7',
              "111100" : '8', "111101" : '9', "111110" : '+', "111111" : '/' }

def base64(seq):
    length = len(seq)

    if length < 6:
        seq += (0 for _ in range (6 - length))

    seq.reverse()
    seq = ''.join(str(v) for v in seq)

    return b64decode[seq]

def user():
    while True:
        userinput = input("Choose an option:\n[1]\tHEX\n[Oths]\tEXIT\n\nOption: ")

        if int(userinput) == 1:
            userinput = input("Hex value: ")
            opc = int(userinput, 16)
            print("\n[{} {}]".format(ops[opc].instruction, ops[opc].addressingMode))
            for instr, arr in microcode.items():
                if ops[opc].addressingMode in arr and ops[opc].instruction in arr:
                    print(instr)

            print("\n-------------------------\n")

        else:
            break

def maketbl():
    cnt = 0
    for instr, arr in microcode.items():
        lst = list()
        for op in ops:
            if ops[op].addressingMode in arr and ops[op].instruction in arr:
                lst += [1]
            else:
                lst += [0]

            cnt += 1
            if (cnt % 6 == 0):
                cnt = 0
                print(base64(lst), end = "")
                lst = list()
        
        cnt = 0
        print(base64(lst), end = "")
        lst = list()
        print(" {}".format(instr))

def print_ops():

    with open("opcodes.txt", "w") as f:
        for op in ops:
            print("[{} {}]".format(ops[op].instruction, ops[op].addressingMode), file = f)
            for instr, arr in microcode.items():
                if ops[op].addressingMode in arr and ops[op].instruction in arr:
                    print(instr, file = f)
            print("\n---------------------", file = f)

def main():
    print_ops()
        
if __name__ == '__main__':
    main()
