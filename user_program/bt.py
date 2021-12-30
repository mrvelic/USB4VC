import time
import os
import subprocess

LINUX_EXIT_CODE_TIMEOUT = 124

def bt_setup():
	rfkill_str = subprocess.getoutput("/usr/sbin/rfkill -n")
	if 'bluetooth' not in rfkill_str:
		return 1, "no bluetooth receiver"
	os.system('/usr/sbin/rfkill unblock bluetooth')
	time.sleep(0.1)
	exit_code = os.system('timeout 1 bluetoothctl agent on')
	if exit_code == LINUX_EXIT_CODE_TIMEOUT:
		return 2, 'bluetoothctl stuck'
	return 0, ''

def scan_bt_devices(timeout_sec = 5):
    exit_code = os.system(f"timeout {timeout_sec} bluetoothctl scan on") >> 8
    if exit_code != LINUX_EXIT_CODE_TIMEOUT:
        print('bluetoothctl scan error')
        return None
    device_str = subprocess.getoutput("bluetoothctl devices")
    print(device_str)
    bt_dev_list = []
    for line in device_str.replace('\r', '').split('\n'):
        if 'device' not in line.lower():
            continue
        line_split = line.split(' ', maxsplit=2)
        # skip if device has no name
        if len(line_split) < 3 or line_split[2].count('-') == 5:
            continue
        bt_dev_list.append((line_split[1], line_split[2]))
    return bt_dev_list

def pair_bt_device(mac_addr):
	result_str = subprocess.getoutput(f"timeout 10 bluetoothctl pair {mac_addr}")
	print(result_str)

print(bt_setup())

# dev_list = scan_bt_devices()
# print(dev_list)
# pair_bt_device(dev_list[0][0])