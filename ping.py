import subprocess
import re
import string
import sys

# hosts to check
hosts = ['google.com', 'nytimes.com', 'facebook.com']

# length of history to keep
history_len = 10

history = {}
for h in hosts:
    history[h] = []

# example summary line that we want to extract from ping output
# rtt min/avg/max/mdev = 41.924/86.305/106.894/22.820 ms
ping_time_re = '([0-9.]+)'
ping_summary_re = 'rtt min/avg/max/mdev = ' + '/'.join([ping_time_re] * 4)

def add_to_history(host, val):
    hist = history[host]
    if len(hist) >= history_len:
        hist.pop()
    hist.insert(0, val)

def do_ping ():
    for h in hosts:
        try:
            ping_resp = subprocess.check_output(['timeout', '2s', 'ping', '-c', '1', '-W', '1', h], text=True)
            non_empty_lines = list(filter(lambda x: len(x) > 0, ping_resp.split('\n')))
            if len(non_empty_lines) == 0:
                print('Error, no non-empty lines in ping output')
                sys.exit(1)
            else:
                non_empty_lines.reverse()
                summary = non_empty_lines[0]
                m = re.match(ping_summary_re, summary)
                if m:
                    (_ping_min, ping_mean, _ping_max, _ping_mdev) = m.groups()
                    add_to_history(h, int(round(float(ping_mean))))
                else:
                    print('Error, could not parse summary from ping')
                    sys.exit(1)
        except subprocess.CalledProcessError:
            # if we don't hear back, add a history item for 1s (1000 ms)
            add_to_history(h, 1000)
            print("ping failed")

# returns a list containing pairs of hostname and most recent ping times
def get_history ():
    l = []
    for h in history:
        l.append((h, history[h]))
    return l
