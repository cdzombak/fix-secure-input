#!/usr/bin/env python3

import os
import re

pid_re = re.compile('"kCGSSessionSecureInputPID"=(\d+)')

ioreg_out = os.popen('ioreg -l -w 0 | grep SecureInput').read()

pids = set()
for ioreg_line in ioreg_out.splitlines():
    match = pid_re.search(ioreg_line)
    pid = match.group(1)
    pids.add(pid)

for pid in pids:
    ps_out = os.popen(f"ps -p {pid} | sed -n '2 p'").read()
    ps_name = ps_out.split()[3]
    print('PID ' + pid + ' (' + ps_name + ') is using Secure Input')
    if 'loginwindow' in ps_name:
        os.popen("""osascript -e 'Tell application "System Events" to display dialog "loginwindow is using Secure Input. Lock & unlock the screen to fix it." with title "Secure Input" buttons {"OK"} default button 1 with icon caution'""").read()
    else:
        os.popen(f"""osascript -e 'Tell application "System Events" to display dialog "{ps_name} (PID {pid}) is using Secure Input. Kill it?" with title "Secure Input" buttons {{"No", "Kill"}} default button 2 with icon caution' -e 'if result = {{button returned:"Kill"}} then' -e 'do shell script "kill {pid}"' -e 'end if'""").read()
