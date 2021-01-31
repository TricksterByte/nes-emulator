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
// for more info

//static const uint8_t baseCycles[256] =
//{
///*0x00*/ 7, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 4, 4, 6, 6,
///*0x10*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
///*0x20*/ 6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 4, 4, 6, 6,
///*0x30*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
///*0x40*/ 6, 6, 2, 8, 3, 3, 5, 5, 3, 2, 2, 2, 3, 4, 6, 6,
///*0x50*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
///*0x60*/ 6, 6, 2, 8, 3, 3, 5, 5, 4, 2, 2, 2, 5, 4, 6, 6,
///*0x70*/ 2, 5, 2, 8, 4, 4, 6, 6, 2, 4, 2, 7, 4, 4, 7, 7,
///*0x80*/ 2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2, 2, 4, 4, 4, 4,
///*0x90*/ 2, 6,  ,  , 4, 4, 4, 4, 2, 5, 2,  ,  , 5,  ,  ,
///*0xA0*/ 2, 6, 2, 6, 3, 3, 3, 3, 2, 2, 2,  , 4, 4, 4, 4,
///*0xB0*/ 2, 5,  , 5, 4, 4, 4, 4, 2, 4, 2,  , 4, 4, 4, 4,
///*0xC0*/ 2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
///*0xD0*/ 2, 5,  , 8, 4, 4, 6, 6, 2, 4, 2, 7,  , 4, 7, 7,
///*0xE0*/ 2, 6, 2, 8, 3, 3, 5, 5, 2, 2, 2, 2, 4, 4, 6, 6,
///*0xF0*/ 2, 5,  , 8, 4, 4, 6, 6, 2, 4, 2, 7,  , 4, 7, 7,
//};

void X6502::clock()
{
	if (cycles == 0)
	{
		uint8_t opcode = read(pc); // Read next instruction byte

		SET_BIT(p, U); // Always set Unused flag bit to 1

		pc++; // Increment Program Counter

		//cycles = basicCycles[opcode]; // Get base number of cycles
	}

	cycles--;
}
