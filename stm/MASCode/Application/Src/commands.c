#include "move.h"
#include "commands.h"
#include "usbd_cdc_if.h"
#include "motors.h"
#include "servos.h"
#include "switches.h"
#include "position.h"
#include "gyro.h"
#include "PID.h"

/* HEADERS */
//NUC
//0xxxxxxx send
//1xxxxxxx request

//STM32
//0xxxxxxx send
//1xxxxxxx reply

/* COMMANDS */
//-> move line
//-> move rotate
//-> move spin wheel
//-> move stop

//<- isMoving

//-> move camera
//-> open gate
//-> close gate

//-> chute down
//-> chute up

void Command_Handler(uint8_t *rxBuf) {
	float param1, param2, param3;

	uint8_t resp[16] = {rxBuf[0], 0};
	uint8_t resp_len = 1;
	switch (rxBuf[0]) {
	case 0:
		/* GOOD */
		moveServo(rxBuf[1], *((uint16_t*)(rxBuf+2)));
		break;
	case 1:
		startMovement(rxBuf[1], *((uint32_t*)(rxBuf+2)));
		break;
	case 2:
		memcpy(&param1, &rxBuf[1], 4);
		memcpy(&param2, &rxBuf[5], 4);
		setParameters(param1, param2);
		break;
	case 3:
		/* GOOD */
		smallMotorDuty(rxBuf[1], rxBuf[2], rxBuf[3]);
		break;
	case 4:
		/* GOOD */
		largeMotorEnable(rxBuf[1], rxBuf[2]);
		break;
	case 5:
		/* GOOD */
		largeMotorCurrent(rxBuf[1], rxBuf[2]);
		break;
	case 6:
		/* GOOD */
		largeMotorDirection(rxBuf[1], rxBuf[2]);
		break;
	case 7:
		/* GOOD */
		largeMotorSpeed(rxBuf[1], rxBuf[2]);
		break;
	case 8:
		resp[1] = isMoving();
		resp_len = 2;
		break;
	case 9:
		resp[1] = getSwitch(rxBuf[1]);
		resp_len = 2;
		break;
	case 10:
		param1 = getPosX();
		param2 = getPosY();
		param3 = getGyro();
		memcpy(&resp[1], &param1, 4);
		memcpy(&resp[5], &param2, 4);
		memcpy(&resp[9], &param3, 4);
		resp_len = 13;
		break;
	case 11:
		memcpy(&param1, &rxBuf[1], 4);
		memcpy(&param2, &rxBuf[5], 4);
		memcpy(&param3, &rxBuf[9], 4);
		setPosition(param1, param2);
		setGyro(param3);
		break;
	case 12:
		stopMovement();
		break;
	case 13:
		startCalibration(*((uint16_t*)(rxBuf+1)));
		break;
	case 14:
		resp[1] = isCalibrated();
		resp_len = 2;
		break;
	case 15:
		resetPID();
		break;
	default:
		break;
	}

	CDC_Transmit_FS(resp, resp_len);
}
