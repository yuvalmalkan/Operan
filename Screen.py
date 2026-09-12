import pyautogui
import logging
import mss
import mss.tools

class Screen:
    _scale_factor = None

    @classmethod
    def get_scale_factor(cls) -> int:
        # Use cached value if already computed
        if cls._scale_factor is not None:
            return cls._scale_factor

        logical_width, _ = pyautogui.size()
        screenshot = pyautogui.screenshot()
        pixel_width, _ = screenshot.size
        
        scale_factor = round(pixel_width / logical_width)
        cls._scale_factor = max(1, scale_factor)
        
        logging.info(f"Calculated Scale factor: {cls._scale_factor}x")
        return cls._scale_factor

    @staticmethod
    def adjust_coordinates(x: int, y: int, scale_factor: int) -> tuple[int, int]:
        if scale_factor > 1:
            adjusted_x = x // scale_factor
            adjusted_y = y // scale_factor
            logging.debug(f"Adjusted coordinates from ({x}, {y}) to ({adjusted_x}, {adjusted_y})")
            return adjusted_x, adjusted_y
        
        return x, y

    @staticmethod
    def take_screenshot(output_filename: str = "current_screen.png") -> str:
        try:
            with mss.MSS() as sct:
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
                
                logging.info(f"Screenshot successfully saved to: {output_filename}")
                return output_filename
                
        except Exception as e:
            logging.error(f"Failed to capture screen using mss: {e}")
            return ""