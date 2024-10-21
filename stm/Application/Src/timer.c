#include "timer.h"

void updateTimer(struct Timer *timer) {
	timer->currentTime = HAL_GetTick();
	if (timer->lastTime) {
		timer->deltaTime = timer->currentTime - timer->lastTime;
	}
	timer->lastTime = timer->currentTime;
}

uint32_t timerReady(struct Timer *timer) {
	return timer->lastTime;
}
