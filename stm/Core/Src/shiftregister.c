/*
 * shiftregister.c
 *
 *  Created on: Jan 9, 2024
 *      Author: Anshul
 */

#include "main.h"

uint8_t clock_state = 0;
uint8_t req;

void SRHandler(void) {
	clock_state = !clock_state;
	HAL_GPIO_WritePin(LMCLK_GPIO_Port, LMCLK_Pin, clock_state);
	cycle++ ;
	HAL
}

void RegisterRequest(uint8_t value) {
	req = value;
}
