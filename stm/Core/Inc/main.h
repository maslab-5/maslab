/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */

/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define TRIG2_Pin GPIO_PIN_2
#define TRIG2_GPIO_Port GPIOE
#define ECHO2_Pin GPIO_PIN_3
#define ECHO2_GPIO_Port GPIOE
#define ECHO1_Pin GPIO_PIN_4
#define ECHO1_GPIO_Port GPIOE
#define M2EN_Pin GPIO_PIN_5
#define M2EN_GPIO_Port GPIOE
#define M2REF_Pin GPIO_PIN_6
#define M2REF_GPIO_Port GPIOE
#define TRIG1_Pin GPIO_PIN_13
#define TRIG1_GPIO_Port GPIOC
#define AMB2_Pin GPIO_PIN_0
#define AMB2_GPIO_Port GPIOC
#define AIN4_Pin GPIO_PIN_1
#define AIN4_GPIO_Port GPIOC
#define AIN2_Pin GPIO_PIN_2
#define AIN2_GPIO_Port GPIOC
#define AIN1_Pin GPIO_PIN_3
#define AIN1_GPIO_Port GPIOC
#define AIN3_Pin GPIO_PIN_0
#define AIN3_GPIO_Port GPIOA
#define RM1_Pin GPIO_PIN_1
#define RM1_GPIO_Port GPIOA
#define RM2_Pin GPIO_PIN_2
#define RM2_GPIO_Port GPIOA
#define RM3_Pin GPIO_PIN_3
#define RM3_GPIO_Port GPIOA
#define RM6_Pin GPIO_PIN_4
#define RM6_GPIO_Port GPIOA
#define RM5_Pin GPIO_PIN_5
#define RM5_GPIO_Port GPIOA
#define RM4_Pin GPIO_PIN_6
#define RM4_GPIO_Port GPIOA
#define BREF_Pin GPIO_PIN_7
#define BREF_GPIO_Port GPIOA
#define AMB1_Pin GPIO_PIN_4
#define AMB1_GPIO_Port GPIOC
#define LMDAT_Pin GPIO_PIN_5
#define LMDAT_GPIO_Port GPIOC
#define M1EN_Pin GPIO_PIN_0
#define M1EN_GPIO_Port GPIOB
#define M1REF_Pin GPIO_PIN_1
#define M1REF_GPIO_Port GPIOB
#define BOOT1_Pin GPIO_PIN_2
#define BOOT1_GPIO_Port GPIOB
#define LMSV_Pin GPIO_PIN_7
#define LMSV_GPIO_Port GPIOE
#define LMCLK_Pin GPIO_PIN_8
#define LMCLK_GPIO_Port GPIOE
#define SRV1_Pin GPIO_PIN_9
#define SRV1_GPIO_Port GPIOE
#define ENSO_Pin GPIO_PIN_10
#define ENSO_GPIO_Port GPIOE
#define SRV2_Pin GPIO_PIN_11
#define SRV2_GPIO_Port GPIOE
#define ENPL_Pin GPIO_PIN_12
#define ENPL_GPIO_Port GPIOE
#define SRV3_Pin GPIO_PIN_13
#define SRV3_GPIO_Port GPIOE
#define SRV4_Pin GPIO_PIN_14
#define SRV4_GPIO_Port GPIOE
#define ENCLK_Pin GPIO_PIN_15
#define ENCLK_GPIO_Port GPIOE
#define M5IN1_Pin GPIO_PIN_10
#define M5IN1_GPIO_Port GPIOB
#define M5IN2_Pin GPIO_PIN_11
#define M5IN2_GPIO_Port GPIOB
#define STRP2_Pin GPIO_PIN_12
#define STRP2_GPIO_Port GPIOB
#define STRP1_Pin GPIO_PIN_13
#define STRP1_GPIO_Port GPIOB
#define M6IN1_Pin GPIO_PIN_14
#define M6IN1_GPIO_Port GPIOB
#define M6IN2_Pin GPIO_PIN_15
#define M6IN2_GPIO_Port GPIOB
#define SRDAT_Pin GPIO_PIN_8
#define SRDAT_GPIO_Port GPIOD
#define SRSV_Pin GPIO_PIN_9
#define SRSV_GPIO_Port GPIOD
#define SRCLK_Pin GPIO_PIN_10
#define SRCLK_GPIO_Port GPIOD
#define DRE1_Pin GPIO_PIN_11
#define DRE1_GPIO_Port GPIOD
#define M7IN1_Pin GPIO_PIN_12
#define M7IN1_GPIO_Port GPIOD
#define M7IN2_Pin GPIO_PIN_13
#define M7IN2_GPIO_Port GPIOD
#define M8IN1_Pin GPIO_PIN_14
#define M8IN1_GPIO_Port GPIOD
#define M8IN2_Pin GPIO_PIN_15
#define M8IN2_GPIO_Port GPIOD
#define TX2_Pin GPIO_PIN_6
#define TX2_GPIO_Port GPIOC
#define RX2_Pin GPIO_PIN_7
#define RX2_GPIO_Port GPIOC
#define DRE2_Pin GPIO_PIN_8
#define DRE2_GPIO_Port GPIOC
#define SDA2_Pin GPIO_PIN_9
#define SDA2_GPIO_Port GPIOC
#define SCL2_Pin GPIO_PIN_8
#define SCL2_GPIO_Port GPIOA
#define DRESW_Pin GPIO_PIN_10
#define DRESW_GPIO_Port GPIOA
#define GCS_Pin GPIO_PIN_15
#define GCS_GPIO_Port GPIOA
#define GSCK_Pin GPIO_PIN_10
#define GSCK_GPIO_Port GPIOC
#define GMISO_Pin GPIO_PIN_11
#define GMISO_GPIO_Port GPIOC
#define GMOSI_Pin GPIO_PIN_12
#define GMOSI_GPIO_Port GPIOC
#define GINT2_Pin GPIO_PIN_0
#define GINT2_GPIO_Port GPIOD
#define GINT2_EXTI_IRQn EXTI0_IRQn
#define GINT1_Pin GPIO_PIN_1
#define GINT1_GPIO_Port GPIOD
#define GINT1_EXTI_IRQn EXTI1_IRQn
#define RMD7_Pin GPIO_PIN_2
#define RMD7_GPIO_Port GPIOD
#define RMD8_Pin GPIO_PIN_3
#define RMD8_GPIO_Port GPIOD
#define RMD9_Pin GPIO_PIN_4
#define RMD9_GPIO_Port GPIOD
#define TX1_Pin GPIO_PIN_5
#define TX1_GPIO_Port GPIOD
#define RX1_Pin GPIO_PIN_6
#define RX1_GPIO_Port GPIOD
#define RMD10_Pin GPIO_PIN_7
#define RMD10_GPIO_Port GPIOD
#define M4EN_Pin GPIO_PIN_4
#define M4EN_GPIO_Port GPIOB
#define M4REF_Pin GPIO_PIN_5
#define M4REF_GPIO_Port GPIOB
#define SCL1_Pin GPIO_PIN_6
#define SCL1_GPIO_Port GPIOB
#define SDA1_Pin GPIO_PIN_7
#define SDA1_GPIO_Port GPIOB
#define M3EN_Pin GPIO_PIN_8
#define M3EN_GPIO_Port GPIOB
#define M3REF_Pin GPIO_PIN_9
#define M3REF_GPIO_Port GPIOB
#define RMD11_Pin GPIO_PIN_0
#define RMD11_GPIO_Port GPIOE
#define RMD12_Pin GPIO_PIN_1
#define RMD12_GPIO_Port GPIOE

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
