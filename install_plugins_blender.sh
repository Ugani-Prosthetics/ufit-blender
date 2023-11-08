rm -rf C:/Users/bertj/Documents/Blender/blender-3.5.0-windows-x64/3.5/scripts/addons/ufit
mkdir C:/Users/bertj/Documents/Blender/blender-3.5.0-windows-x64/3.5/scripts/addons/ufit/
cp -R ufit/. C:/Users/bertj/Documents/Blender/blender-3.5.0-windows-x64/3.5/scripts/addons/ufit/
mv C:/Users/bertj/Documents/Blender/blender-3.5.0-windows-x64/3.5/scripts/addons/ufit/__init_plugins__.py C:/Users/bertj/Documents/Blender/blender-3.5.0-windows-x64/3.5/scripts/addons/ufit/__init__.py

taskkill /F /IM blender.exe
start "" "C:/Users/bertj/Documents/Blender/blender-3.5.0-windows-x64/blender"