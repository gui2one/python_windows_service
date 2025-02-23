import time
import sys
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
from global_vars import SERVICE_NAME, SERVICE_DISPLAY_NAME, SERVICE_DESCRIPTION
from config import Config, get_config_path
import logging
import os
import subprocess


logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
class MyService:
    """Silly little application stub"""

    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        config_path = get_config_path()
        config = None
        with open(config_path, "r") as f:
            config = Config.from_json(f.read())
            
        if config is None:
            return
        self.running = True
        while self.running:
            
            
            script = f"{BASE_DIR}\\python_scripts\\{config.python_script}".replace("\\", "/")
            src_file = f"{config.file_to_convert}".replace("\\", "/")
            target_file = f"{config.target_file}".replace("\\", "/")
            cmd = ["python",script, src_file, target_file]
            servicemanager.LogInfoMsg(f"python {script} {src_file} {target_file}")
            try :
                subprocess.run(cmd)
            except Exception as e:
                servicemanager.LogInfoMsg(str(e))
            # # servicemanager.LogInfoMsg(f"{args.file} {args.target_file}")

            time.sleep(3)  # Important work


class MyServiceFramework(win32serviceutil.ServiceFramework):

    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_description_ = SERVICE_DESCRIPTION

    def SvcStop(self):
        """Stop the service"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        """Start the service; does not return until stopped"""
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = MyService()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyServiceFramework)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyServiceFramework)


if __name__ == "__main__":
    init()
