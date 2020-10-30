@echo off

for /F "tokens=*" %%A in (computers.txt) do start cmd /k psexec -h -u cc\kaimikad -p Akuamakana211$ \\%%A "C:\source\DumpEDID\edidDump.bat"

exit