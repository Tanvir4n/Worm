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
