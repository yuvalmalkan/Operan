import logging
import mss
import pyautogui
import Constants
import base64
import io
from PIL import Image



class Screen:
    _scale_factor = None

    @classmethod
    def get_scale_factor(cls) -> float:
        if cls._scale_factor is not None:
            return cls._scale_factor

        logical_width, _ = pyautogui.size()
        screenshot = pyautogui.screenshot()
        pixel_width, _ = screenshot.size

        cls._scale_factor = max(1.0, pixel_width / logical_width)

        logging.info(f"Calculated display scale factor: {cls._scale_factor}x")
        return cls._scale_factor

    @staticmethod
    def adjust_coordinates(x: int, y: int, scale_factor: float) -> tuple[int, int]:
        if scale_factor > 1:
            adjusted_x = int(round(x / scale_factor))
            adjusted_y = int(round(y / scale_factor))

            logging.debug(f"Adjusted coordinates from ({x}, {y}) to ({adjusted_x}, {adjusted_y})")

            return adjusted_x, adjusted_y

        return x, y


    @staticmethod
    def GetCurrentScreen() -> str:
        #get current screen as base64
        try:
            with mss.mss() as screenshot:
                monitor = screenshot.monitors[1]
                captured_screen = screenshot.grab(monitor)
                
                img = Image.frombytes("RGB", captured_screen.size, captured_screen.bgra, "raw", "BGRX")
            
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")

                base64_encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
                
                logging.info("Screenshot successfully captured to memory as Base64")

                return base64_encoded
                
        except Exception as error:
            logging.error(f"Failed to capture screen to memory: {error}")
            return ""