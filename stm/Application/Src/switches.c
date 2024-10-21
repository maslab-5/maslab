#include "switches.h"
#include "main.h"

static uint8_t switches = 0;

static struct DigitalPin pins[6] = {
		{RMD7_GPIO_Port, RMD7_Pin},
		{RMD8_GPIO_Port, RMD8_Pin},
		{RMD9_GPIO_Port, RMD9_Pin},
		{RMD10_GPIO_Port, RMD10_Pin},
		{RMD11_GPIO_Port, RMD11_Pin},
		{RMD12_GPIO_Port, RMD12_Pin},
};

void updateSwitches(void) {
	uint8_t data = 0;
	for (uint8_t rmd = 0; rmd < 6; rmd++) {
		data |= !HAL_GPIO_ReadPin(pins[rmd].port, pins[rmd].pin) << rmd;
	}
	switches = data;
}

uint8_t getSwitches(void) {
	return switches;
}

uint8_t getSwitch(uint8_t sw) {
	return (switches>>sw) & 1;
}
