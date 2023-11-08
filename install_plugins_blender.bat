@echo off

:: Remove the ufit folder and its contents
rmdir /s /q "C:\Users\bertj\Documents\Blender\blender-3.5.0-windows-x64\3.5\scripts\addons\ufit"

:: Recreate the ufit folder
mkdir "C:\Users\bertj\Documents\Blender\blender-3.5.0-windows-x64\3.5\scripts\addons\ufit"

:: Copy the contents of the local ufit folder to the destination
xcopy /E /Y "ufit" "C:\Users\bertj\Documents\Blender\blender-3.5.0-windows-x64\3.5\scripts\addons\ufit"

:: Rename the __init_plugins__.py file to __init__.py
ren "C:\Users\bertj\Documents\Blender\blender-3.5.0-windows-x64\3.5\scripts\addons\ufit\__init_plugins__.py" "__init__.py"

:: Terminate Blender
taskkill /F /IM blender.exe

:: Start Blender
start "" "C:\Users\bertj\Documents\Blender\blender-3.5.0-windows-x64\blender"