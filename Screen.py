import pyautogui
import logging
import mss
import mss.tools
from PIL import Image

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class Screen:
    """
    Handles screen capture operations and coordinate scaling for high-DPI displays (e.g., Retina).
    """

    @staticmethod
    def get_scale_factor() -> int:
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
    def adjust_coordinates(x: int, y: int, scale_factor: int) -> tuple[int, int]:
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

    @staticmethod
    def take_screenshot(output_filename: str = "current_screen.png") -> str:
        """
        Captures the primary monitor using the fast 'mss' library.
        
        Args:
            output_filename (str): The destination path for the saved image.
            
        Returns:
            str: The path to the saved screenshot, or an empty string if it fails.
        """
        try:
            with mss.MSS() as sct:
                # Get information of monitor 1 (primary monitor)
                monitor = sct.monitors[1]
                
                # Grab the data
                sct_img = sct.grab(monitor)
                
                # Save to the picture file
                mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
                
                logging.info(f"Screenshot successfully saved to: {output_filename}")
                return output_filename
                
        except Exception as e:
            logging.error(f"Failed to capture screen using mss: {e}")
            return ""

if __name__ == "__main__":
    print("\n--- Testing Screen Class ---")
    
    # 1. Test Scale Factor Detection
    scale = Screen.get_scale_factor()
    print(f"Detected Scale Factor: {scale}")
    
    # 2. Test Coordinate Adjustment
    test_x, test_y = 1000, 500
    adj_x, adj_y = Screen.adjust_coordinates(test_x, test_y, scale)
    print(f"Raw coordinates: ({test_x}, {test_y}) -> Adjusted for mouse: ({adj_x}, {adj_y})")
    
    # 3. Test Screen Capture
    capture_path = Screen.take_screenshot("test_capture_mss.png")
    print(f"Capture result path: {capture_path}")