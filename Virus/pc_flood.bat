@echo off
REM This batch script repeatedly opens Notepad, File Explorer, and a new Command Prompt window.

:repeat
:: Output a random number
echo %random%

:: Open a new instance of Notepad
start notepad

:: Open a new instance of File Explorer
start explorer

:: Open a new instance of Command Prompt
start cmd

:: Loop back to the 'repeat' label
goto repeat

REM ====================
::• Use Task Manager:

:: Press Ctrl + Shift + Esc to open Task Manager.
:: Find the "Windows Command Processor" (cmd.exe) or any other applications that were started by the batch file (like Notepad and File Explorer).
:: Select the process and click "End Task".
REM ====================
