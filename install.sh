#!/bin/bash
set -eu

adb push totmann.apk /sdcard/

adb root

adb shell mount -o rw,remount /system

adb shell rm -rf /system/priv-app/Totmann

adb shell mkdir /system/priv-app/Totmann
adb shell chmod 0755 /system/priv-app/Totmann

adb shell cp /sdcard/totmann.apk  /system/priv-app/Totmann/base.apk

adb shell chmod 0644 /system/priv-app/Totmann/base.apk
adb shell chown -R root:root /system/priv-app/Totmann

adb shell chcon "u:object_r:system_file:s0" /system/priv-app/Totmann
adb shell chcon "u:object_r:system_file:s0" /system/priv-app/Totmann/base.apk

adb shell reboot
