./copy_python_to_dist.ps1
pyinstaller.exe --log-level INFO service.spec
pyinstaller.exe --log-level INFO control_window.spec
