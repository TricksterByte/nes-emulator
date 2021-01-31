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
