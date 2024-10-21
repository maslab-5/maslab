#ifndef INC_DRIVERS_PID_H_
#define INC_DRIVERS_PID_H_

#include "motors.h"

void initPID(float kp, float ki, float kd, uint8_t maxSignal);
void resetPID(void);

void updatePID(void);

void setTarget(enum LargeMotor motor, int32_t target);

#endif
