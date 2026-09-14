import ollama
from Constants import *
import json
from utilities.Screen import get_scale_factor, adjust_coordinates

currentScreen = DEFAULT_SCREENSHOT_NAME


def GetCords(target: str) -> tuple[int, int]:
    #ollama gets current screen and returns the cords of an object in tuple

    prompt = f"""
        Look at the attached screenshot of the current screen interface.
        this is what the user requested, find the coordinates of it: "{target}"
        Return ONLY a valid JSON object containing where the button/text is located.
        try to be as precise as possible.
        Example output: "x": "400" , "y": "234"
        """
    
    response = ollama.chat(
    model='llava-phi3',
    format='json',
    messages=[
        {
            'role': 'user',
            'content': prompt,
            'images': [currentScreen]
        }])
    

    result = response['message']['content']

    try:
        data = json.loads(result)
        x = data.get('x')
        y = data.get('y')
        scale = get_scale_factor()
        x,y = adjust_coordinates(x,y,scale)

        return x,y
        
    except json.JSONDecodeError:
        print("Failed to parse json try again")
    