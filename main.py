from mss import mss  # Screen capture
import cv2  # Image processing
import time  # Time
import serial  # Serial communication
import pyautogui  # Mouse and keyboard control
from gym import Env  # Gym environment
import numpy as np  # Numpy
from PIL import Image
import pytesseract  # OCR (Optical Character Recognition)
import os


# Debug : found ressources position
# screen positions (for top right to "wind" button of pycharm)
# while True:
#     print(pyautogui.position())  # Print mouse position
#     time.sleep(0.3)


class CocGF(Env):
    def __init__(self):
        self.capture = mss()
        self.game_location = {"top": 128, "left": 673, "width": 80, "height": 85}  # full
        # self.gold_location = {"top": 128, "left": 678, "width": 80, "height": 20}  # gold
        # self.elixir_location = {"top": 154, "left": 678, "width": 80, "height": 20}  # elixir
        # self.dark_location = {"top": 181, "left": 678, "width": 80, "height": 20}  # dark elixir
        self.minRessources = 600000  # Minimum ressources of any type to stop searching
        self.ser = serial.Serial('COM3', 9600)

    def get_ressources(self, minRessources):
        ressources = np.array(self.capture.grab(self.game_location))
        res = pytesseract.image_to_string(Image.fromarray(ressources))
        res = res.replace(" ", "")
        res = ''.join(i for i in res if i.isdigit() or i == '\n')
        res = res.split('\n')
        res = list(filter(None, res))

        # debug
        # cv2.imshow("Captured Image", ressources)
        # cv2.waitKey(0)
        # end debug

        # if any value in result is higher than minRessources, send 0 to arduino
        if any(int(i) > minRessources for i in res):
            return 0, res
        else:
            return 1, res

        # Gold capture
        # gold_capture = np.array(self.capture.grab(self.gold_location))
        # gold_img = Image.fromarray(gold_capture)
        # gold_img.save("temp_screen.png")
        # os.system("tesseract temp_screen.png stdout")
        # os.remove("temp_screen.png")
        #
        # # Elixir capture
        # elixir_capture = np.array(self.capture.grab(self.elixir_location))
        # elixir_img = Image.fromarray(elixir_capture)
        # elixir_img.save("temp_screen.png")
        # os.system("tesseract temp_screen.png stdout")
        # os.remove("temp_screen.png")
        #
        # # Dark elixir capture
        # dark_capture = np.array(self.capture.grab(self.dark_location))
        # dark_img = Image.fromarray(dark_capture)
        # dark_img.save("temp_screen.png")
        # os.system("tesseract temp_screen.png stdout")
        # os.remove("temp_screen.png")


if __name__ == "__main__":
    env = CocGF()
    if not env.ser.isOpen():
        env.ser.open()
    print(f"COM3 open : {env.ser.isOpen()}\n[WAIT] 4s before beginning...")
    time.sleep(4)

    # Arduino communication
    while True:
        result, ressources = env.get_ressources(env.minRessources)
        if result == 1:
            env.ser.write(b'1')
            print(f"[{result}] Insufficient ressources ({ressources})")
            time.sleep(8)
        else:
            print(f"[{result}] Game found ! ({ressources})")
            env.close()
            break
