@echo off
mkdir C:\bin

REM Copy our files
copy install\mubuild.bat C:\bin\mubuild.bat
copy mubuild.py C:\bin\mubuild.py
IF EXIST C:\bin\donepath exit

REM add to path
setx path "C:\bin;%path%"
echo DonePath >> C:\bin\donepath