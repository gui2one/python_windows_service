import customtkinter as ctk
import tkinter
from subprocess import run, CREATE_NO_WINDOW
import psutil
import sys, os
from pathlib import Path
from global_vars import SERVICE_NAME
from config import Config, CONFIG_FILE_NAME, get_config_path


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    EXE = "service.exe"
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE = "service.py"

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
class FileWidget(ctk.CTkFrame):
    
    def __init__(self, master=None, callback=lambda: None, **kwargs):
        super().__init__(master, **kwargs)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        
        self.file_path : Path = None
        self.callback = callback

        
        
        self.btn_choose_file = ctk.CTkButton(self,text = "choose file", command = self.choose_file)
        self.btn_choose_file.grid(column=0, row=0, pady=5)
        
        self.title_label = ctk.CTkLabel(self, text = "No Title")
        self.title_label.grid(column=1, row=0, padx=10, sticky="e")
        
        self.file_label = ctk.CTkLabel(self, text=self.file_path, anchor="e")
        self.file_label.configure(text="Choose File")
        self.file_label.grid(column=0, row=1, padx=10, columnspan=2, sticky="w")
        
        
    def choose_file(self):
        file_path = ctk.filedialog.askopenfilename()
        self.file_path = Path(file_path)
        self.file_label.configure(text=self.file_path)
        if self.callback != None:
            self.callback()
        
    def setTitle(self, title : str):
        self.title_label.configure(text=title)
    
    def setFilePath(self, path : Path):
        self.file_path = path
        self.file_label.configure(text=self.file_path)
        
class ControlWindow(ctk.CTk):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.title("Control Window")
        self.geometry("400x500")
        
        self.config = Config("","")

        self.btn_install = ctk.CTkButton(self, text="Install Service", command=self.install_service)
        self.btn_install.pack(pady=5)
        
        self.btn_remove = ctk.CTkButton(self, text="Uninstall Service", command=self.remove_service)
        self.btn_remove.pack(pady=5)
        
        self.btn_start = ctk.CTkButton(self, text="Start Service", command=self.start_service)
        self.btn_start.pack(pady=5)

        self.btn_stop = ctk.CTkButton(self, text="Stop Service", command=self.stop_service)
        self.btn_stop.pack(pady=5)

        self.status_bar = StatusBar(self)
        
        self.file_widget = FileWidget(self, callback=lambda: self.set_file_to_convert(self.file_widget.file_path))
        self.file_widget.setTitle("File to Convert")
        self.file_widget.pack(pady=5, fill="x")

        self.converted_file = FileWidget(self, callback=lambda: self.set_target_file(self.converted_file.file_path))
        self.converted_file.setTitle("Converted File")
        self.converted_file.pack(pady=5, fill="x")
        
        self.service_is_installed = False 
        self.service_is_running = False 
        
        self.load_config()
        self.check_service()
        
    def install_service(self):


        full_path = f"{BASE_DIR}\\{EXE}".replace("\\", "/")
        cmd = [ f"{full_path}", "install"]

        run(cmd, creationflags=CREATE_NO_WINDOW)
        self.check_service()

    def remove_service(self):
        # try and stop it before hand
        try:
            self.stop_service()
            print("Did I Stopped service ?")
        except:
            pass

        full_path = f"{BASE_DIR}\\{EXE}".replace("\\", "/")
        cmd = [ f"{full_path}", "remove"]


        run(cmd, creationflags=CREATE_NO_WINDOW)
        self.check_service()

    def start_service(self):

        full_path = f"{BASE_DIR}\\{EXE}".replace("\\", "/")
        cmd = [ f"{full_path}", "start"]


        run(cmd, creationflags=CREATE_NO_WINDOW)
        self.check_service()

    def stop_service(self):

        full_path = f"{BASE_DIR}\\{EXE}".replace("\\", "/")
        cmd = [ f"{full_path}", "stop"]
        
        run(cmd, creationflags=CREATE_NO_WINDOW)
        self.check_service()

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

    def set_file_to_convert(self, path : Path):
        self.config.file_to_convert = str(path)
        self.save_config()
        
    def set_target_file(self, path : Path):
        self.config.target_file = str(path)        
        self.save_config()
        
    def save_config(self):
        with open(get_config_path(), "w") as f:
            f.write(self.config.to_json(indent=1))
            
    def load_config(self):
        try :
            with open(get_config_path(), "r") as f:
                self.config = Config.from_json(f.read())
                self.file_widget.setFilePath(Path(self.config.file_to_convert))
                self.converted_file.setFilePath(Path(self.config.target_file))
                print("loaded config ....") 
                return
        except:
            print("no config to load ... \ncreating one")
            self.save_config() # create a new empty config file
        
            
if __name__ == "__main__":
    window = ControlWindow()
    window.mainloop()
