@echo off
:repeat
echo %random%

:: Create a temporary file with the message
echo see you > temp.txt

:: Open Notepad with the temporary file
start notepad temp.txt

:: Wait for a brief moment to avoid overwhelming the system
ping 127.0.0.1 -n 2 > nul

:: Loop back to the 'repeat' label
goto repeat
