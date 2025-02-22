import customtkinter as ctk
import tkinter
from subprocess import Popen, STDOUT, PIPE, run
import psutil
import sys, os
from pathlib import Path
from time import sleep
from global_vars import SERVICE_NAME

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
        self.geometry("300x500")
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
        
        
        self.service_is_installed = False 
        self.service_is_running = False 
        
        self.check_service()
    def install_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "install"]
        else:
            pass

        # print(cmd)
        
        run(cmd)
        
        self.check_service()

    def remove_service(self):
        # try and stop it before hand
        try:
            self.stop_service()
            print("Did I Stopped service ?")
        except:
            pass
        
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "remove"]
        else:
            pass

        run(cmd)
        self.check_service()

    def start_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "start"]
        else:
            pass

        run(cmd)
        self.check_service()

    def stop_service(self):
        if getattr(sys, 'frozen', False):
            BASE_DIR = os.path.dirname(sys.executable)
            full_path = f"{BASE_DIR}\\service.exe".replace("\\", "/")
            cmd = [ f"{full_path}", "stop"]
        else:
            pass
        
        run(cmd)
        self.check_service()

    def choose_file(self):
        file_path = ctk.filedialog.askopenfilename()
        self.file_to_convert = Path(file_path)
        self.status_bar.setText(self.file_to_convert)

    def check_service(self):
        try :
            service = psutil.win_service_get(SERVICE_NAME)
            if service != None:
                # print(service)
                # print(dir(service))
                # print(service.status())
                # print(service.binpath())
                self.status_bar.setSuccess("Service is installed")
                self.service_is_installed = True
                if service.status() == "running":
                    self.status_bar.setSuccess("Service is Running")
                    self.service_is_running = True
                else:
                    self.status_bar.setSuccess("Service is Stopped")
                    self.service_is_running = False
            else : 
                self.service_is_installed = False
                self.service_is_running = False
                self.status_bar.setAlert("Service is NOT installed")
                print("Couldn't find service with that name")
            pass
        except:
            self.status_bar.setAlert("Service Not Found")
            self.service_is_installed = False
            self.service_is_running = False
            # sleep(0.5)
            # self.install_service()
        
        self.update_buttons()

    def update_buttons(self):
        if self.service_is_installed:
            self.btn_install.configure(state="disabled")
            self.btn_remove.configure(state="normal")
            self.btn_start.configure(state="normal")
            self.btn_stop.configure(state="normal")
        else:
            self.btn_install.configure(state="normal")
            self.btn_remove.configure(state="disabled")
            self.btn_start.configure(state="disabled")
            self.btn_stop.configure(state="disabled")
if __name__ == "__main__":
    window = ControlWindow()
    window.mainloop()
