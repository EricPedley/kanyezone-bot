import win32gui
import win32ui
import win32con
from ctypes import windll
from PIL import Image
import ctypes
import numpy as np

#window_name = "Don't let Kanye into his zone: Kanye Zone - Google Chrome"

def getWindowScreenshotWithAlpha(window_name):
    hwnd_target = win32gui.FindWindow(None, window_name)

    left, top, right, bot = win32gui.GetWindowRect(hwnd_target)
    w = right - left
    h = bot - top
    win32gui.SetForegroundWindow(hwnd_target)
    hdesktop = win32gui.GetDesktopWindow()
    hwndDC = win32gui.GetWindowDC(hdesktop)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (left, top), win32con.SRCCOPY)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    # im = Image.frombuffer(
    #     'RGB',
    #     (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    #     bmpstr, 'raw', 'BGRX', 0, 1)
    im = np.fromstring(bmpstr, dtype='uint8')
    im.shape = (bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hdesktop, hwndDC)
    if result == None:
        #PrintWindow Succeeded
        return im

def getWindowScreenshot(window_name):
    img = getWindowScreenshotWithAlpha(window_name)
    img = img[0:,0:,0:3]
    return img