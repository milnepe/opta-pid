#include <PortentaEthernet.h>
#include "PID_v2.h"
arduino::EthernetClass eth(&m_netInterface);
double Kp = 2, Ki = 5, Kd = 1;
PID_v2 myPID(Kp, Ki, Kd, PID::Reverse);
unsigned long windowStartTime;

void setup() {
	IPAddress ip(192, 168, 1, 40);
	IPAddress dns(192, 168, 1, 254);
	IPAddress gateway(192, 168, 1, 254);
	IPAddress subnet(255, 255, 255, 0);
	eth.begin(ip, dns, gateway, subnet);
    delay(5000);
    windowStartTime = millis();
    myPID.SetOutputLimits(0, 5000);
    myPID.Start(PLCOut.out_temperature, 0, 100);
}

void loop()
{
    const double input = PLCOut.out_temperature;
    const double Kp = PLCOut.out_kp;
    const double Ki = PLCOut.out_ki;
    const double Kd = PLCOut.out_kd;
    const int WindowSize = PLCOut.out_windowsize;    
    const double setpoint = PLCOut.out_setpoint;

    myPID.SetOutputLimits(0, WindowSize);
    myPID.Setpoint(setpoint);
    myPID.SetTunings(Kp, Ki, Kd);    
    const double output = myPID.Run(input);
    PLCIn.in_output = output;

    while (millis() - windowStartTime > WindowSize) {
        windowStartTime += WindowSize;
    }
    unsigned long window = millis() - windowStartTime;
    PLCIn.in_window = window;
    if (output < window)
        PLCIn.in_heater = true;
    else
        PLCIn.in_heater = false;
}

