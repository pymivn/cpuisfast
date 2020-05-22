#!/usr/bin/env python
# Copy from https://github.com/pymivn/cpuisfast/blob/master/cpuisfast/client.py
# Change should do in that repo instead and copy here afterward

import json
import platform as plf
import re
import subprocess
import timeit

try:
    # Py3
    import urllib.request as urll
except ImportError:
    # Py2
    import urllib2 as urll


GITHUB_ISSUE = "https://github.com/pymivn/cpuisfast/issues/new"


def get_processor_name():
    # type: () -> str
    if plf.system() == "Windows":
        try:
            import winreg

            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"Hardware\Description\System\CentralProcessor\0",
            )  # NOQA
            processor_brand = winreg.QueryValueEx(key, "ProcessorNameString")[
                0
            ]
            winreg.CloseKey(key)
            return processor_brand
        except Exception:
            return plf.processor()
    elif plf.system() == "Darwin":
        command = ["sysctl", "-n", "machdep.cpu.brand_string"]
        return subprocess.check_output(command).strip().decode()
    elif plf.system() == "Linux":
        with open("/proc/cpuinfo") as f:
            for line in f:
                if "model name" in line:
                    return re.sub(".*model name.*:", "", line, 1)
    elif "bsd" in plf.system().lower():
        try:
            with open("/var/run/dmesg.boot") as f:
                for line in f:
                    if line.startswith("CPU:"):
                        return line.replace("CPU:", "").strip()
        except Exception as e:
            print("Cannot get *BSD CPU %s", e)

    return "" or plf.machine()


ONE_MILLION = 10 ** 6
t_empty = timeit.Timer(
    "for i in range({}):\n    pass\n".format(ONE_MILLION)
)  # NOQA
t = timeit.Timer(
    "s = 0\nfor i in range({}):\n    s = s + i\nprint(s)".format(ONE_MILLION)
)  # NOQA

# read timeit doc for why use min
took_empty = t_empty.repeat(10, 1)
empty_best = min(took_empty)

took = t.repeat(10, 1)
best = min(took)
cpu_name = get_processor_name()
empty_iterate_freq = ONE_MILLION // empty_best
plus_iterate_freq = ONE_MILLION // best
print("Your CPU is %s" % cpu_name)
arch = plf.machine()
implementation = plf.python_implementation()
py_ver = plf.python_version()
system = plf.system()
print("This is running on", system, arch, implementation, py_ver)


print("It can loop %d times per second" % empty_iterate_freq)
print("Calculating sum from 0 to %d" % ONE_MILLION)
print("Best took %s s" % best)
print("Your CPU can do: %d (+) operations/second" % plus_iterate_freq)
data = {
    "cpu": cpu_name,
    "empty_iterate_freq": empty_iterate_freq,
    "plus_iterate_freq": plus_iterate_freq,
    "implementation": implementation,
    "arch": arch,
    "system": system,
    "python_version": py_ver,
}

URL = "https://cpu.pymi.vn/cpudata"

params = json.dumps(data).encode("utf8")
# CloudFlare blocks Python-urllib user-agent, fake it
headers = {
    "content-type": "application/json",
    "User-Agent": "python-requests/2.18.1",
}
req = urll.Request(URL, data=params, headers=headers)
try:
    response = urll.urlopen(req)
except Exception as e:
    print("Please copy output and report at: %s" % GITHUB_ISSUE)
    raise e
else:
    print(response.read())
    print("DONE, visit https://cpu.pymi.vn/ to see result")
