//#include "move.h"
//#include "encoders.h"
//#include "PID.h"
//#include "main.h"
//#include "math.h"
//
////struct PidParam motorPID = { 80, 2, 0.05, 0.2 };
//
//static struct Transform transform;
//
//static float target;
//static float current;
//
//static struct WheelState wheels[2];
//static uint8_t retract = 0;
//
//static uint32_t lastTime;
//static uint8_t moving[2] = {0};
//
//static void update_pv(struct WheelState *wheel, uint32_t deltaTime) {
//	if (wheel->state == VelocityAccel) {
//		wheel->velocity = wheel->startVelocity + ((float)deltaTime) * wheel->accel;
//		wheel->position = ((float)wheel->startDistance)
//				+ ((float)deltaTime) * (wheel->velocity + wheel->startVelocity)
//						/ 2.0;
//	} else if (wheel->state == VelocityDecel) {
//		wheel->velocity = wheel->startVelocity - (float)deltaTime * wheel->accel;
//		wheel->position = (float) wheel->startDistance
//				+ (float) deltaTime * (wheel->velocity + wheel->startVelocity)
//						/ 2.0;
//	} else {
//		wheel->position = (float) wheel->startDistance
//				+ (float) deltaTime * wheel->velocity;
//	}
//}
//
//static void calculate_move(struct WheelState *wheel, uint32_t currentTime, uint8_t index) {
//	if (wheel->cut && wheel->stage == 1) {
//		wheel->stage=2;
//	}
//	if (wheel->stage == 0) {
//		wheel->cut = 0;
//		//speed
//		float peakDist = wheel->velocity*wheel->velocity/wheel->accel;
//		float distLeft = wheel->target-wheel->position;
//
//		if (fabs(distLeft) >= peakDist) {
//			wheel->endTime = wheel->maxSpeed/wheel->accel;
//		}else{
//			wheel->endTime = sqrtf(fabs(distLeft)/wheel->accel);
//			wheel->cut = 1;
//		}
//		if (distLeft > 0) {
//			wheel->state = VelocityAccel;
//		}else {
//			wheel->state = VelocityDecel;
//		}
//	}else if (wheel->stage == 1){
//		//constant
//		float slowDist = wheel->velocity*wheel->velocity/wheel->accel/2.0;
//		float distLeft = wheel->target-wheel->position;
//
//		wheel->endTime = (fabs(distLeft) - slowDist)/wheel->maxSpeed;
//		wheel->state = VelocityConst;
//	}else if (wheel->stage == 2) {
//		//slow
//		float distLeft = fabs(wheel->target-wheel->position);
//
//		wheel->endTime = sqrtf(distLeft*2.0/wheel->accel);
//		wheel->velocity = (float)wheel->endTime*wheel->accel;
//		if (wheel->position<wheel->target) {
//			wheel->state = VelocityDecel;
//		}else{
//			wheel->velocity = -wheel->velocity;
//			wheel->state = VelocityAccel;
//		}
//	}else if (wheel->stage == 3) {
//		//over
//		wheel->position = wheel->target;
//		wheel->velocity = 0;
//		moving[index] = 0;
//	}
//	wheel->startDistance = wheel->position;
//	wheel->startTime = currentTime;
//	wheel->startVelocity = wheel->velocity;
//
//	wheel->endTime += currentTime;
//	wheel->stage++;
//}
//
//void moveUpdate(void) {
//	const uint32_t currentTime = HAL_GetTick();
////	const uint32_t dt = currentTime - lastTime;
//	lastTime = currentTime;
//
//	for (uint8_t motor = 0; motor < 2; motor++) {
//		struct WheelState *wheel = &wheels[motor];
//		if (moving[motor]) {
//			if (wheel->endTime >= currentTime) {
//				//update movement
//				update_pv(wheel, currentTime - wheel->startTime);
//			} else {
//				//new stage
//				calculate_move(wheel, currentTime, motor);
//			}
//		}
//
////		updatePID(motor, wheel->position, dt);
//	}
//}
//
//void setParameters(uint8_t ret, float acceleration, float speed) {
//	retract = ret;
//	for (uint8_t motor = 0; motor < 2; motor++) {
//		wheels[motor].accel = acceleration;
//		wheels[motor].maxSpeed = speed;
//	}
//}
//
//void startMovement(enum Movement move, int32_t moveAmount) {
//	if (isMoving()) {
//		return;
//	}
//	switch (move) {
//	case Line:
//		wheels[LeftMotor].target = wheels[LeftMotor].position + moveAmount;
//		wheels[RightMotor].target = wheels[RightMotor].position - moveAmount;
//		moving[0] = 1;
//		moving[1] = 1;
//		break;
//	case Spin:
//		wheels[LeftMotor].target = wheels[LeftMotor].position + moveAmount;
//		wheels[RightMotor].target = wheels[RightMotor].position + moveAmount;
//		moving[0] = 1;
//		moving[1] = 1;
//		break;
//	case PivotLeft:
//		wheels[LeftMotor].target = wheels[LeftMotor].position;
//		wheels[RightMotor].target = wheels[RightMotor].position - moveAmount;
//		moving[1] = 1;
//		break;
//	case PivotRight:
//		wheels[LeftMotor].target = wheels[LeftMotor].position + moveAmount;
//		wheels[RightMotor].target = wheels[RightMotor].position;
//		moving[0] = 1;
//		break;
//	case Stop:
//	default:
//		wheels[LeftMotor].target = wheels[LeftMotor].position;
//		wheels[RightMotor].target = wheels[RightMotor].position;
//	}
//
//	uint32_t time = HAL_GetTick();
//	wheels[LeftMotor].stage = 0;
//	wheels[RightMotor].stage = 0;
//	calculate_move(&wheels[LeftMotor], time, 0);
//	calculate_move(&wheels[RightMotor], time, 1);
//}
//
//uint8_t isMoving(void) {
//	return moving[0] | moving[1];
//}
