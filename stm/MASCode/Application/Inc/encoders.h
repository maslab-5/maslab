#ifndef INC_DRIVERS_ENCODERS_H_
#define INC_DRIVERS_ENCODERS_H_

#include "motors.h"
#include "inttypes.h"

void setChannels(uint8_t channels);

int32_t getEncoder(enum LargeMotor motor);

void encoderHandler(uint8_t value);

void resetEncoders(void);

#endif
