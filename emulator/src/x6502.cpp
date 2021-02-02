#include "x6502.h"
#include "Bus.h"

///////////////////////////////////////
// BASIC I/O

void X6502::connectBus(Bus *b)
{
	bus = b;
}

uint8_t X6502::read(uint16_t addr) const
{
	return bus->read(addr);
}

void X6502::write(uint16_t addr, uint8_t value) const
{
	bus->write(addr, value);
}

// See:
// https://www.masswerk.at/6502/6502_instruction_set.html
// http://wiki.nesdev.com/w/index.php/Programming_with_unofficial_opcodes
// http://www.ffd2.com/fridge/docs/6502-NMOS.extra.opcodes
// for more info

static const uint8_t baseCycles[256] =
{
/*0x00*/ 7, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 4, 4, 6, 6,
/*0x10*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
/*0x20*/ 6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 4, 4, 6, 6,
/*0x30*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
/*0x40*/ 6, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 3, 4, 6, 6,
/*0x50*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
/*0x60*/ 6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 5, 4, 6, 6,
/*0x70*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
/*0x80*/ 2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
/*0x90*/ 2, 6, 2, 6, 4, 4, 4, 4, 2, 5, 2, 5, 5, 5, 5, 5,
/*0xA0*/ 2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
/*0xB0*/ 2, 5, 2, 5, 4, 4, 4, 4, 2, 4, 2, 4, 4, 4, 4, 4,
/*0xC0*/ 2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
/*0xD0*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
/*0xE0*/ 2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
/*0xF0*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
};

void X6502::clock()
{
	if (cycles == 0)
	{
		uint8_t opcode = read(pc); // Read next instruction byte

		SET_BIT(p, U); // Always set Unused flag bit to 1

		pc++; // Increment Program Counter

		cycles = baseCycles[opcode]; // Get base number of cycles

		switch (opcode)
		{
			// #include "opcodes.inc"
		}
	}

	cycles--;
}

///////////////////////////////////////
// ADDRESSING MODES

// See:
// http://wiki.nesdev.com/w/index.php/CPU_addressing_modes
// for more info

// Implied/Implicit
// Desc.: Instructions that have no address operand
//        and the destination of results is implied.
void X6502::IMP()
{
	return;
}

// Accumulator
// Desc.: Instructions that operate on the accumulator.
//        Can be considered an implicit A.
void X6502::ACC()
{
	value = a;
	return;
}

// Immediate
// Desc.: Instructions that expect the next byte to be
//        used as an operand, rather than fethcing a
//        value from memory.
void X6502::IMM()
{
	addr = pc++;

	value = read(addr);
	return;
}

// 16-bit addresses address a 64kB memory range
// The 6502 interprets addresses by page and offset:
// the hi byte representes the page, the lo byte
// represents the offset.
// Effectively, there are 256 pages which address
// a 256 byte range.

// Zero Page
// Desc.: Instructions that fetch the value from an 8-bit
//        address on the first (zero) page
void X6502::ZPG()
{
	addr =  read(pc++);
	addr &= 0x00FF;

	value = read(addr);
	return;
}

// Zero Page X-Indexed
// Desc.: Fundamentally the same as ZPG, but the contents
//        of the X register are added to the supplied address.
//        This is useful for iterating through ranges within
//        the first page.
void X6502::ZPX()
{
	addr =  read(pc++);
	addr += uint16_t(x);
	addr &= 0x00FF;

	value = read(addr);
	return;
}

// Zero Page Y-Indexed
// Desc.: Fundamentally the same as ZPX, but the contents
//        of the Y register are added instead.
void X6502::ZPY()
{
	addr =  read(pc++);
	addr += uint16_t(y);
	addr &= 0x00FF;

	value = read(addr);
	return;
}


// Relative
// Desc.: Branch instructions that have a relative addressing
//        mode specified by an 8-bit -sigmed- offset.
void X6502::REL()
{
	displ = int8_t(read(pc++));
	return;
}

// Absolute
// Desc.: Instructions that fetch the value from a 16-bit
//        address anywhere in memory.
void X6502::ABS()
{
	addr =  read(pc++);      // lo byte
	addr |= read(pc++) << 8; // hi byte

	value = read(addr);
	return;
}

// Absolute X-Indexed for reads
// Desc.: Fundamentally the same as ABS for read ops,
//        but the contents of the X register are added
//        to the supplied address.
// Ntes.: Adds 1 to cycles if page boundary is crossed.
void X6502::ABXRD()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(x);

	if ((addr ^ tmp) & 0x100)
		cycles++;

	value = read(addr);
	return;
}

// Absolute Y-Indexed for reads
// Desc.: Fundamentally the same as ABXRD, but the
//        contents of the Y register are used instead.
// Ntes.: Adds 1 to cycles if page boundary is crossed.
void X6502::ABYRD()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(y);

	if ((addr ^ tmp) & 0x100)
		cycles++;
	
	value = read(addr);
	return;
}

// Absolute X-Indexed for writes and rmws
// Desc.: Essentially the same as ABXRD for write
//        and rmw ops.
// Ntes.: Write and Read-Modify-Write ops do not
//        increment the number of cycles. (why??)
void X6502::ABXWR()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(x);

	addr = (addr & 0x00FF) | (tmp && 0xFF00);

	value = read(addr);
	return;
}

// Absolute Y-Indexed for writes and rmws
// Desc.: Essentially the same as ABXWR, but the
//        contents of the Y register are used instead.
// Ntes.: Write and Read-Modify-Write ops do not
//        increment the number of cycles. (why??)
void X6502::ABYWR()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(y);

	addr = (addr & 0x00FF) | (tmp && 0xFF00);

	value = read(addr);
	return;
}

// Indirect
// Desc.: JMP instruction has a special addressing mode
//        where the supplied 16-bit address is read to
//        get the actual 16-bit adddress
// Ntes.: This instruction has a bug in the hardware, in
//        that if the lo byte is FF, then the CPU will not
//        increment the hi byte and read from the wrong page.
void X6502::IND()
{
	uint16_t ptr = read(pc++);
	ptr |= read(pc++);

	if ((ptr & 0x00FF) == 0x00FF)
		addr = (read(ptr & 0xFF00) << 8) | read(ptr);
	else
		addr = (read(ptr + 1) << 8) | read(ptr);

	value = read(addr);
	return;
}

// Indirect X-Indexed
// Desc.: Instructions that read from an address on the zero
//        page, indexed by the supplied 8-bit address offset
//        by the X register.
// Ntes.: Doesn't discriminate between reads and writes.
void X6502::IZX()
{
	uint16_t tmp = read(pc++);
	tmp += uint16_t(x);

	addr  = read(tmp & 0x00FF);
	addr |= read((tmp + 1) & 0x00FF) << 8;

	value = read(addr);
	return;
}

// Indirect Y-Indexed for reads
// Desc.: Instructions where the supllied address is
//        a location on the zero page and from where
//        the actual 16-bit address is read and then
//        offset by the contents in the Y register.
// Ntes.: Adds 1 to cycles if page boundary is crossed.
void X6502::IZYRD()
{
	uint16_t tmp = read(pc++);
	uint16_t target = read(tmp & 0x00FF);
	target |= read((tmp + 1) & 0x00FF) << 8;

	addr = target;
	addr += uint16_t(y);

	if ((addr ^ target) & 0x100)
		cycles++;

	value = read(addr);
	return;
}

// Indirect Y-Indexed for writes and rmws
// Desc.: Essentially the same as ABYRD for write
//        and rmw ops.
// Ntes.: Write and Read-Modify-Write ops do not
//        increment the number of cycles. (why??)
void X6502::IZYWR()
{
	uint16_t tmp = read(pc++);
	uint16_t target = read(tmp & 0x00FF);
	target |= read((tmp + 1) & 0x00FF) << 8;

	addr = target;
	addr += uint16_t(y);

	addr = (addr & 0x00FF) | (target & 0xFF00);

	value = read(addr);
	return;
}

///////////////////////////////////////
// Instructions

// Add Memory to Accumulator w/ Carry
// Func.: A + M + C -> A, C
// Flags: N, Z, C, V
void X6502::ADC()
{
	uint16_t tmp = a + value + BIT_VALUE(p, C);

	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, (tmp & 0xFF) == 0);
	ASSIGN_BIT(p, C, tmp > 255);
	ASSIGN_BIT(p, V, 0x0080 & (~(a ^ value) & (a ^ tmp)));

	a = tmp & 0x00FF;
	return;
}

// AND Memory w/ Accumulator
// Func.: A AND M -> A
// Flags: N, Z
void X6502::AND()
{
	a &= value;

	ASSIGN_BIT(p, N, a & 0x80);
	ASSIGN_BIT(p, Z, a == 0);

	return;
}

// TODO
// Shift Left One Bit (Memory or Accumulator)
// Func.: C <- [76543210] <- 0
// Flags: N, Z, C
void X6502::ASL()
{

}

// Branch on Carry Clear
// Func.: branch on C = 0
// Flags: -
void X6502::BCC()
{
	if (!BIT_VALUE(p, C))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}

// Branch on Carry Set
// Func.: branch on C = 1
// Flags: -
void X6502::BCS()
{
	if (BIT_VALUE(p, C))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}

// Branch on Result Zero
// Func.: branch on Z = 1
// Flags: -
void X6502::BEQ()
{
	if (BIT_VALUE(p, Z))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}

// Test Bits in Memory w/ Accumulator
// Func.: A AND M, M7 -> N, M6 -> V
// Flags: N, Z, V
void X6502::BIT()
{
	uint8_t tmp = a & value;

	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, tmp == 0);
	ASSIGN_BIT(p, V, tmp & 0x40);

	return;
}

// Branch on Result Minus
// Func.: branch on N = 1
// Flags: -
void X6502::BMI()
{
	if (BIT_VALUE(p, N))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}

// Branch on Result not Zero
// Func.: branch on Z = 0
// Flags: -
void X6502::BNE()
{
	if (!BIT_VALUE(p, Z))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}


// Branch on Result Plus
// Func.: branch on N = 0
// Flags: -
void X6502::BPL()
{
	if (!BIT_VALUE(p, N))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}

// TODO
// Force Break
// Func.: interrupt, push PC+2, push P
// Flags: I
void X6502::BRK()
{

}

// Branch on Overflow Clear
// Func.: branch on V = 0
// Flags: -
void X6502::BVC()
{
	if (!BIT_VALUE(p, V))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}

// Branch on Overflow Set
// Func.: branch on V = 1
// Flags: -
void X6502::BVS()
{
	if (BIT_VALUE(p, V))
	{
		cycles++;
		addr = pc + displ;

		if ((addr ^ pc) & 0x100)
			cycles++;

		pc = addr;
	}

	return;
}

// Clear Carry Flag
// Func.: 0 -> C
// Flags: C
void X6502::CLC()
{
	CLEAR_BIT(p, C);
	return;
}

// Clear Decimal Mode
// Func.: 0 -> D
// Flags: D
void X6502::CLD()
{
	CLEAR_BIT(p, D);
	return;
}

// Clear Interrupt Disable Bit
// Func.: 0 -> I
// Flags: I
void X6502::CLI()
{
	CLEAR_BIT(p, I);
	return;
}

// Clear Overflow Flag
// Func.: 0 -> V
// Flags: V
void X6502::CLV()
{
	CLEAR_BIT(p, V);
	return;
}

// Compare Memory w/ Accumulator
// Func.: A - M
// Flags: N, Z, C
void X6502::CMP()
{
	uint8_t tmp = a - value;
	
	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, tmp == 0);
	ASSIGN_BIT(p, C, a >= value);

	return;
}

// Compare Memory and Index X
// Func.: X - M
// Flags: N, Z, C
void X6502::CPX()
{
	uint8_t tmp = x - value;

	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, tmp == 0);
	ASSIGN_BIT(p, C, x >= value);

	return;
}

// Compare Memory and Index Y
// Func.: Y - M
// Flags: N, Z, C
void X6502::CPY()
{
	uint8_t tmp = y - value;

	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, tmp == 0);
	ASSIGN_BIT(p, C, y >= value);

	return;
}

// Decrement Memory by One
// Func.: M - 1 -> M
// Flags: N, Z
void X6502::DEC()
{
	uint8_t tmp = value - 1;

	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, tmp == 0);

	write(addr, tmp);
	return;
}

// Decrement Index X by One
// Func.: X - 1 -> x
// Flags: N, Z
void X6502::DEX()
{
	x--;

	ASSIGN_BIT(p, N, x & 0x80);
	ASSIGN_BIT(p, Z, x == 0);

	return;
}

// Decrement Index Y by One
// Func.: Y - 1 -> Y
// Flags: N, Z
void X6502::DEY()
{
	y--;

	ASSIGN_BIT(p, N, y & 0x80);
	ASSIGN_BIT(p, Z, y == 0);

	return;
}

// Exclusive-OR Memory w/ Accumulator
// Func.: A EOR M -> A
// Flags: N, Z
void X6502::EOR()
{
	a ^= value;

	ASSIGN_BIT(p, N, a & 0x80);
	ASSIGN_BIT(p, Z, a == 0);

	return;
}

// Increment Memory by One
// Func.: M + 1 -> M
// Flags: N, Z
void X6502::INC()
{
	uint8_t tmp = value + 1;

	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, tmp == 0);

	write(addr, tmp);
	return;
}

// Increment Index X by One
// Func.: X + 1 -> X
// Flags: N, Z
void X6502::INX()
{
	x++;

	ASSIGN_BIT(p, N, x & 0x80);
	ASSIGN_BIT(p, Z, x == 0);

	return;
}

// Increment Index Y by One
// Func.: Y + 1 -> Y
// Flags: N, Z
void X6502::INY()
{
	y++;

	ASSIGN_BIT(p, N, y & 0x80);
	ASSIGN_BIT(p, Z, y == 0);

	return;
}

// Jump to New Location
// Func.: PC+1 -> PCL, PC+2 -> PCH
// Flags: -
void X6502::JMP()
{
	pc = addr;
}

// TODO
// Jump to New Location Saving Return Address
// Func.: push PC+2, PC+1 -> PCL, PC+2 -> PCH
// Flags: -
void X6502::JSR()
{

}

// Load Accumulator w/ Memory
// Func.: M -> A
// Flags: N, Z
void X6502::LDA()
{
	a = value;

	ASSIGN_BIT(p, N, a & 0x80);
	ASSIGN_BIT(p, Z, a == 0);

	return;
}

// Load Index X w/ Memory
// Func.: M -> X
// Flags: N, Z
void X6502::LDX()
{
	x = value;

	ASSIGN_BIT(p, N, x & 0x80);
	ASSIGN_BIT(p, Z, x == 0);

	return;
}

// Load Index Y w/ Memory
// Func.: M -> Y
// Flags: N, Z
void X6502::LDY()
{
	y = value;

	ASSIGN_BIT(p, N, y & 0x80);
	ASSIGN_BIT(p, Z, y == 0);

	return;
}

// TODO
// Shift One Bit Right (Memory or Accumulator)
// Func.: 0 -> [76543210] -> C
// Flags: N, Z, C
void X6502::LSR()
{

}

// OR Memory w/ Accumulator
// Func.: A OR M -> A
// Flags: N, Z
void X6502::ORA()
{
	a |= value;

	ASSIGN_BIT(p, N, a & 0x80);
	ASSIGN_BIT(p, Z, a == 0);

	return;
}

// TODO
// Push Accumulator on Stack
// Func.: push A
// Flags: -
void X6502::PHA()
{

}

// TODO
// Push Processor Status on Stack
// Func.: push P
// Flags: -
void X6502::PHP()
{

}

// TODO
// Pull Accumulator from Stack
// Func.: pull A
// Flags: N, Z
void X6502::PLA()
{
	
}

// TODO
// Pull Processor Status from Stack
// Func.: pull P
// Flags: from stack
void X6502::PLP()
{

}

// TODO
// Rotate One Bit Left (Memory or Accumulator)
// Func.: C <- [76543210] <- C
// Flags: N, Z, C
void X6502::ROL()
{

}

// TODO
// Rotate One Bit Right (Memory or Accumulator)
// Func.: C -> [76543210] -> C
// Flags: N, Z, C
void X6502::ROR()
{

}

// TODO
// Return from Interrupt
// Func.: pull P, pull PC
// Flags: from stack
void X6502::RTI()
{

}

// TODO
// Return from Subroutine
// Func.: pull PC, PC+1 -> PC
// Flags: -
void X6502::RTS()
{

}

// Subtract Memory from Accumulator w/ Borrow
// Func.: A - M - (C - 1) -> A
// Flags: N, Z, C, V
// Ntes.: SBC is essentially the same as ADC
//        with the memory operand inverted
//        (http://forum.6502.org/viewtopic.php?f=2&t=2944)
void X6502::SBC()
{
	uint16_t inv = value ^ 0xFF;
	uint16_t tmp = a + inv + BIT_VALUE(p, C);

	ASSIGN_BIT(p, N, tmp & 0x80);
	ASSIGN_BIT(p, Z, (tmp & 0xFF) == 0);
	ASSIGN_BIT(p, C, tmp > 255);
	ASSIGN_BIT(p, V, 0x0080 & (~(a ^ inv) & (a ^ tmp)));

	a = tmp;
	return;
}

// Set Carry Flag
// Func.: 1 -> C
// Flags: C
void X6502::SEC()
{
	SET_BIT(p, C);
	return;
}

// Set Decimal Flag
// Func.: 1 -> D
// Flags: D
void X6502::SED()
{
	SET_BIT(p, D);
	return;
}

// Set Interrupt Disable Status
// Func.: 1 -> I
// Flags: I
void X6502::SEI()
{
	SET_BIT(p, I);
	return;
}

// Store Accumulator in Memory
// Func.: A -> M
// Flags: -
void X6502::STA()
{
	write(addr, a);
	return;
}

// Store Index X in Memory
// Func.: X -> M
// Flags: -
void X6502::STX()
{
	write(addr, x);
	return;
}

// Store Index Y in Memory
// Func.: Y -> M
// Flags: -
void X6502::STY()
{
	write(addr, y);
	return;
}

// Transfer Accumulator to Index X
// Func.: A -> X
// Flags: N, Z
void X6502::TAX()
{
	x = a;

	ASSIGN_BIT(p, N, x & 0x80);
	ASSIGN_BIT(p, Z, x == 0);

	return;
}

// Transfer Accumulator to Index Y
// Func.: A -> Y
// Flags: N, Z
void X6502::TAY()
{
	y = a;

	ASSIGN_BIT(p, N, y & 0x80);
	ASSIGN_BIT(p, Z, y == 0);

	return;
}

// Transfer Stack Pointer to Index X
// Func.: SP -> X
// Flags: N, Z
void X6502::TSX()
{
	x = sp;

	ASSIGN_BIT(p, N, x & 0x80);
	ASSIGN_BIT(p, Z, x == 0);

	return;
}

// Transfer Index X to Accumulator
// Func.: X -> A
// Flags: N, Z
void X6502::TXA()
{
	a = x;

	ASSIGN_BIT(p, N, x & 0x80);
	ASSIGN_BIT(p, Z, x == 0);

	return;
}

// Transfer Index X to Stack Pointer
// Func.: X -> SP
// Flags: N, Z
void X6502::TXS()
{
	sp = x;

	ASSIGN_BIT(p, N, sp & 0x80);
	ASSIGN_BIT(p, Z, sp == 0);

	return;
}

// Transfer Index U to Accumulator
// Func.: Y -> A
// Flags: N, Z
void X6502::TYA()
{
	a = y;

	ASSIGN_BIT(p, N, y & 0x80);
	ASSIGN_BIT(p, Z, y == 0);

	return;
}

// Mo Operation
void X6502::NOP()
{
	return;
}

// Called by unofficial opcodes, to be implemented
// for 100% compatibility
void X6502::ILL()
{
	return;
}
