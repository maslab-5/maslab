#ifndef INC_POSITION_H_
#define INC_POSITION_H_

#include "inttypes.h"

#define TIRE_SPACING 501.34

void positionHandler(int8_t *move);

void resetPosition(void);

float getPosX(void);
float getPosY(void);

void setPosition(float oX, float oY);

#endif
