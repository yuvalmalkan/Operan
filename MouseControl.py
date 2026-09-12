import pyautogui
import time

# Failsafe mechanism: Move the mouse to any corner of the screen to abort execution
pyautogui.FAILSAFE = True

def move_mouse(x, y, duration=0.5):
    """
    Moves the mouse cursor to the specified (x, y) coordinates on the screen.
    
    Args:
        x (int): The x-coordinate target.
        y (int): The y-coordinate target.
        duration (float): The time in seconds it takes to move the mouse. 
                          Setting this > 0 helps the movement look human-like.
    """
    try:
        # Move the mouse smoothly to the target
        pyautogui.moveTo(x, y, duration=duration)
        print(f"Mouse successfully moved to ({x}, {y}).")

    except pyautogui.FailSafeException:
        print("Failsafe triggered! Mouse moved to a corner. Aborting movement.")

def click_mouse(button='left', clicks=1, interval=0.1):
    """
    Performs a mouse click at the current cursor location.
    
    Args:
        button (str): The mouse button to click ('left', 'middle', or 'right').
        clicks (int): Number of clicks to perform (1 for single click, 2 for double).
        interval (float): Time in seconds between clicks if clicks > 1.
    """
    try:
        # Perform the click action
        pyautogui.click(button=button, clicks=clicks, interval=interval)
        print(f"Performed {clicks} '{button}' click(s) at current location.")


    except pyautogui.FailSafeException:
        print("Failsafe triggered! Mouse moved to a corner. Aborting click.")



if __name__ == "__main__":
    # Short delay to allow you to switch windows before the script runs
    print("Starting in 3 seconds...")
    time.sleep(3)
    
    # Get the current screen resolution
    screen_width, screen_height = pyautogui.size()
    print(f"Screen resolution detected: {screen_width}x{screen_height}")
    
    # Define a target coordinate (e.g., the center of the screen)
    target_x = screen_width // 2
    target_y = screen_height // 2
    
    # 1. AI decides to move the mouse
    move_mouse(target_x, target_y)
    
    # Short pause to simulate human reaction time between moving and clicking
    time.sleep(0.2)
    
    # 2. AI decides to click
    click_mouse(button='left')