[app]

# (str) Title of your application
title = ZustellApp

# (str) Package name
package.name = zustellapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.braunau

# (str) Source code where the main.py live
source.dir = ZustellApp

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,db

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,requests,sqlite3,kivy_garden.mapview

# (str) Custom source folders for requirements
# (list) garden recipes to include in the application
garden_requirements = mapview

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientations (landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = CAMERA, INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Android API to use
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
#android.ndk = 25b

# (bool) use posix to build (default True)
#android.use_posix = True

# (list) Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup
android.allow_backup = True

# (list) The Android entry point to use (default is main.py)
#android.entrypoint = main.py

# (list) Screen (screen) titles to include
#android.window_titles = ZustellApp

[buildozer]

# (int) log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1

# (str) Path to build artifact storage, accessible in a container
# build_dir = ./.buildozer

# (str) Path to bin directory, accessible in a container
# bin_dir = ./bin
