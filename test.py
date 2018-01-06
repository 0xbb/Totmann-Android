#!/usr/bin/env python3
from subprocess import check_call, check_output
from time import sleep
import re
ADB = './adb.exe'


def wait_for_emulator():
    print("Waiting for emulator")
    check_call([ADB, 'wait-for-device', 'shell', 'while [[ -z $(getprop sys.boot_completed) ]]; do sleep 1; done; input keyevent 82'])
    root()
    sleep(15)

def root():
    print('Enabling root')
    check_call([ADB, 'root'])
    assert 'root' == check_output([ADB, 'shell', 'whoami']).decode().strip(), 'adb root'

def boot_id():
    return check_output([ADB, 'shell', 'cat', '/proc/sys/kernel/random/boot_id']).decode().strip()

def check_alarm(mins, msg):
    print('Checking alarm')
    alarms = check_output([ADB, 'shell', 'dumpsys', 'alarm']).decode()
    print(alarms)
    a = re.search(r'Alarm{([0-9a-f]+) type 2 when [0-9]+ net\.bierbaumer\.totmann}\r\n.+net\.bierbaumer\.totmann/\.AlarmReceiver\r\n.+when=\+([0-9]+)d([0-9]+)h([0-9]+)m', alarms)
    assert a, 'Alarm not found'
    print(a.group(0))
    assert 4 == int(a.group(2)) and 23 == int(a.group(3)) and mins <= int(a.group(4)), msg

    return a.group(1) #alarm id

print("Starting Totmann tests")
wait_for_emulator()

boot_id0 = boot_id()

print('Installing System App')
check_call([ADB, 'shell', 'mount', '-o', 'rw,remount', '/system'])
check_call([ADB, 'shell', 'rm', '-rf', '/system/priv-app/Totmann'])
check_call([ADB, 'shell', 'mkdir', '/system/priv-app/Totmann'])
check_call([ADB, 'shell', 'chmod', '0755', '/system/priv-app/Totmann'])
#check_call([ADB, 'push', './app/build/outputs/apk/debug/app-debug.apk', '/system/priv-app/Totmann/base.apk'])
check_call([ADB, 'push', 'base.apk', '/system/priv-app/Totmann/base.apk'])
check_call([ADB, 'shell', 'chmod', '0644', '/system/priv-app/Totmann/base.apk'])
check_call([ADB, 'shell', 'chown', '-R', 'root:root', '/system/priv-app/Totmann'])
check_call([ADB, 'shell', 'chcon', 'u:object_r:system_file:s0', '/system/priv-app/Totmann'])
check_call([ADB, 'shell', 'chcon', 'u:object_r:system_file:s0', '/system/priv-app/Totmann/base.apk'])

print('Reboot')
check_call([ADB, 'reboot'])
wait_for_emulator()
boot_id1 = boot_id()
assert boot_id0 != boot_id1

print("Totmann should be installed as System App now")

print("Testing if Reboot Button works")
check_call([ADB, 'shell',  'am', 'start', '-n', 'net.bierbaumer.totmann/net.bierbaumer.totmann.MainActivity'])
try:
    for _ in range(5):
        check_call([ADB, 'shell', 'input', 'keyevent', '66'])
except:
    pass

wait_for_emulator()
boot_id2 = boot_id()
assert boot_id0 != boot_id1 != boot_id2

print("Testing if BOOT_COMPLETED works")
alarm_id0 = check_alarm(30, 'Alarm should be set after boot')

check_call([ADB, 'shell', 'am', 'broadcast', '-a', 'android.intent.action.BOOT_COMPLETED'])
alarm_id1 = check_alarm(59, 'Alarm reset after BOOT_COMPLETED')
assert alarm_id0 != alarm_id1

print("Testing if USER_PRESENT works")
check_call([ADB, 'shell', 'am', 'broadcast', '-a', 'android.intent.action.USER_PRESENT'])
alarm_id2 = check_alarm(59, 'Alarm reset after USER_PRESENT')
assert alarm_id0 != alarm_id1 != alarm_id2

print("Testing if Alarm will reboot")
check_call([ADB, 'shell', 'am', 'broadcast', '-n', 'net.bierbaumer.totmann/net.bierbaumer.totmann.AlarmReceiver'])
wait_for_emulator()
boot_id3 = boot_id()
assert boot_id0 != boot_id1 != boot_id2 != boot_id3

print("Test done :)")
