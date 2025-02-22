import time
import sys
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
from global_vars import SERVICE_NAME, SERVICE_DISPLAY_NAME, SERVICE_DESCRIPTION
import argparse
from pathlib import Path

class MyService:
    """Silly little application stub"""

    def stop(self):
        """Stop the service"""
        self.running = False

    def run(self):
        """Main service loop. This is where work is done!"""
        
        parser = argparse.ArgumentParser()
        parser.add_argument("start", nargs="?", default=False)
        parser.add_argument("stop", nargs="?", default=False)
        parser.add_argument("debug", nargs="?", default=False)
        parser.add_argument("--file", type=str)
        parser.add_argument("--target-file", type=str)
        args = parser.parse_args()
        self.running = True
        while self.running:
            
            servicemanager.LogInfoMsg("Service running...")
            # servicemanager.LogInfoMsg(f"{args.file} {args.target_file}")
            data : str = ""
            if args.file and args.target_file:
                servicemanager.LogInfoMsg(args.file)
                servicemanager.LogInfoMsg(args.target_file)
                with open(Path(args.file), "r") as f:
                    data = f.read()
                with open(Path(args.target_file), "w") as f:
                    f.write(data)
                    # f.write("I am a service")
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
