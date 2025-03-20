from L3.L3_mission_control import MissionControl
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.DEBUG)

def main():
    try:
        mission_control = MissionControl()
        mission_control.start_mission()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()