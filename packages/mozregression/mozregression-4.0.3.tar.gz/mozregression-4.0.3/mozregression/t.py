import subprocess

import six

output = subprocess.Popen(
    ["adb", "version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
).communicate()
re_version = re.compile(r"Android Debug Bridge version (.*)")
_adb_version = re_version.match(str(output[0])).group(1)

print(bytes(output[0]))
