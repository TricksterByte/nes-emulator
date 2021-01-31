#pragma once

#include <cstdint>

#define BIT_VALUE(b,i) ((b & (1 << i)) >> i)
#define TOGGLE_BIT(b,i) b ^= (1 << i)
#define SET_BIT(b,i) b |= (1 << i)
#define CLEAR_BIT(b,i) b &= ~(1 << i)
#define ASSIGN_BIT(b,i,v) if (v) SET_BIT(b,i); else CLEAR_BIT(b,i);

class Bus;

class X6502
{
public:
	X6502() = default;
	~X6502() = default;

	void connectBus(Bus *b);

	uint8_t read(uint16_t addr) const;
	void write(uint16_t addr, uint8_t value) const;

	void clock();

private:
	Bus *bus = nullptr;

	/* Registers */
	uint8_t  a       = 0x00;   // Accumulator (1-byte)
	uint8_t  x       = 0x00;   // X Register (1-byte)
	uint8_t  y       = 0x00;   // Y Register (1-byte)
	uint16_t pc      = 0x0000; // Program Counter (2-byte)
	uint8_t  sp      = 0x00;   // Stack Pointer (1-byte)
	uint8_t  p       = 0x00;   // Status Register (1-byte)

	/* Status Flags */
	enum Flag
	{
		C = 0, // Carry bit
		Z,     // Zero bit
		I,     // Interrupt bit    (disables interrupts when set)
		D,     // Decimal Mode bit (unused)
		B,     // Break bit
		U,     // Unused
		V,     // Overflow bit
		N,     // Negative bit
	};

	uint8_t  value = 0x00;   // Any currently working input value
	uint16_t  addr = 0x0000; // Any currently working memory address
	uint8_t cycles = 0x00;   // Remaining cycles in the current instr.

	/* Addressing Modes */
	void IMP(); // Implicit
	void ACC(); // Accumulator
	void IMM();	// Immediate
	void ZP0();	// Zero Page
	void ZPX();	// Zero Page X-Indexd
	void ZPY();	// Zero Page Y-Indexed
	void REL();	// Relative
	void ABS();	// Absolute
	void ABX();	// Absolute X-Indexed
	void ABY();	// Absolute Y-Indexed
	void IND();	// Indirect
	void IZX();	// Indirect X-Indexed
	void IZY();	// Indirect Y-Indexed

	/* Instructions */
	void ADC(); void AND(); void ASL(); void BCC(); void BCS();
	void BEQ(); void BIT(); void BMI(); void BNE(); void BPL();
	void BRK(); void BVC(); void BVS(); void CLC(); void CLD();
	void CLI(); void CLV(); void CMP(); void CPX(); void CPY();
	void DEC(); void DEX(); void DEY(); void EOR(); void INC();
	void INX(); void INY(); void JMP(); void JSR(); void LDA();
	void LDX(); void LDY(); void LSR(); void ORA(); void PHA();
	void PHP(); void PLA(); void PLP(); void ROL(); void ROR();
	void RTI(); void RTS(); void SBC(); void SEC(); void SED();
	void SEI(); void STA(); void STX(); void STY(); void TAX();
	void TAY(); void TSX(); void TXA(); void TXS(); void TYA();

	void NOP();
	void ILL(); // Illegal instruction / Unofficial opcode

};
