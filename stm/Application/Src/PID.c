#include "PID.h"
#include "encoders.h"
#include <stdlib.h>
#include "math.h"
#include "timer.h"

//kd -> enc/ms
//ki -> enc*ms
static float kp, ki, kd;//2, 0.00005, 200
static uint8_t maxSignal;//80

static int32_t errPrev[2] = {0};
static int32_t errInt[2] = {0};
static int32_t target[2] = {0};

static struct Timer timer = {0};

void initPID(float _kp, float _ki, float _kd, uint8_t maxSig) {
	kp = _kp;
	ki = _ki;
	kd = _kd;
	maxSignal = maxSig;
}

void resetPID(void) {
	for (uint8_t motor = 0; motor < 2; motor++) {
		errPrev[motor] = 0;
		errInt[motor] = 0;
	}
}

void updatePID(void) {
	updateTimer(&timer);
	if (!timerReady(&timer)) {
		return;
	}
	//sample encoders at same time
	const int32_t pos[2] = {getEncoder(LeftMotor), getEncoder(RightMotor)};

	uint8_t dir[2] = {0};
	uint8_t speed[2] = {0};

	for (uint8_t motor = 0; motor < 2; motor++) {
		const int32_t err = pos[motor] - target[motor];

		errInt[motor] += err*timer.deltaTime;
		const float drive = kp*(float)err + kd*(float)(err - errPrev[motor])/(float)timer.deltaTime + ki*(float)errInt[motor];
		errPrev[motor] = err;

		dir[motor] = drive > 0;
		speed[motor] = fmin(fabs(drive), maxSignal);
	}

	//write motor speeds at same time
	for (uint8_t motor = 0; motor < 2; motor++) {
		largeMotorDirection(motor, dir[motor]);
		largeMotorSpeed(motor, speed[motor]);
	}
}

void setTarget(enum LargeMotor motor, int32_t trgt) {
	target[motor] = trgt;
}
