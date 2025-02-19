import customtkinter as ctk
import tkinter
from subprocess import Popen, STDOUT, PIPE, run
import psutil
import sys, os
from pathlib import Path
from time import sleep
class StatusBar(tkinter.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs, relief="sunken", bd=1, anchor="e")
        self.configure(text="hello there", font=("Helvetica", 15))
        self.pack(fill="x", pady=5, side="bottom")
        
    def setText(self, text : str):
        self.configure(text=text)
        
    def setAlert(self, text : str):
        self.setText(text)
        self.configure(foreground="red")
        
    def setSuccess(self, text : str):
        self.setText(text)
        self.configure(foreground="green")
                       
class ControlWindow(ctk.CTk):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Control Window")
        # self.geometry("300x200")
        # self.resizable(False, False)
        
        self.file_to_convert : Path = None
        self.btn_install = ctk.CTkButton(self, text="Install Service", command=self.install_service)
        self.btn_install.pack(pady=5)
        
        self.btn_remove = ctk.CTkButton(self, text="Uninstall Service", command=self.remove_service)
        self.btn_remove.pack(pady=5)
        
        self.btn_start = ctk.CTkButton(self, text="Start Service", command=self.start_service)
        self.btn_start.pack(pady=5)

        self.btn_stop = ctk.CTkButton(self, text="Stop Service", command=self.stop_service)
        self.btn_stop.pack(pady=5)
        
        self.btn_choose_file = ctk.CTkButton(self,text = "choose file", command = self.choose_file)
        self.btn_choose_file.pack(pady=5)
        
        # self.file_label = tkinter.Label(self, text=self.file_to_convert, relief="sunken", bd=1, anchor="e")
        self.status_bar = StatusBar(self)
        
        self.check_service()
    def install_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "install"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "install"]

        # print(cmd)
        
        run(cmd)
        
        self.check_service()

    def remove_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "remove"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "remove"]

        # print(cmd)
        
        run(cmd)
        self.check_service()

    def start_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "start"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "start"]

        run(cmd)
        self.check_service()

    def stop_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "stop"]
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            cmd = ["python", f"{BASE_DIR}/service.py", "stop"]
        
        run(cmd)
        self.check_service()

    def choose_file(self):
        file_path = ctk.filedialog.askopenfilename()
        self.file_to_convert = Path(file_path)
        self.status_bar.setText(self.file_to_convert)

    def check_service(self):
        try :
            service = psutil.win_service_get("MyService")
            if service != None:
                # print(service)
                # print(dir(service))
                # print(service.status())
                # print(service.binpath())
                self.status_bar.setSuccess("Service is installed")
            else : 
                self.status_bar.setAlter("Service is NOT installed")
                print("Couldn't find service with that name")
            pass
        except:
            self.status_bar.setAlert("Service Not Found")
            # sleep(0.5)
            # self.install_service()
        
if __name__ == "__main__":
    window = ControlWindow()
    window.mainloop()
