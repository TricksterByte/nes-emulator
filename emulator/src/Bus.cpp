#include "Bus.h"

Bus::Bus()
{
	cpu.connectBus(this);
}

uint8_t Bus::read(uint16_t addr)
{
	if (0x0000 < addr && addr < 0xFFFF)
		return ram[addr];

	return 0x00;
}

void Bus::write(uint16_t addr, uint8_t value)
{
	if (0x0000 < addr && addr < 0xFFFF)
		ram[addr] = value;
}
