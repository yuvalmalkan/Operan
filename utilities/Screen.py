import logging
import mss
import mss.tools
import pyautogui
import Constants


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
    def take_screenshot(output_filename: str = Constants.DEFAULT_SCREENSHOT_NAME) -> str:
        try:
            with mss.mss() as screenshot:
                monitor = screenshot.monitors[1]
                captured_screen = screenshot.grab(monitor)

                mss.tools.to_png(
                    captured_screen.rgb,
                    captured_screen.size,
                    output=output_filename,
                )

            logging.info("Screenshot successfully saved to: %s", output_filename)
            return output_filename
        
        except OSError as error:
            logging.error("Failed to capture the macOS screen: %s", error)
            return ""
