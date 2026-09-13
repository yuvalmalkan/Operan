import pyautogui
import json
import ollama
from utilities.Screen import Screen

def GetCords(target: str, base64_image: str) -> tuple[int, int]:
    # Requesting normalized coordinates (0.0 to 1.0) to avoid hardcoded physical pixels
    prompt = f"""
        Look at the attached screenshot of the entire screen.
        First, locate the macOS Calculator application window. 
        Then, find the exact location of the "{target}" ONLY inside the Calculator application.
        Strictly ignore any numbers, text, or elements outside of the Calculator window (such as the terminal, menu bar, or background).
        Return ONLY a valid JSON object containing the normalized coordinates (between 0.0 and 1.0) for the center of the target.
        Example output: {{"x": 0.453, "y": 0.821}}
        """
    
    response = ollama.chat(
        model='llava-phi3',
        format='json',
        messages=[
            {
                'role': 'user',
                'content': prompt,
                'images': [base64_image]
            }
        ]
    )

    result = response['message']['content']

    try:
        data = json.loads(result)
        norm_x = data.get('x')
        norm_y = data.get('y')
        
        # Fetch logical resolution via pyautogui
        logical_width, logical_height = pyautogui.size()
        scale = Screen.get_scale_factor()
        
        # Calculate physical pixels by applying the scale factor to the logical resolution,
        # then multiplying by the normalized ratio provided by the model
        physical_x = int(norm_x * (logical_width * scale))
        physical_y = int(norm_y * (logical_height * scale))
        
        # Use the custom adjustment function to translate physical coordinates back to logical mouse coordinates
        final_x, final_y = Screen.adjust_coordinates(physical_x, physical_y, scale)

        return final_x, final_y
        
    except json.JSONDecodeError:
        print("Failed to parse JSON, try again")
        return -1, -1