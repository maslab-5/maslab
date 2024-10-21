#include "encoders.h"
#include "position.h"

static uint8_t maxChannels = 2;
static uint8_t lastRegister = 0;
static int32_t encoders[4] = {0};

//for position mapping
static int8_t move[4] = {0};

int32_t getEncoder(enum LargeMotor motor) {
	return encoders[motor];
}

void setChannels(uint8_t channels) {
	maxChannels = channels;
}

void encoderHandler(uint8_t currentRegister) {
	if (lastRegister == currentRegister) {
		return;
	}
	const uint8_t tempRegister = currentRegister;
	for (uint8_t chan = 0; chan < maxChannels; chan++) {
		move[chan] = 0;
		const uint8_t endCurrent = currentRegister&0x03;
		const uint8_t endLast = lastRegister&0x03;
		const uint8_t change = endCurrent^endLast;
		if ((change & endCurrent) == 1) {
			const int8_t diff = -1 + (endLast&0x02);
			encoders[chan] += diff;
			move[chan] += diff;
//			if (endLast>>1) {
//				encoders[3-chan]++;
//				move[3-chan]++;
//			}else{
//				encoders[3-chan]--;
//				move[3-chan]--;
//
//			}
		}
		currentRegister >>= 2;
		lastRegister >>= 2;
	}
	lastRegister = tempRegister;

	positionHandler(move);
}

void resetEncoders(void) {
	for (uint8_t i = 0; i < 4; i++) {
		encoders[i] = 0;
	}
}
