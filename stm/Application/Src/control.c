#include "control.h"
#include "switches.h"
#include "gyro.h"
#include "servos.h"
#include "motors.h"
#include "encoders.h"
#include "move.h"
#include "PID.h"

void Control_Init(void) {
	initServos();
	initMotors();
	initGyro();

	largeMotorEnable(LeftMotor, 1);
	largeMotorEnable(RightMotor, 1);
	largeMotorCurrent(LeftMotor, 100);
	largeMotorCurrent(RightMotor, 100);

	initPID(2.0, 0.00004, 180.0, 80);

	resetEncoders();
}

void Control_Loop(void) {
	updateMove();
	updatePID();

	updateGyro();
	updateSwitches();

	HAL_Delay(5);
}
