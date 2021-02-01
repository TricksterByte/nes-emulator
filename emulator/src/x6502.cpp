#include "x6502.h"
#include "Bus.h"

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
	}

	cycles--;
}

void X6502::IMP()
{
	return;
}

void X6502::ACC()
{
	value = a;
	return;
}

void X6502::IMM()
{
	addr = pc++;
	return;
}

void X6502::ZPG()
{
	addr =  read(pc++);
	addr &= 0x00FF;
	return;
}

void X6502::ZPX()
{
	addr =  read(pc++);
	addr += uint16_t(x);
	addr &= 0x00FF;
	return;
}

void X6502::ZPY()
{
	addr =  read(pc++);
	addr += uint16_t(y);
	addr &= 0x00FF;
	return;
}

void X6502::REL()
{
	displ = int8_t(read(pc++));
	return;
}

void X6502::ABS()
{
	addr =  read(pc++);      // lo byte
	addr |= read(pc++) << 8; // hi byte
	return;
}

void X6502::ABXRD()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(x);

	if ((addr ^ tmp) & 0x100)
		cycles++;

	return;
}

void X6502::ABYRD()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(y);

	if ((addr ^ tmp) & 0x100)
		cycles++;
	
	return;
}

void X6502::ABXWR()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(x);

	addr = (addr & 0x00FF) | (tmp && 0xFF00);

	return;
}

void X6502::ABYWR()
{
	uint16_t tmp = read(pc++);
	tmp |= read(pc++) << 8;

	addr = tmp;
	addr += uint16_t(y);

	addr = (addr & 0x00FF) | (tmp && 0xFF00);

	return;
}

void X6502::IND()
{
	uint16_t ptr = read(pc++);
	ptr |= read(pc++);

	if ((ptr & 0x00FF) == 0x00FF)
		addr = (read(ptr & 0x00FF) << 8) | read(ptr);
	else
		addr = (read(ptr + 1) << 8) | read(ptr);

	return;
}

void X6502::IZX()
{
	uint16_t tmp = read(pc++);
	tmp += uint16_t(x);

	addr  = read(tmp & 0x00FF);
	addr |= read((tmp + 1) & 0x00FF) << 8;

	return;
}

void X6502::IZYRD()
{
	uint16_t tmp = read(pc++);
	uint16_t target = read(tmp & 0x00FF);
	target |= read((tmp + 1) & 0x00FF) << 8;

	addr = target;
	addr += uint16_t(y);

	if ((addr ^ target) & 0x100)
		cycles++;

	return;
}

void X6502::IZYWR()
{
	uint16_t tmp = read(pc++);
	uint16_t target = read(tmp & 0x00FF);
	target |= read((tmp + 1) & 0x00FF) << 8;

	addr = target;
	addr += uint16_t(y);

	addr = (addr & 0x00FF) | (target & 0xFF00);

	return;
}
