import time
import random
import os
import winreg
from configs.logger import logger
from activities.apps.native_apps.base import NativeApp

class MicrosoftWord(NativeApp):
    def __init__(self):
        super().__init__()
        self.window_info = "[CLASS:OpusApp]"
        
    def _get_executable_path(self):
        registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\winword.exe", 0, winreg.KEY_READ)
        path, _ = winreg.QueryValueEx(registry_key, None)
        if path:
            return path
        return None 
        
    def check_existing_window(self):
        logger.info("Checking existing Microsoft Word window")
        if self.dll.AU3_WinExists(self.window_info, ""):
            logger.info("Activating Microsoft Word window")
            self.dll.AU3_WinActivate(self.window_info, "")
            logger.info("Waiting Microsoft Word window to be active")
            if not self.dll.AU3_WinWaitActive(self.window_info, "", 10):
                return "could not activate Microsoft Word window"
        else:
            return "Microsoft Word window didn't exist"
        
        return None
        
    def create_window(self):
        logger.info("Getting Microsoft Word executable path")
        executable_path = self._get_executable_path()
        if not executable_path:
            return "could not get Microsoft Word executable path"
        
        logger.info("Creating new Microsoft Word window")
        if not self.dll.AU3_Run(executable_path, "", 1):
            return "could not run Microsoft Word"

        time.sleep(2)
        logger.info("Checking existing Microsoft Word window")
        if self.dll.AU3_WinExists(self.window_info, ""):
            logger.info("Getting Microsoft Word window handle")
            handle = self.dll.AU3_WinGetHandle(self.window_info, "")
            if not handle:
                return "could not get window handle"
            else:
                self.window_info = "[HANDLE:%s]" % f"{handle:08X}" 
            logger.info("Activating Microsoft Word window")
            self.dll.AU3_WinActivate(self.window_info, "")
            logger.info("Waiting Microsoft Word window to be active")
            if not self.dll.AU3_WinWaitActive(self.window_info, "", 10):
                return "could not activate Microsoft Word"
        else:
            return "Microsoft Word window didn't exist"

        time.sleep(2)
        logger.info("Maximizing Microsoft Word window")
        if not self.dll.AU3_WinSetState(self.window_info, "", 3):
            return "could not maximize Microsoft Word window"
        
        time.sleep(2)
        logger.info("Sending enter to Microsoft Word window")
        if not self.dll.AU3_Send("{ENTER}", 0):
            return "could not send Enter key to create new docx"
        
        return None
        
    def open_docx(self, path):
        if not path:
            return "path must be provided"
        
        if not os.path.exists(path):
            return f"file path '{path}' does not exist"
        
        if not os.path.isfile(path):
            return f"path '{path}' is not a file"
        
        logger.info("Getting Microsoft Word executable path")
        executable_path = self._get_executable_path()
        if not executable_path:
            return "could not get Microsoft Word executable path"
        
        logger.info("Opening docx file")
        if not self.dll.AU3_Run(f'{executable_path} "{path}"', "", 1):
            return "could not open docx file"

        time.sleep(2)
        logger.info("Checking existing Microsoft Word window")
        if self.dll.AU3_WinExists(self.window_info, ""):
            logger.info("Getting Microsoft Word window handle")
            handle = self.dll.AU3_WinGetHandle(self.window_info, "")
            if not handle:
                return "could not get window handle"
            else:
                self.window_info = "[HANDLE:%s]" % f"{handle:08X}" 
            logger.info("Activating Microsoft Word window")
            self.dll.AU3_WinActivate(self.window_info, "")
            logger.info("Waiting Microsoft Word window to be active")
            if not self.dll.AU3_WinWaitActive(self.window_info, "", 10):
                return "could not activate Microsoft Word"
        else:
            return "Microsoft Word window didn't exist"
        
        time.sleep(2)
        logger.info("Maximizing Microsoft Word window")
        if not self.dll.AU3_WinSetState(self.window_info, "", 3):
            return "could not maximize Microsoft Word window"

        return None
    
    def write_docx(self, text = ""):
        err = self.check_existing_window()
        if err:
            return err
            
        if text == "":
            text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. In ultricies cursus sagittis."
            
        logger.info("Moving cursor to the bottom of docx file")
        if not self.dll.AU3_Send("^{END}", 0):
            return "could not send keys to move cursor"

        time.sleep(2)
        for letter in text:
            logger.info("Checking if Microsoft Word window is active")
            if not self.dll.AU3_WinActive(self.window_info, ""):
                return "Microsoft Word window is inactive"

            logger.info("Sending letter to Microsoft Word window")
            if not self.dll.AU3_Send(letter, 1):
                return f"could not send {letter} to Microsoft Word"
            rand = random.uniform(0.05, 0.15)
            time.sleep(rand)
            
        return None
    
    def scroll(self, direction = "down", clicks = 10, scroll_delay = 0.05):
        if direction != "up" and direction != "down":
            return "invalid scroll direction"
        
        err = self.check_existing_window()
        if err:
            return err

        time.sleep(2)
        for _ in range(clicks):
            logger.info("Checking if Microsoft Word window is active")
            if not self.dll.AU3_WinActive(self.window_info, ""):
                return "Microsoft Word window is inactive"
            
            logger.info("Scrolling Mouse wheel")
            time.sleep(scroll_delay)
            if not self.dll.AU3_MouseWheel(direction, 1):
                return "could not scroll mouse wheel"
        
        return None
    
    def save_docx(self):
        err = self.check_existing_window()
        if err:
            return err
        
        logger.info("Saving docx file")
        if not self.dll.AU3_Send("^s", 0):
            return "could not send ctrl+s to save docx file"
        
        return None