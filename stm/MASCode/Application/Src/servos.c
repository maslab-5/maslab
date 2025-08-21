#include "servos.h"
#include "main.h"

extern TIM_HandleTypeDef htim1;

static uint16_t channels[4] = {
		TIM_CHANNEL_1,
		TIM_CHANNEL_2,
		TIM_CHANNEL_3,
		TIM_CHANNEL_4
};

void initServos(void) {
	for (uint8_t chan = 0; chan < 4; chan++) {
		HAL_TIM_PWM_Start(&htim1, channels[chan]);
	}
}

//0-500
void moveServo(enum Servo servo, uint16_t position) {
	__HAL_TIM_SET_COMPARE(&htim1, channels[servo], position+500);
}
