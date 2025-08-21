////#include "drivers/encoders.h"
////#include "drivers/PID.h"
//#include "move_old_.h"
//#include "main.h"
//#include "math.h"
//
////static struct PathProfile slowProfile = {0.002, 0.1};
////static struct PathProfile fastProfile = {0.002, 0.5};
////static struct PathChannel path;
//
//static struct PidParam motorPID = { 70, 0.9, 0.1, 0.05 };
//static uint8_t positionThresh = 5;
//static float speedThresh = 0.01;
//
//struct WheelState wheels[2];
//static uint8_t retract = 0;
//
//static uint32_t lastTime;
//static uint8_t moving = 0;
//
//void initMove(void) {
//	initPID(LeftMotor, motorPID);
//	initPID(RightMotor, motorPID);
//}
//
//static void update_pv(struct WheelState *wheel, uint32_t deltaTime) {
//	if (wheel->state == VelocityAccel) {
//		wheel->velocity = wheel->startVelocity + ((float)deltaTime) * wheel->accel;
//		wheel->position = ((float)wheel->startDistance)
//				+ ((float)deltaTime) * (wheel->velocity + wheel->startVelocity)
//						/ 2.0;
//	} else if (wheel->state == VelocityDecel) {
//		wheel->velocity = wheel->startVelocity - (float) deltaTime * wheel->accel;
//		wheel->position = (float) wheel->startDistance
//				+ (float) deltaTime * (wheel->velocity + wheel->startVelocity)
//						/ 2.0;
//	} else {
//		wheel->position = (float) wheel->startDistance
//				+ (float) deltaTime * wheel->velocity;
//	}
//}
//
//static void calculate_move(struct WheelState *wheel, uint32_t currentTime, uint8_t new) {
//	if (fabs(wheel->velocity) < speedThresh) {
//		if (new) {
//			/* GOOD */
//			float diff = (float) wheel->target - wheel->position;
//			float peak = wheel->maxSpeed*wheel->maxSpeed/wheel->accel;
//
//			wheel->startTime = currentTime;
//			wheel->startDistance = wheel->position;
//			wheel->startVelocity = wheel->velocity;
//
//			if (fabs(diff) > peak) {
//				//accel to max
//				wheel->endTime = (float)currentTime + wheel->maxSpeed/wheel->accel;
//			}else{
//				//partial accel
//				wheel->endTime = (float)currentTime + sqrt(fabs(diff)*wheel->accel);
//			}
//
//			if (diff > 0) {
//				wheel->state = VelocityAccel;
//			}else{
//				wheel->state = VelocityDecel;
//			}
//		}else if (fabs((float)wheel->target - wheel->position)
//				< positionThresh) {
//			//stop exact
//			wheel->position = wheel->target;
//			moving = 0;
//		} else if (!retract) {
//			//overshoot
//			wheel->target = wheel->position;
//			moving = 0;
//		} else {
//			//retract
//			float diff = (float) wheel->target - wheel->position;
//			wheel->startTime = currentTime;
//			wheel->startDistance = wheel->position;
//			wheel->startVelocity = wheel->velocity;
//
//			wheel->endTime = currentTime
//					+ sqrt(fabs(diff) / wheel->accel);
//			if (diff > 0) {
//				wheel->state = VelocityAccel;
//			} else {
//				wheel->state = VelocityDecel;
//			}
//		}
//	} else if (fabs(wheel->velocity) > wheel->maxSpeed + speedThresh) {
//		/* NOT GOOD */
//		setMotorEnable(ChuteMotor, 1);
//		wheel->startTime = currentTime;
//		wheel->startVelocity = wheel->velocity;
//		wheel->startDistance = wheel->position;
//
//		wheel->endTime = currentTime
//				+ (fabs(wheel->velocity) - wheel->maxSpeed)
//						/ wheel->accel;
//		if (wheel->velocity > 0) {
//			wheel->state = VelocityDecel;
//		} else {
//			wheel->state = VelocityAccel;
//		}
//	} else if (wheel->velocity * wheel->velocity / wheel->accel / 2.0
//			> fabs((float) wheel->target - wheel->position)) {
//		setMotorEnable(ChuteMotor, 1);
//		//overshoot
//		wheel->startTime = currentTime;
//		wheel->startVelocity = wheel->velocity;
//		wheel->startDistance = wheel->position;
//
//		wheel->endTime = currentTime + wheel->velocity / wheel->accel;
//		if (wheel->velocity > 0) {
//			wheel->state = VelocityDecel;
//		} else {
//			wheel->state = VelocityAccel;
//		}
//	} else {
//		//plenty of time
//		wheel->startTime = currentTime;
//		wheel->startVelocity = wheel->velocity;
//		wheel->startDistance = wheel->position;
//
//		float decelDist = wheel->velocity * wheel->velocity
//				/ wheel->accel / 2.0;
//
//		if (fabs(wheel->velocity) >= wheel->maxSpeed - speedThresh) {
//			/* GOOD */
//			wheel->startVelocity = wheel->maxSpeed;
//			//constant
//			float constDist = fabs(
//					(float) wheel->target - wheel->position)
//					- decelDist;
//			wheel->endTime = (float)currentTime
//					+ constDist / wheel->maxSpeed;
//			wheel->state = VelocityConst;
//		} else if (fabs((float) wheel->target - wheel->position)
//				- decelDist
//				< ((wheel->maxSpeed - fabs(wheel->velocity))
//						/ wheel->accel)
//						* (wheel->maxSpeed + wheel->velocity)) {
//			//partial accel
//			setMotorEnable(ChuteMotor, 1);
//			float peakDist = fabs(
//					(float) wheel->target - wheel->position)
//					- decelDist;
//
//			wheel->endTime = currentTime
//					+ (sqrt(
//							wheel->velocity * wheel->velocity
//									- wheel->accel * peakDist)
//							- fabs(wheel->velocity)) / wheel->accel;
//			if (wheel->velocity > 0) {
//				wheel->state = VelocityAccel;
//			} else {
//				wheel->state = VelocityDecel;
//			}
//		} else {
//			setMotorEnable(ChuteMotor, 1);
//			//full accel
//			wheel->endTime = currentTime
//					+ (wheel->maxSpeed - fabs(wheel->velocity))
//							/ wheel->accel;
//			if (wheel->velocity > 0) {
//				wheel->state = VelocityAccel;
//			} else {
//				wheel->state = VelocityDecel;
//			}
//		}
//	}
//}
//
//void moveUpdate(void) {
//	const uint32_t currentTime = HAL_GetTick();
//	const uint32_t dt = currentTime - lastTime;
//	lastTime = currentTime;
//
//	for (uint8_t motor = 0; motor < 2; motor++) {
//		struct WheelState *wheel = &wheels[motor];
//		if (moving) {
//			if (wheel->endTime >= currentTime) {
//				//update movement
//				update_pv(wheel, currentTime - wheel->startTime);
//			} else {
//				calculate_move(wheel, currentTime, 0);
//			}
//		}
//
//		updatePID(motor, wheel->position, dt);
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
//	switch (move) {
//	case Line:
//		wheels[LeftMotor].target = getEncoder(LeftMotor) + moveAmount;
//		wheels[RightMotor].target = getEncoder(RightMotor) - moveAmount;
//		break;
//	case Spin:
//		wheels[LeftMotor].target = getEncoder(LeftMotor) + moveAmount;
//		wheels[RightMotor].target = getEncoder(RightMotor) + moveAmount;
//		break;
//	case PivotLeft:
//		wheels[LeftMotor].target = getEncoder(LeftMotor);
//		wheels[RightMotor].target = getEncoder(RightMotor) - moveAmount;
//		break;
//	case PivotRight:
//		wheels[LeftMotor].target = getEncoder(LeftMotor) + moveAmount;
//		wheels[RightMotor].target = getEncoder(RightMotor);
//		break;
//	case Stop:
//	default:
//		wheels[LeftMotor].target = getEncoder(LeftMotor);
//		wheels[RightMotor].target = getEncoder(RightMotor);
//	}
//	moving = 1;
//	uint32_t time = HAL_GetTick();
//	calculate_move(&wheels[LeftMotor], time, 1);
//	calculate_move(&wheels[RightMotor], time, 1);
//}
//
//uint8_t isMoving(void) {
//	return moving;
//}
