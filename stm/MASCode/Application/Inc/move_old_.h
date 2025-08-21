#ifndef INC_MOVE_OLD_H_
#define INC_MOVE_OLD_H_

#include "inttypes.h"

enum VelocityState {
	VelocityAccel,
	VelocityConst,
	VelocityDecel
};

struct WheelState {
	float position;
	int32_t target;

	float accel;
	float maxSpeed;

	//signed
	float velocity;

	uint32_t startTime;
	float startVelocity;
	int32_t startDistance;
	uint32_t endTime;
	enum VelocityState state;
};

enum Movement {
	Line,
	Spin,
	PivotLeft,
	PivotRight,
	Stop
};

void initMove(void);
void moveUpdate(void);

void setParameters(uint8_t ret, float acceleration, float speed);
void startMovement(enum Movement move, int32_t moveAmount);

uint8_t isMoving(void);

#endif
