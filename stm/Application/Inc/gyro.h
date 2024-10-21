#ifndef INC_GYRO_H_
#define INC_GYRO_H_

#include "inttypes.h"

void startCalibration(uint32_t time);
uint8_t isCalibrated(void);

void initGyro(void);
void updateGyro(void);

float getGyro(void);
void setGyro(float ang);

#endif
