import pyautogui
import logging
import time
from Screen import Screen

class Mouse:
    def __init__(self, failsafe=True):
        """
        Initializes the Mouse controller.
        
        Args:
            failsafe (bool): If True, moving the mouse to a screen corner aborts execution.
        """
        pyautogui.FAILSAFE = failsafe
        logging.info(f"Mouse controller initialized. Failsafe enabled: {failsafe}")



    def move(self, x, y, duration=0.5):
        """
        Moves the mouse cursor to the specified logical (x, y) coordinates.
        """
        try:
            pyautogui.moveTo(x, y, duration=duration)
            logging.info(f"Mouse successfully moved to ({x}, {y}).")
        except pyautogui.FailSafeException:
            logging.error("Failsafe triggered! Mouse moved to a corner. Aborting movement.")



    def click(self, button='left'):
        """
        Performs a single mouse click at the current cursor location.
        """
        try:
            pyautogui.click(button=button, clicks=1)
            logging.info(f"Performed single '{button}' click.")
        except pyautogui.FailSafeException:
            logging.error("Failsafe triggered! Mouse moved to a corner. Aborting click.")



    def double_click(self, button='left', interval=0.1):
        """
        Performs a double mouse click at the current cursor location.
        
        Args:
            button (str): The mouse button to click ('left', 'middle', 'right').
            interval (float): Time in seconds between the two clicks.
        """
        try:
            pyautogui.click(button=button, clicks=2, interval=interval)
            logging.info(f"Performed double '{button}' click.")
        except pyautogui.FailSafeException:
            logging.error("Failsafe triggered! Mouse moved to a corner. Aborting double click.")





# Example usage/testing block
if __name__ == "__main__":
    # Configure logging for the test run
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    logging.info("Starting test in 3 seconds...")
    time.sleep(3)
    
    # Initialize the Mouse controller
    mouse_controller = Mouse()
    
    # Use the Screen class to handle resolution scaling
    current_scale = Screen.get_scale_factor()
    
    # Mock AI target pixels
    ai_vision_x, ai_vision_y = 1000, 800
    
    # Adjust and execute
    target_x, target_y = Screen.adjust_coordinates(ai_vision_x, ai_vision_y, current_scale)
    
    mouse_controller.move(target_x, target_y, duration=0.8)
    time.sleep(0.2)
    
    # Test the new double click
    mouse_controller.double_click(button='left')