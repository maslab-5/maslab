#include "move.h"
#include "timer.h"
#include "motors.h"
#include "encoders.h"
#include "PID.h"
#include "stdlib.h"

struct Timer timer;

static float maxSpeed = 1;
static float accel = 0.001f;

static float lastSpeed = 0;
static float speed = 0;
static float distance = 0;

static int32_t leftStart = 0;
static int32_t rightStart = 0;
static float amount = 0;
static float dir = 1;

static struct Transform movements[6] = {
		{-1.0, 1.0},
		{1.0, 1.0},
		{1.0, 0.0},
		{0.0, 1.0},
		{1.0, -0.3},
		{-0.3, 1},
};

//init zero transform
static struct Transform trans = {0.0, 0.0};

void updateMove(void) {
	updateTimer(&timer);
	if (!timerReady(&timer)) {
		return;
	}

	const float deltaspeed = (float)accel * (float)timer.deltaTime;
	if (amount - distance <= lastSpeed*lastSpeed/2.0/accel) {
		speed = lastSpeed - deltaspeed;
		if (speed < 0) {
			speed = 0;
		}
	} else {
		speed = lastSpeed + deltaspeed;
		if (speed > maxSpeed) {
			speed = maxSpeed;
		}
	}

	distance += (float)timer.deltaTime*(speed+lastSpeed)/2.0;
	lastSpeed = speed;

	setTarget(LeftMotor, leftStart + distance*trans.leftMult*dir);
	setTarget(RightMotor, rightStart  + distance*trans.rightMult*dir);
}

void startMovement(enum Movement move, int32_t amt) {
	leftStart = getEncoder(LeftMotor);
	rightStart = getEncoder(RightMotor);

	trans = movements[move];

	distance = 0;
	dir = ((float)(amt < 0)*2.0)-1.0;
	amount = labs(amt);
}

void stopMovement(void) {
	leftStart = getEncoder(LeftMotor);
	rightStart = getEncoder(RightMotor);

	distance = 0;
	amount = 0;
}

void setParameters(float speed, float acceleration) {
	maxSpeed = speed;
	accel = acceleration;
}

uint8_t isMoving(void) {
	return distance < amount || speed != 0;
}
