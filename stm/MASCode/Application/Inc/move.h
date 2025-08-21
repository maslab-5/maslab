#ifndef INC_MOVE_H_
#define INC_MOVE_H_

#include "inttypes.h"

enum Movement {
	Line,
	Spin,
	PivotLeft,
	PivotRight,
	ArcLeft,
	ArcRight,
};

struct Transform {
	float leftMult;
	float rightMult;
};

//enum VelocityState {
//	VelocityAccel,
//	VelocityConst,
//	VelocityDecel
//};

struct MoveState {
	int32_t distance;
};

void updateMove(void);
void startMovement(enum Movement move, int32_t amount);

void setParameters(float maxSpeed, float accel);
void stopMovement(void);
uint8_t isMoving(void);

#endif
