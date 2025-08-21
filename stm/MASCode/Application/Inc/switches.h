#ifndef INC_RESISTIVE_H_
#define INC_RESISTIVE_H_

#include "inttypes.h"
#include "main.h"

struct DigitalPin {
	GPIO_TypeDef *port;
	uint16_t pin;
};

void updateSwitches(void);

uint8_t getSwitches(void);
uint8_t getSwitch(uint8_t sw);

#endif
