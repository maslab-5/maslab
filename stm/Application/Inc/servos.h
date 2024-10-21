#ifndef INC_DRIVERS_SERVOS_H_
#define INC_DRIVERS_SERVOS_H_

#include "inttypes.h"

enum Servo {
	CameraServo,
	GateServo,
	LeftChuteServo,
	RightChuteServo,
};

void initServos(void);
void moveServo(enum Servo servo, uint16_t position);

#endif
