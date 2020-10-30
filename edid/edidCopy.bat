@echo off

REM Declare variables
set edid_source=C:\source\DumpEDID
set edid_dest=\\%1\C$\source\DumpEDID

REM Copy DumpEDID.exe to source folder
Robocopy %edid_source% %edid_dest% /zb /dst /r:1 /w:0 /nfl /ndl

REM Exit script
exit