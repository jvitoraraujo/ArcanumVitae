[app]
title = Arcanum Vitae
package.name = arcanumvitae
package.domain = org.arcanumvitae
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas
source.include_patterns = assets/*,assets/*/*
source.exclude_dirs = bin,.buildozer,__pycache__
version = 2.2
requirements = python3,kivy==2.3.0,certifi
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/assets/logo.png
presplash.filename = %(source.dir)s/assets/logo.png
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
