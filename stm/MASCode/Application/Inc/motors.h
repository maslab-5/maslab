#ifndef INC_DRIVERS_MOTORS_H_
#define INC_DRIVERS_MOTORS_H_

#include "main.h"
#include "inttypes.h"

struct LargeMotorPins {
	TIM_HandleTypeDef speedTimer;
	uint16_t speedChannel;
	TIM_HandleTypeDef currentTimer;
	uint16_t currentChannel;
	uint8_t registerDirection;
	uint8_t registerEnable;
};

struct SmallMotorPins {
	TIM_HandleTypeDef aTimer;
	uint16_t aChannel;
	TIM_HandleTypeDef bTimer;
	uint16_t bChannel;
};

enum LargeMotor {
	LeftMotor = 0u,
	RightMotor = 1u,
	ChuteMotor = 2u,
};

enum SmallMotor {
	GateMotor = 0u,//5
};

void initMotors(void);

//0-100
void largeMotorEnable(enum LargeMotor motor, uint8_t enable);
void largeMotorSpeed(enum LargeMotor rmotor, uint8_t speed);
void largeMotorDirection(enum LargeMotor motor, uint8_t dir);
//0-100 = 0-6.5
void largeMotorCurrent(enum LargeMotor motor, uint8_t current);

void smallMotorDuty(enum SmallMotor motor, uint8_t aDuty, uint8_t bDuty);

#endif
