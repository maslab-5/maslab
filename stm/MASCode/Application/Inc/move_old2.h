//#ifndef INC_MOVE_H_
//#define INC_MOVE_H_
//
//#include "inttypes.h"
//
//struct Transform {
//	int32_t leftStart;
//	int32_t rightStart;
//
//	float leftMult;
//	float rightMult;
//};
//
//enum VelocityState {
//	VelocityAccel,
//	VelocityConst,
//	VelocityDecel
//};
//
////struct WheelState {
////	float position;
////	int32_t target;
////
////	float accel;
////	float maxSpeed;
////
////	//signed
////	float velocity;
////
////	uint32_t startTime;
////	float startVelocity;
////	int32_t startDistance;
////	int32_t endTime;
////	enum VelocityState state;
////	uint8_t stage;
////	uint8_t cut;
////};
//
//enum Movement {
//	Line,
//	Spin,
//	PivotLeft,
//	PivotRight,
//	Stop
//};
//
//void moveUpdate(void);
//
//void setParameters(uint8_t ret, float acceleration, float speed);
//void startMovement(enum Movement move, int32_t moveAmount);
//
//uint8_t isMoving(void);
//
//#endif
