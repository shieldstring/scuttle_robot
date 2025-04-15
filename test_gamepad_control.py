import time
import logging
from L1.L1_gamepad import Gamepad
from L1.L1_motor import MotorController
from L2.L2_kinematics import Kinematics
from utils.constants import WHEELBASE, MAX_SPEED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test')

def main():
    try:
        logger.info("Initializing systems...")
        gamepad = Gamepad()
        motors = MotorController()
        kin = Kinematics(WHEELBASE)
        
        logger.info("System ready! Use left stick to move. Press any button to stop.")
        
        while True:
            # Check for exit button
            pygame.event.pump()
            if any(gamepad.joystick.get_button(i) for i in range(gamepad.joystick.get_numbuttons())):
                logger.info("Stop button pressed")
                break
            
            # Get gamepad input
            x, y = gamepad.get_input()
            
            # Convert to robot commands
            linear = y * MAX_SPEED  # Forward/back
            angular = x * 1.0       # Rotation rate
            
            # Compute wheel speeds
            speeds = kin.compute_wheel_speeds(linear, angular)
            
            # Send to motors
            motors.set_speed(speeds)
            
            time.sleep(0.02)  # 50Hz control loop
            
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        motors.stop()
        logger.info("Motors stopped")

if __name__ == "__main__":
    main()