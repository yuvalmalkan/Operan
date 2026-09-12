import logging
import pyautogui
from Command import Command
from Mouse import Mouse
from Screen import Screen
import Constants


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
)

pyautogui.FAILSAFE = True


def main():
    logging.info("Starting automation process...")

    if not Command.open_application(Constants.TARGET_APP_NAME):
        logging.error("Failed to open '%s'. Exiting.", Constants.TARGET_APP_NAME)
        return

    screenshot_path = Screen.take_screenshot()
    if screenshot_path:
        logging.info("Screenshot taken: %s", screenshot_path)

    scale = Screen.get_scale_factor()
    x, y = Screen.adjust_coordinates(
        Constants.CALC_BUTTON_X,
        Constants.CALC_BUTTON_Y,
        scale,
    )

    mouse = Mouse()
    mouse.move(x, y)
    mouse.click()
    logging.info("automation process completed successfully.")


if __name__ == "__main__":
    main()