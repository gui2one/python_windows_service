@echo off
powershell -NoExit -Command "dist/service.exe start -Verb RunAs" 
PAUSE