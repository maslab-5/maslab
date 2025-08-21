#include <motors.h>
#include "main.h"
#include "registers.h"

extern TIM_HandleTypeDef htim2;
extern TIM_HandleTypeDef htim3;
extern TIM_HandleTypeDef htim4;
extern TIM_HandleTypeDef htim9;
extern TIM_HandleTypeDef htim10;
extern TIM_HandleTypeDef htim11;
extern TIM_HandleTypeDef htim12;

static struct LargeMotorPins largeMotorPins[4];
static struct SmallMotorPins smallMotorPins[4];

void initMotors(void) {
	largeMotorPins[0] = (struct LargeMotorPins ) { htim3, TIM_CHANNEL_3,
				htim3, TIM_CHANNEL_4, M1PH, M1EN };
	largeMotorPins[1] = (struct LargeMotorPins ) { htim9, TIM_CHANNEL_1,
					htim9, TIM_CHANNEL_2, M2PH, M2EN };
	largeMotorPins[2] = (struct LargeMotorPins ) { htim10, TIM_CHANNEL_1,
					htim11, TIM_CHANNEL_1, M3PH, M3EN };
	largeMotorPins[3] = (struct LargeMotorPins ) { htim3, TIM_CHANNEL_1,
					htim3, TIM_CHANNEL_2, M4PH, M4EN };

	//start channels
	for (uint8_t chan = 0; chan < 4; chan++) {
		HAL_TIM_PWM_Start(&largeMotorPins[chan].speedTimer, largeMotorPins[chan].speedChannel);
		HAL_TIM_PWM_Start(&largeMotorPins[chan].currentTimer, largeMotorPins[chan].currentChannel);
	}

	smallMotorPins[0] = (struct SmallMotorPins ) { htim2, TIM_CHANNEL_3,
		htim2, TIM_CHANNEL_4};
	smallMotorPins[1] = (struct SmallMotorPins ) { htim12, TIM_CHANNEL_1,
			htim12, TIM_CHANNEL_2};
	smallMotorPins[2] = (struct SmallMotorPins ) { htim4, TIM_CHANNEL_1,
			htim4, TIM_CHANNEL_2};
	smallMotorPins[3] = (struct SmallMotorPins ) { htim4, TIM_CHANNEL_3,
			htim4, TIM_CHANNEL_4};

	for (uint8_t chan = 0; chan < 4; chan++) {
		HAL_TIM_PWM_Start(&smallMotorPins[chan].aTimer, smallMotorPins[chan].aChannel);
		HAL_TIM_PWM_Start(&smallMotorPins[chan].bTimer, smallMotorPins[chan].bChannel);
	}
}

void largeMotorEnable(enum LargeMotor motor, uint8_t enable) {
	if (enable) {
		setRegisterBit(MotorRegister, largeMotorPins[motor].registerEnable);
	}else{
		clearRegisterBit(MotorRegister, largeMotorPins[motor].registerEnable);
	}
}
//0-100
void largeMotorSpeed(enum LargeMotor motor, uint8_t speed) {
	__HAL_TIM_SET_COMPARE(&largeMotorPins[motor].speedTimer, largeMotorPins[motor].speedChannel, speed);
}
void largeMotorDirection(enum LargeMotor motor, uint8_t dir) {
	if (dir) {
		setRegisterBit(MotorRegister, largeMotorPins[motor].registerDirection);
	}else{
		clearRegisterBit(MotorRegister, largeMotorPins[motor].registerDirection);
	}
}
//0-100 = 0-6.5
void largeMotorCurrent(enum LargeMotor motor, uint8_t current) {
	__HAL_TIM_SET_COMPARE(&largeMotorPins[motor].currentTimer, largeMotorPins[motor].currentChannel, current);
}

void smallMotorDuty(enum SmallMotor motor, uint8_t aDuty, uint8_t bDuty) {
	__HAL_TIM_SET_COMPARE(&smallMotorPins[motor].aTimer, smallMotorPins[motor].aChannel, aDuty);
	__HAL_TIM_SET_COMPARE(&smallMotorPins[motor].bTimer, smallMotorPins[motor].bChannel, bDuty);
}
