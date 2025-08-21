#include "gyro.h"
#include "timer.h"
#include "math.h"
#include "main.h"

extern SPI_HandleTypeDef hspi3;

static float angle = 0;

static struct Timer timer = {0};

static uint32_t calibrateEnd = 0;
static uint8_t calibrated = 0;
static uint16_t calReads = 0;
static float offset = 0;

void startCalibration(uint32_t time) {
	calibrateEnd = HAL_GetTick() + time;
	calibrated = 0;
	calReads = 0;
	angle = 0;
}

uint8_t isCalibrated(void) {
	return calibrated;
}

static int16_t read(void) {
	uint8_t address = 0x95;
	uint8_t data[2];
	HAL_GPIO_WritePin (GCS_GPIO_Port, GCS_Pin, 0);
	HAL_SPI_Transmit (&hspi3, &address, 1, 100);
	HAL_SPI_Receive (&hspi3, data, 2, 100);
	HAL_GPIO_WritePin (GCS_GPIO_Port, GCS_Pin, 1);
	uint8_t temp = data[0];
	data[0] = data[1];
	data[1] = temp;
	return *((int16_t*)data);
}

static void transmit(uint8_t address, uint8_t value) {
	uint8_t data[2];
	data[0] = address;
	data[1] = value;
	HAL_GPIO_WritePin (GCS_GPIO_Port, GCS_Pin, 0);
	HAL_SPI_Transmit (&hspi3, data, 2, 100);
	HAL_GPIO_WritePin (GCS_GPIO_Port, GCS_Pin, 1);
}

void initGyro(void) {
	//enable gyro
	transmit(0x1F, 0b00001100);
	HAL_Delay(1);
	//set gyro data rate and scale
	transmit(0x20, 0b00100110);
	//set low pass filter
	transmit(0x23, 0b00110010);
}

void updateGyro(void) {
	updateTimer(&timer);
	if (!timerReady(&timer)) {
		return;
	}
	if (!calibrated) {
		if (timer.currentTime >= calibrateEnd) {
			offset = angle/(float)calReads;
			angle = 0;
			calibrated = 1;
		}else{
			calReads+=1;
			angle += (float)read();
		}
	}else{
		angle += ((float)read() - offset) * (float)timer.deltaTime * 0.001 * 0.0174533 / 32.8;
	}
}

float getGyro(void) {
	return angle;
}

void setGyro(float ang) {
	angle = ang;
}
