import logging
import pyautogui
from Command import Command
from Mouse import Mouse
from Screen import Screen
import Constants

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

pyautogui.FAILSAFE = True

def main():
    logging.info("Starting automation process...")

    success = Command.open_application(Constants.TARGET_APP_NAME)
    if not success:
        logging.error(f"Failed to open '{Constants.TARGET_APP_NAME}'. Exiting.")
        return

    screenshot_path = Screen.take_screenshot()
    if screenshot_path:
        logging.info(f"Screenshot taken: {screenshot_path}")

    scale = Screen.get_scale_factor()
    x, y = Screen.adjust_coordinates(Constants.CALC_BUTTON_X, Constants.CALC_BUTTON_Y, scale)
    
    mouse = Mouse()
    mouse.move(x, y)
    mouse.click()

    logging.info("Automation process completed successfully.")

if __name__ == "__main__":
    main()