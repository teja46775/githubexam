import os
import sys

def get_uptime():
    if sys.platform.startswith('linux'):
        # Read uptime from /proc/uptime
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        return uptime_seconds
    elif sys.platform == 'darwin':
        # Use sysctl for macOS
        import subprocess
        output = subprocess.check_output(['sysctl', '-n', 'kern.boottime']).decode()
        import re, time
        match = re.search(r'{ sec = (\d+),', output)
        if match:
            boot_time = int(match.group(1))
            uptime_seconds = time.time() - boot_time
            return uptime_seconds
        else:
            raise RuntimeError("Could not parse kern.boottime")
    elif sys.platform.startswith('win'):
        # Use uptime from 'net stats srv'
        import subprocess
        output = subprocess.check_output("net stats srv", shell=True).decode(errors='ignore')
        for line in output.split('\n'):
            if "Statistics since" in line:
                import datetime
                uptime_str = line.strip().split("since")[1].strip()
                boot_time = datetime.datetime.strptime(uptime_str, '%m/%d/%Y %I:%M:%S %p')
                uptime_seconds = (datetime.datetime.now() - boot_time).total_seconds()
                return uptime_seconds
        raise RuntimeError("Could not parse uptime from net stats srv")
    else:
        raise NotImplementedError("Unsupported platform")

def format_uptime(seconds):
    days = int(seconds // (24 * 3600))
    seconds %= (24 * 3600)
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{days}d {hours}h {minutes}m {seconds}s"

if __name__ == "__main__":
    try:
        uptime = get_uptime()
        print(f"System uptime: {format_uptime(uptime)}")
    except Exception as e:
        print(f"Error getting uptime: {e}")
