#!/usr/bin/env python

# adapted from http://matplotlib.org/examples/animation/simple_anim.html

import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import ping

# Don't show toolbar
plt.rcParams['toolbar'] = 'None'

# Show 1" x 1" figure
fig = plt.figure(figsize=(1,1))

index = np.arange(len(ping.hosts))
bar_width = .75
y_max = 200

rects = plt.bar(index, [1000] * len(ping.hosts), bar_width)

plt.xticks([])
plt.yticks([])
plt.ylim([0, y_max])
plt.xlim([0, len(ping.hosts) - 1 + bar_width])

def animate(i):
    ping.do_ping()
    for r,t in zip(rects, map (lambda x: np.mean(x[1]), ping.get_history())):
        r.set_height(t)
        plt.setp(r, color=cm.rainbow((1.0 * t) / y_max))
    return r

ani = animation.FuncAnimation(fig, animate)

plt.show()
