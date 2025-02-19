import customtkinter as ctk
from subprocess import Popen, STDOUT, PIPE
import sys, os
class ControlWindow(ctk.CTk):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Control Window")
        self.geometry("300x200")
        # self.resizable(False, False)
        
        self.btn_install = ctk.CTkButton(self, text="Install Service", command=self.install_service)
        self.btn_install.pack(pady=20)
        
        self.btn_remove = ctk.CTkButton(self, text="Uninstall Service", command=self.remove_service)
        self.btn_remove.pack(pady=20)
        
        self.btn_start = ctk.CTkButton(self, text="Start Service", command=self.start_service)
        self.btn_start.pack(pady=20)

        self.btn_stop = ctk.CTkButton(self, text="Stop Service", command=self.stop_service)
        self.btn_stop.pack(pady=20)
        
    def install_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "install"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "install"]

        print(cmd)
        
        Popen(cmd)

    def remove_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "remove"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "remove"]

        print(cmd)
        
        Popen(cmd)

    def start_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "start"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "start"]

        print(cmd)
        
        Popen(cmd)

    def stop_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "stop"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "stop"]

        print(cmd)
        
        Popen(cmd)

if __name__ == "__main__":
    window = ControlWindow()
    window.mainloop()
