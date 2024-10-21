#ifndef INC_TIMER_H_
#define INC_TIMER_H_

#include "main.h"

struct Timer {
	uint32_t currentTime;
	uint32_t lastTime;
	uint32_t deltaTime;
};

void updateTimer(struct Timer *timer);
uint32_t timerReady(struct Timer *timer);

#endif
