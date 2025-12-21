# space-motion-shooter
![Unity](https://img.shields.io/badge/Unity-Game_Engine-black?logo=unity&logoColor=white)
![C#](https://img.shields.io/badge/C%23-Scripting-239120?logo=c-sharp&logoColor=white)
![C](https://img.shields.io/badge/C-Firmware-00599C?logo=c&logoColor=white)
![STM32](https://img.shields.io/badge/STM32-Hardware-03234B?logo=stmicroelectronics&logoColor=white)
![UART](https://img.shields.io/badge/UART-Serial_Comm-red)
![Kalman Filter](https://img.shields.io/badge/Algorithm-Kalman_Filter-FF6F00)

## Scope of the Project
This project aims to develop an intuitive Unity space-shooter game that employs the microcontroller as a motion controller. The microcontroller's onboard accelerometer was utilized to measure motion and estimate tilt angles. These measurements were processed using a Kalman filter to reduce noise and enhance accuracy. Real-time communication with Unity was facilitated via UART, enabling seamless gameplay interactions. Additionally, a pushbutton interrupt allows the player to fire weapons in the game, accompanied by sound effects generated through a DAC speaker.

## Meet the Team
- Namir Habib: U3 Computer Engineering
- Thibaut Chan Teck Su: U3 Computer Engineering
- Haoyuan Sun: U3 Computer Engineering
- Faiza Chowdhury: U4 Computer Engineering

## How to Run the Program

1. **Connect the Microcontroller**  
   Connect the STM B-L475E-IOT01A microcontroller to your device via USB.

2. **Check the COM Port**  
   Ensure that the microcontroller is recognized as a Virtual COM Port (COM5).

3. **Flash the Firmware**  
   - Open the `main.c` file located at `firmware/stm32-final-project/Core/Src/`.  
   - Write the code onto the microcontroller using your preferred IDE (e.g., STM32CubeIDE).  
   - Ensure the program is successfully flashed onto the microcontroller.

4. **Launch the Game**  
   Navigate to the `game/` directory and open the game file to start the program.
