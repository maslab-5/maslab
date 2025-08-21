#include "position.h"
#include "encoders.h"
#include "gyro.h"
#include "math.h"

static const float tickAng = atan(1.0/TIRE_SPACING);

static float posX = 0;
static float posY = 0;

//-1, 0, 1
//[left, right]

void positionHandler(int8_t *move) {
	if (!move[0] && !move[1]) {
		return;
	}

	const float bearing = getGyro();

	if (move[0] == -move[1]) {
		//straight
		if (move[0]) {
			posX += cos(bearing);
			posY += sin(bearing);
		}else{
			posX -= cos(bearing);
			posY -= sin(bearing);
		}
		return;
	}
//	if (move[0] == move[1]) {
////		bearing -= 2.0*tickAng*(float)move[0];
//		return;
//	}

	if (move[0] - move[1] > 0) {
		posX += cos(bearing)*0.5;
		posY += sin(bearing)*0.5;
	}else{
		posX -= cos(bearing)*0.5;
		posY -= sin(bearing)*0.5;
	}

//	bearing -= tickAng*(float)(move[0]+move[1]);
}

float getPosX() {
	return posX;
}

float getPosY() {
	return posY;
}

void setPosition(float oX, float oY) {
	posX = oX;
	posY = oY;
}
