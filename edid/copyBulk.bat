@echo off

for /F "tokens=*" %%A in (computers.txt) do start cmd /k "C:\Users\kaimikad\Documents\Github\Inventory_Tools\edid\edidCopy.bat" %%A