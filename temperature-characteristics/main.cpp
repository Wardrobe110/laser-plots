#include "main.h"

CircularBuffer<Event> cBuf;


#define KP 6
#define KI 0.000005
#define KD 0.0001
#define SETPOINT 150


//PWM DUTY 0 - 4799 => 0 - 100 %
#define PWM_DUTY 4799
#define PWM_ACTIVATION_DELAY_US 5000000
#define PWM_UPTIME_US 1000000

int main(void)
{
  clockInit(96);
  HAL_Init();
  MX_USB_DEVICE_Init();
  //This config gives us 20 kHz PWM given 96 MHz clock speed
  TIM4Init(1, 4800);
  TIM4PWM2(0);
  SysTickInit();
  UART1Init();

  thermalRegulator.DEBUGforceKp(KP);
  thermalRegulator.DEBUGforceKi(KI);
  thermalRegulator.DEBUGforceKd(KD);
  thermalRegulator.setProcessTemperature(SETPOINT);
	//Testing
	std::string s;
	uint32_t tickRef = 0;
  uint8_t pwmArmed = 1;
  uint8_t pwmFired = 0;

	//Delay for terminal connection
	for(uint16_t i = 0; i < 500; i++){
	  sleep(10000);
	}



	/*
	s = std::to_string(KP);
	s += ", ";
	s += std::to_string(KI);
	s += ", ";
	s += std::to_string(KD);
	s += ", ";
	s += std::to_string(SETPOINT);
	s += "\r\n";
	CDC_Transmit_FS(reinterpret_cast<uint8_t*>(s.data()), s.size());

	thermalRegulator.setLastTick();
	*/

  s = std::to_string(PWM_DUTY);
  s += ", 4799 \r\n";
  CDC_Transmit_FS(reinterpret_cast<uint8_t*>(s.data()), s.size());

  tickRef = uwTick;
	while(1)
	{
	  //Terrible non timer solution for short period active PWM
    if(pwmArmed && uwTick - tickRef > PWM_ACTIVATION_DELAY_US){
      TIM4PWM2Update(PWM_DUTY);
      pwmArmed = 0;
    }
    /*if(!pwmFired && uwTick - tickRef > PWM_ACTIVATION_DELAY_US + PWM_UPTIME_US){
      TIM4PWM2Update(0);
      pwmFired = 1;
    }*/
    if( thermalRegulator.DEBUGgetCurrentTemperature() > 2500){
      TIM4PWM2Update(0);
    }


	  //Non DMA atm program WILL hang with no UART input
	  thermalRegulator.getCurrentTemperature();
    //thermalRegulator.correctProcess();
	  s = std::to_string(uwTick);
    s += ", ";
    s += std::to_string(thermalRegulator.DEBUGgetCurrentTemperature());
    s += "\r\n";
    CDC_Transmit_FS(reinterpret_cast<uint8_t*>(s.data()), s.size());

    /*
    s = std::to_string(thermalRegulator.DEBUGgetDt());
    s += "\r\n";
    CDC_Transmit_FS(reinterpret_cast<uint8_t*>(s.data()), s.size());
    sleep(100);
     */
	}
}

void CDC_ReceiveCallBack(uint8_t *buf, uint32_t len)
{
	Event e = Frame::bufferToEvent(buf);
	cBuf.put(e);
}

void Error_Handler(void)
{
	/* USER CODE BEGIN Error_Handler_Debug */
	/* User can add his own implementation to report the HAL error return state */
	__disable_irq();
	while (1)
	{

	}
	/* USER CODE END Error_Handler_Debug */
}


void assert_failed(uint8_t *file, uint32_t line)
{
	printf("Assert failed: file %s on line %d\r\n", file, line);
}

