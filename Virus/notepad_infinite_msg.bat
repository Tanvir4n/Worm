@echo off
:repeat
echo %random%

:: Create a temporary file with the message
echo There is no escape! > no escape.txt

:: Open Notepad with the temporary file
start notepad no escape.txt

:: Wait for a brief moment to avoid overwhelming the system
ping 127.0.0.1 -n 2 > nul

:: Loop back to the 'repeat' label
goto repeat

REM Caution: Running this script will continue to open new instances of Notepad indefinitely until you manually stop it. 
REM To stop the script, you can:

REM • Close the Command Prompt window.
REM • Use Task Manager to end the batch file process.
REM • Press Ctrl + C in the Command Prompt window to terminate the batch script.




