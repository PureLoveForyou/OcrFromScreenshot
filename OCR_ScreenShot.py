import pytesseract
# from PIL import Image
import PIL.ImageGrab
import pyperclip
import pyautogui
import time
import keyboard
from winotify import Notification, audio

# call windows notification
def notification(content="Recognition finished...\nPress Esc to exit completely..."):
    toast = Notification(
        app_id="ScreenShot OCR",
        title="ScreenShot OCR",
        msg=content,
        duration="short",
        icon=r"E:\Documents\Code\Python\OCR\fromScreenShot\ocr.ico")

    toast.set_audio(audio.Default, loop=False)
    toast.show()

def takeScreenshot():
    # take screenshot
    # im = PIL.ImageGrab.grab()

    # record original clipboard content
    start_clip = pyperclip.paste()

    pyautogui.hotkey('winleft', 'shift','s') # windows screenshot hotkey

    # wait for screenshot to complete
    count = 0
    while(True):
        count += 1
        # test if new image is coming
        end_clip = pyperclip.paste()
        if end_clip != start_clip:
            break

        time.sleep(0.4)
        if count >= 20: # after 20*0.4 = 8 seconds, still no image, then exit
            break
    OCR()


def OCR():
    print('Recognition started...')
    try:
        # grab picture from clipboard
        image = PIL.ImageGrab.grabclipboard()
        # image.show()

        # image = Image.open('ocr.png')
        text = pytesseract.image_to_string(image, lang='chi_sim')
        # text = pytesseract.image_to_string(image, lang='eng')
        print('Result: \n', text)

        notification()

        pyperclip.copy(text)
    except:
        # if clipboard has no image, then don't do it
        pass


if __name__ == "__main__":
    # # add to system tray
    # import pystray
    # import PIL.Image

    # image = PIL.Image.open("ocr.ico")

    # def on_cLicked(icon, item):
    #     if str(item) == 'Screenshot to recognize':
    #         takeScreenshot()
    #     elif(str(item)=='Exit'):
    #         pyautogui.hotkey('esc')
    #         icon.stop()

    # icon = pystray.Icon("OCR", image, menu=pystray.Menu(
    #     pystray.MenuItem("Screenshot to recognize", on_cLicked),
    #     pystray.MenuItem('Exit', on_cLicked)))
    # icon.run()

    # main body
    notification('Press win + shift to start...\nPress Esc to exit')
    # Loop. Wait for hotkey to recognize
    keyboard.add_hotkey('win + shift', callback=takeScreenshot)
    keyboard.wait('esc') # press esc to exit
    notification('OCR has totally exit. Restart it if you want to use again...')