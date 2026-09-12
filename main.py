import logging
import pyautogui
import time
from Command import Command
from Mouse import Mouse
from Screen import Screen

# הגדרת לוגר מרכזית עבור כל הפרויקט
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)

# הגדרות גלובליות של הסביבה (במקום לשנות מצב בתוך המחלקה של העכבר)
pyautogui.FAILSAFE = True

# קבועים (Magic Numbers Extraction)
TARGET_APP_NAME = 'Calculator'
CALC_BUTTON_X = 100
CALC_BUTTON_Y = 323
WAIT_TIME_APP_LOAD = 2.0

def main():
    logging.info("Starting automation process...")

    # פתיחת האפליקציה ברקע (Non-blocking)
    success = Command.open_application(TARGET_APP_NAME)
    if not success:
        logging.error(f"Failed to open '{TARGET_APP_NAME}'. Exiting.")
        return

    # המתנה קלה כדי שהאפליקציה תספיק לעלות לפני שמצלמים מסך ולוחצים
    logging.info("Waiting for the application to load...")
    time.sleep(WAIT_TIME_APP_LOAD)

    # צילום מסך
    screenshot_path = Screen.take_screenshot()
    if screenshot_path:
        logging.info(f"Screenshot taken: {screenshot_path}")

    # חישוב קנה מידה והתאמת קואורדינטות
    scale = Screen.get_scale_factor()
    x, y = Screen.adjust_coordinates(CALC_BUTTON_X, CALC_BUTTON_Y, scale)
    
    # הפעלת העכבר
    mouse = Mouse()
    mouse.move(x, y)
    mouse.click()

    logging.info("Automation process completed successfully.")

if __name__ == "__main__":
    main()