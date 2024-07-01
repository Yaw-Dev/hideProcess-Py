import sys
import platform
import ctypes
from ctypes import wintypes
import win32api
import win32con

import time

def hide_process():
    is_64bit_os = platform.machine().endswith('64')
    ptr_size = ctypes.sizeof(ctypes.c_void_p)

    if is_64bit_os and ptr_size != 4:
        hMod = win32api.LoadLibrary("hyde64.dll")
    elif not is_64bit_os and ptr_size == 4:
        hMod = win32api.LoadLibrary("hyde.dll")
    else:
        sys.exit("Incompatible architecture")

    if hMod:
        CBProc_addr = win32api.GetProcAddress(hMod, "CBProc")
        if not CBProc_addr:
            sys.exit("Failed to get CBProc address")

        CBProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)(CBProc_addr)

        WH_CBT = win32con.WH_CBT
        hMod_cast = ctypes.cast(hMod, wintypes.HMODULE)
        hHook = ctypes.windll.user32.SetWindowsHookExW(WH_CBT, CBProc, hMod_cast, 0)
        if not hHook:
            sys.exit("Failed to set the hook")
    else:
        sys.exit("Failed to load library")


hide_process() # UAC elevation is required!
while True:
    print("keep alive...")
    time.sleep(0.5)