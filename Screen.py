import pyautogui
import logging

class Screen:
    @staticmethod
    def get_scale_factor():
        """
        Detects if the screen uses a high-DPI scaling factor.
        Compares the logical screen size with the actual pixel resolution of a screenshot.
        
        Returns:
            int: The scaling factor (e.g., 1 for standard, 2 for Retina displays).
        """
        # Logical size reported by the OS
        logical_width, _ = pyautogui.size()
        
        # Actual pixel size of a screenshot
        screenshot = pyautogui.screenshot()
        pixel_width, _ = screenshot.size
        
        # Calculate the ratio
        scale_factor = round(pixel_width / logical_width)
        
        # Ensure it never returns less than 1
        scale_factor = max(1, scale_factor)
        
        logging.info(f"Logical width: {logical_width}, Pixel width: {pixel_width}. Scale factor: {scale_factor}x")
        return scale_factor

    @staticmethod
    def adjust_coordinates(x, y, scale_factor):
        """
        Adjusts raw pixel coordinates into logical coordinates for the OS mouse controller.
        
        Args:
            x (int): Raw X pixel coordinate.
            y (int): Raw Y pixel coordinate.
            scale_factor (int): The display scale factor.
            
        Returns:
            tuple: Adjusted (x, y) logical coordinates.
        """
        if scale_factor > 1:
            adjusted_x = x // scale_factor
            adjusted_y = y // scale_factor
            logging.debug(f"Adjusted coordinates from ({x}, {y}) to ({adjusted_x}, {adjusted_y})")
            return adjusted_x, adjusted_y
        
        return x, y