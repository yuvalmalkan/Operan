import Command as Command
import Mouse as Mouse
from Screen import *


commander = Command.Command()
app = commander.open_application('Calculator')


screenshot = Screen.take_screenshot()

mouse = Mouse.Mouse()
scale = Screen.get_scale_factor()
x,y = Screen.adjust_coordinates(100,323,scale)
mouse.move(x,y)
mouse.click()