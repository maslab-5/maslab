#include "main.h"

#ifndef INC_DRIVERS_REGISTERS_H_
#define INC_DRIVERS_REGISTERS_H_

#define OUTPUTREGISTERS 2
#define INPUTREGISTERS 1

//register mask pins
#define M1PH 7
#define M2PH 6
#define M3PH 5
#define M4PH 0
#define M1EN 4
#define M2EN 3
#define M3EN 2
#define M4EN 1

#define PWR1 0
#define PWR2 7
#define PWR3 6
#define PWR4 5
#define PWR5 4
#define PWR6 3
#define PWR7 2
#define PWR8 1

struct RegisterPins {
	GPIO_TypeDef *clockPort;
	uint16_t clockPin;
	GPIO_TypeDef *dataPort;
	uint16_t dataPin;
	GPIO_TypeDef *loadPort;
	uint16_t loadPin;
};

enum OutputRegister {
	MotorRegister,
	PowerRegister,
};

enum InputRegister {
	EncoderRegister,
};

void registerHandler(void);

void writeRegister(enum OutputRegister reg, uint8_t value);
uint8_t readRegister(enum InputRegister reg);

void setRegisterBit(enum OutputRegister reg, uint8_t bit);
void clearRegisterBit(enum OutputRegister reg, uint8_t bit);

#endif
