import logging
from functools import wraps

import pyautogui

import Constants


def failsafe_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except pyautogui.FailSafeException:
            logging.error(
                "Failsafe triggered during '%s'. Mouse moved to a corner; "
                "aborting action.",
                func.__name__,
            )
            raise

    return wrapper


class Mouse:
    def __init__(self):
        logging.info("macOS mouse controller initialized.")

    @failsafe_handler
    def move(
        self,
        x: int,
        y: int,
        duration: float = Constants.DEFAULT_MOUSE_DURATION,
    ):
        pyautogui.moveTo(x, y, duration=duration)
        logging.info("Mouse successfully moved to (%s, %s).", x, y)

    @failsafe_handler
    def click(self, button: str = "left"):
        pyautogui.click(button=button, clicks=1)
        logging.info("Performed single '%s' click.", button)

    @failsafe_handler
    def double_click(
        self,
        button: str = "left",
        interval: float = Constants.DEFAULT_DOUBLE_CLICK_INTERVAL,
    ):
        pyautogui.click(button=button, clicks=2, interval=interval)
        logging.info("Performed double '%s' click.", button)
