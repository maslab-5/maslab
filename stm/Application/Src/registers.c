#include "registers.h"
#include "encoders.h"
#include "main.h"
#include <string.h>

static uint8_t cycle = 0;

static struct RegisterPins outputRegisterPins[OUTPUTREGISTERS] = { {
		LMCLK_GPIO_Port, LMCLK_Pin,
		LMDAT_GPIO_Port, LMDAT_Pin, LMSV_GPIO_Port, LMSV_Pin }, {
		SRCLK_GPIO_Port, SRCLK_Pin,
		SRDAT_GPIO_Port, SRDAT_Pin, SRSV_GPIO_Port, SRSV_Pin } };
static uint8_t outputRegisterRequest[OUTPUTREGISTERS] = { 0 };
static uint8_t outputRegisterSend[OUTPUTREGISTERS] = { 0 };

static struct RegisterPins inputRegisterPins[INPUTREGISTERS] = { {
		ENCLK_GPIO_Port, ENCLK_Pin,
		ENSO_GPIO_Port, ENSO_Pin, ENPL_GPIO_Port, ENPL_Pin } };
static uint8_t inputRegisterBuffer[INPUTREGISTERS] = { 0 };
static uint8_t inputRegisterOutput[INPUTREGISTERS] = { 0 };

void registerHandler(void) {
	if (cycle == 0) {
		memcpy(outputRegisterSend, outputRegisterRequest, OUTPUTREGISTERS);
		for (uint8_t reg = 0; reg < OUTPUTREGISTERS; reg++) {
			HAL_GPIO_WritePin(outputRegisterPins[reg].loadPort,
					outputRegisterPins[reg].loadPin, 1);
		}
		for (uint8_t reg = 0; reg < INPUTREGISTERS; reg++) {
			HAL_GPIO_WritePin(inputRegisterPins[reg].loadPort,
					inputRegisterPins[reg].loadPin, 0);
		}
	}
	if (cycle % 2 == 0) {
		for (uint8_t reg = 0; reg < OUTPUTREGISTERS; reg++) {
			HAL_GPIO_WritePin(outputRegisterPins[reg].clockPort,
					outputRegisterPins[reg].clockPin, 0);
			HAL_GPIO_WritePin(outputRegisterPins[reg].dataPort,
					outputRegisterPins[reg].dataPin,
					(outputRegisterSend[reg] >> (7 - cycle / 2)) & 1);
		}
		for (uint8_t reg = 0; reg < INPUTREGISTERS; reg++) {
			HAL_GPIO_WritePin(inputRegisterPins[reg].clockPort,
					inputRegisterPins[reg].clockPin, 1);
		}
	} else {
		for (uint8_t reg = 0; reg < OUTPUTREGISTERS; reg++) {
			HAL_GPIO_WritePin(outputRegisterPins[reg].clockPort,
					outputRegisterPins[reg].clockPin, 1);
		}
		for (uint8_t reg = 0; reg < INPUTREGISTERS; reg++) {
			inputRegisterBuffer[reg] |= HAL_GPIO_ReadPin(
					inputRegisterPins[reg].dataPort,
					inputRegisterPins[reg].dataPin) << (7 - cycle / 2);
			//inverted but suppress clock high if cycle == 15
			HAL_GPIO_WritePin(inputRegisterPins[reg].clockPort,
					inputRegisterPins[reg].clockPin, cycle == 15);
		}
	}
	if (cycle == 15) {
		for (uint8_t reg = 0; reg < OUTPUTREGISTERS; reg++) {
			HAL_GPIO_WritePin(outputRegisterPins[reg].loadPort,
					outputRegisterPins[reg].loadPin, 0);
		}
		for (uint8_t reg = 0; reg < INPUTREGISTERS; reg++) {
			HAL_GPIO_WritePin(inputRegisterPins[reg].loadPort,
					inputRegisterPins[reg].loadPin, 1);
		}
		encoderHandler(inputRegisterBuffer[EncoderRegister]);
		memcpy(inputRegisterOutput, inputRegisterBuffer, INPUTREGISTERS);
		memset(inputRegisterBuffer, 0, INPUTREGISTERS);
	}
	cycle++;
	if (cycle == 16) {
		cycle = 0;
	}
}

void writeRegister(enum OutputRegister reg, uint8_t value) {
	outputRegisterRequest[reg] = value;
}

uint8_t readRegister(enum InputRegister reg) {
	return inputRegisterOutput[reg];
}

void setRegisterBit(enum OutputRegister reg, uint8_t bit) {
	outputRegisterRequest[reg] |= 1 << bit;
}

void clearRegisterBit(enum OutputRegister reg, uint8_t bit) {
	outputRegisterRequest[reg] &= 0xFF ^ (1 << bit);
}
