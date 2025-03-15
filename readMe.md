The architecture described in the material involves structuring the software into different levels (L1, L2, L3) and ensuring proper communication between hardware and software components. Below is a detailed breakdown of how to design the software:

## 1. Software Architecture Overview

The software architecture is divided into three levels:

    Level 1 (L1): Hardware-specific programs that directly interact with sensors and actuators.

    Level 2 (L2): Logic-defining programs that process data from L1 and send commands to actuators.

    Level 3 (L3): High-level mission control programs that coordinate the overall behavior of the robot.

## 2. Level 1 (L1) Programs

These programs are responsible for direct communication with the hardware. For the Raspberry Pi 4, We will used libraries like gpiozero for GPIO control and pysicktim for LIDAR communication.

### L1 Programs:

   - L1_motor.py: Controls the motor drivers by generating PWM signals.

   - L1_encoder.py: Reads data from wheel encoders.

   - L1_lidar.py: Communicates with the LIDAR sensor to get distance measurements.

   - L1_gamepad.py: Reads input from the gamepad controller.

   - L1_camera.py: Captures images from the USB camera.

   - L1_mpu.py: Reads data from the IMU (MPU9250) for orientation and motion data.

   - L1_bmp.py: Reads temperature and pressure data from the BMP280 sensor.

   - L1_adc.py: Reads voltage data from the ADC sensor.

## 3. Level 2 (L2) Programs

These programs process data from L1 and generate commands for actuators. They handle the logic for tasks like kinematics, speed control, and obstacle detection.

### L2 Programs:

   - L2_kinematics.py: Computes chassis movement based on wheel encoder data.

   - L2_speed_control.py: Generates wheel duty cycle commands based on desired speed.

   - L2_inverse_kinematics.py: Computes wheel vectors for desired movement.

   - L2_obstacle.py: Processes LIDAR data to detect obstacles.

   - L2_track_target.py: Processes camera data to track a target.

   - L2_onboard.py: Computes battery and environmental data from BMP280 and ADC sensors.

   - L2_log.py: Handles data logging for debugging and analysis.

## 4. Level 3 (L3) Programs

These programs coordinate the overall mission of the robot. They receive data from L2 programs and send high-level commands.
### L3 Programs:

    L3_drive_mt.py: Multithreaded driving program that coordinates movement based on gamepad input or autonomous commands.

    L3_follow.py: Autonomous program for following a target using camera data.

    L3_avoid_obstacles.py: Autonomous program for obstacle avoidance using LIDAR data.

## 5. Multithreading

To ensure smooth operation, especially for tasks like driving, obstacle detection, and audio feedback, multithreading is essential. Each thread should handle a specific task, such as:

    Thread 1: Driving the robot based on gamepad input or autonomous commands.

    Thread 2: Obstacle detection using LIDAR data.

    Thread 3: Audio feedback or text-to-speech output.

## 6. Libraries and Dependencies

For the Raspberry Pi 4, you will use the following libraries:

    gpiozero: For GPIO control.

    pysicktim: For LIDAR communication.

    numpy: For mathematical operations.

    pygame: For gamepad input.

    fastlogging: For logging data.

    smbus2: For I2C communication with sensors like BMP280 and MPU9250.


## Folder Structure
scuttle_robot/
├── L1/                  # Level 1: Hardware-specific programs
│   ├── L1_motor.py
│   ├── L1_encoder.py
│   ├── L1_lidar.py
│   ├── L1_gamepad.py
│   ├── L1_camera.py
│   ├── L1_mpu.py
│   ├── L1_bmp.py
│   └── L1_adc.py
├── L2/                  # Level 2: Logic-defining programs
│   ├── L2_kinematics.py
│   ├── L2_speed_control.py
│   ├── L2_inverse_kinematics.py
│   ├── L2_obstacle.py
│   ├── L2_track_target.py
│   ├── L2_onboard.py
│   └── L2_log.py
├── L3/                  # Level 3: Mission control programs
│   ├── L3_drive_mt.py
│   ├── L3_follow.py
│   ├── L3_avoid_obstacles.py
│   └── L3_mission_control.py
├── utils/               # Utility functions and shared resources
│   ├── constants.py
│   └── logger.py
└── main.py              # Entry point for the system