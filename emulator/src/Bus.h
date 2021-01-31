#pragma once
#include "x6502.h"

#include <cstdint>
#include <array>

class Bus
{
public:
	Bus();
	~Bus() = default;

	uint8_t read(uint16_t);
	void write(uint16_t addr, uint8_t value);

private:
	X6502 cpu;

	// Sample 64kB of RAM
	std::array<uint8_t, 64 * 1024> ram{ 0x00 };
};
