import pyautogui
import logging
from functools import wraps
import Constants

def failsafe_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pyautogui.FailSafeException:
            logging.error(f"Failsafe triggered during '{func.__name__}'! Mouse moved to a corner. Aborting action.")
            raise
    return wrapper

class Mouse:
    def __init__(self):
        logging.info("Mouse controller initialized.")

    @failsafe_handler
    def move(self, x: int, y: int, duration: float = Constants.DEFAULT_MOUSE_DURATION):
        pyautogui.moveTo(x, y, duration=duration)
        logging.info(f"Mouse successfully moved to ({x}, {y}).")

    @failsafe_handler
    def click(self, button: str = 'left'):
        pyautogui.click(button=button, clicks=1)
        logging.info(f"Performed single '{button}' click.")

    @failsafe_handler
    def double_click(self, button: str = 'left', interval: float = Constants.DEFAULT_DOUBLE_CLICK_INTERVAL):
        pyautogui.click(button=button, clicks=2, interval=interval)
        logging.info(f"Performed double '{button}' click.")