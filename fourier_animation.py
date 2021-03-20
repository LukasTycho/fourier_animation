""" Fourier-Synthesis animated.

Copyright (C) <2021> Lukas Tycho Mendelsohn

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details at
<http://www.gnu.org/licenses/>.
"""

import argparse
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np


###############################################################################

def create_axes():
    global fig, cc, im, re, ab, r
    
    # create four subplots
    fig = plt.figure('Fourier Visualization', figsize=(10, 10))
    cc = fig.add_subplot(221, aspect='equal')   # complex plane
    im = fig.add_subplot(222, sharey=cc)        # imaginary
    re = fig.add_subplot(223, sharex=cc)  # real
    ab = fig.add_subplot(224, projection='3d')  # 3D, complex over time
    
    # Normalize time to 2*pi. Animation plots into the past, i.e. the current 
    # value of the animation will always be at time = 0.
    t_ticks = [0, -np.pi/2, -np.pi, -3/2*np.pi, -2*np.pi]
    t_ticks_labels = ['0', r'$-\frac{\pi}{2}$', r'$-\pi$', 
                      r'$-\frac{3}{2} \pi$', r'$-2 \pi$']
    
    cc.set_title('complex plane')
    cc.set_xlabel('real part')
    cc.set_ylabel('imaginary part')
    cc.grid('on')
    cc.axhline(y=0, xmin=0, xmax=1, color='gray')
    cc.axvline(x=0, ymin=0, ymax=1, color='gray')
    
    im.set_title('red: pos. frequencies | blue: neg. frequencies')
    im.set_xlabel('normalized time')
    im.yaxis.set_label_position("right")
    im.yaxis.tick_right()
    im.set_ylabel('imaginary value')
    im.grid('on')
    im.axhline(y=0, xmin=0, xmax=1, color='gray')
    im.set_xticks(t_ticks)
    im.set_xticklabels(t_ticks_labels)
    
    re.set_xlabel('real value')
    re.set_ylabel('normalized time')
    re.grid('on')
    re.axvline(x=0, ymin=0, ymax=1, color='gray')
    re.set_yticks(t_ticks)
    re.set_yticklabels(t_ticks_labels)
    
    ab.set_xlabel('normalized time')
    ab.set_ylabel('imaginary part')
    ab.set_zlabel('real part')
    ab.grid('on')
    ab.plot3D([-2*np.pi, 0], [0, 0], [0, 0], '-', color='gray')
    ab.set_xticks(t_ticks)
    ab.set_xticklabels(t_ticks_labels)
    
    # setting axes limits based on sum of all coefficients and time
    max_r = sum(r)
    lim = 1.1 * max_r
    lims = [-lim, lim]
    cc.set_xlim(lims)
    cc.set_ylim(lims)
    ab.set_ylim(lims)
    ab.set_zlim(lims)
    
    t_lims = [-2*np.pi-0.05, 0.05]
    t_lims_inv = t_lims[::-1]
    im.invert_xaxis()
    im.set_xlim(t_lims_inv)
    re.set_ylim(t_lims)
    ab.set_xlim(t_lims)

###############################################################################

def init():
    """ Plots all lines.
    
    At first call at the start of the animation, the lines will be created, but
    not visible since neither x nor y nor phi have any values stored in them.
    
    When called at the end, all lines will be recreated with the values of x, y
    and phi at time of calling the function.

    Returns
    -------
    list
        Artist objects to be animated.

    """

    global animated_objects, circles, freqs, circles_neg, freqs_neg, \
        xy_line, xy_neg_line, re_line, re_neg_line, im_line, im_neg_line, \
        ab_line, ab_neg_line
    
    # creating lines in all plots for pos and neg frequencies
    xy_line, = cc.plot(x, y, '-', color='red')
    xy_neg_line, = cc.plot(x, -y, ':', color='blue')
    re_line, = re.plot(x, phi, '-', color='red')
    re_neg_line, = re.plot(x, phi, ':', color='blue')
    im_line, = im.plot(phi, y, '-', color='red')
    im_neg_line, = im.plot(phi, -y, ':', color='blue')
    ab_line, = ab.plot3D(phi, y, x, '-', color='red')
    ab_neg_line, = ab.plot3D(phi, -y, x, ':', color='blue')
    
    circles = [None] * len(c)
    freqs = [None] * len(c)
    circles_neg = [None] * len(c)
    freqs_neg = [None] * len(c)
    # creating circles and lines in complex plane (cc)
    # Only for frequencies with a radius greater than 0 a line and circle will
    # be created. The DC-Offset does not get a circle.
    for i in range(len(c)):
        if i > 0 and r[i] > 0:
            circles[i] = plt.Circle((x_pf[i], y_pf[i]), r[i], fill=False, 
                                    color='silver')
            cc.add_patch(circles[i])
            line, = cc.plot([x_pf[i], x_pf[i+1]], [y_pf[i], y_pf[i+1]], 
                            color='tab:orange')
            freqs[i] = line
            # plot negative frequency vectors only when enabled
            if args.neg:
                circles_neg[i] = plt.Circle((x_pf[i], -y_pf[i]), r[i], fill=False, 
                                    color='silver')
                cc.add_patch(circles_neg[i])
                line, = cc.plot([x_pf[i], x_pf[i+1]], [-y_pf[i], -y_pf[i+1]], 
                                color='tab:cyan')
                freqs_neg[i] = line
        elif i == 0 and r[i] > 0:
            line, = cc.plot([x_pf[i], x_pf[i+1]], [y_pf[i], y_pf[i+1]],
                            color='tab:orange')
            freqs[i] = line
            if args.neg:
                line, = cc.plot([x_pf[i], x_pf[i+1]], [-y_pf[i], -y_pf[i+1]], 
                                color='tab:cyan')
                freqs_neg[i] = line

    animated_objects = [xy_line, xy_neg_line, re_line, re_neg_line, im_line, 
                    im_neg_line, ab_line, ab_neg_line] + \
                    [circle for circle in circles if circle != None] + \
                    [line for line in freqs if line != None] + \
                    [circle for circle in circles_neg if circle != None] + \
                    [line for line in freqs_neg if line != None]

    return tuple(animated_objects)

###############################################################################

def animate(i):
    """ Adds a new value to x, y and phi and updates the plots.
    
    For i, a new phi (angle) gets calculated where 
    phi = i / n * 2*pi
    For this phi, new x and y values will be calculated and appended to the 
    existing plots.

    Parameters
    ----------
    i : int
        Time counter where one period is completed when i == n.

    Returns
    -------
    list
        Artist objects to be animated.

    """
    
    global x, y, phi
    
    phi = np.append(-(i / n * 2*np.pi), phi)
    
    # sum all frequencies
    for k in range(len(c)):
        z = c[k] * np.exp(1j * k * (-phi[0]))
        x_pf[k+1] = x_pf[k] + z.real
        y_pf[k+1] = y_pf[k] + z.imag
    x = np.append(x, x_pf[-1])
    y = np.append(y, y_pf[-1])
    
    for k in range(len(circles)):
        if circles[k] is not None:
            circles[k].center = x_pf[k], y_pf[k]
        if freqs[k] is not None:
            freqs[k].set_data([x_pf[k], x_pf[k+1]], [y_pf[k], y_pf[k+1]])
        if circles_neg[k] is not None:
            circles_neg[k].center = x_pf[k], -y_pf[k]
        if freqs_neg[k] is not None:
            freqs_neg[k].set_data([x_pf[k], x_pf[k+1]], [-y_pf[k], -y_pf[k+1]])
    re_line.set_data(x, phi)
    re_neg_line.set_data(x, phi)
    im_line.set_data(phi, y)
    im_neg_line.set_data(phi, -y)
    ab_line.set_data(phi, y)
    ab_line.set_3d_properties(x)
    ab_neg_line.set_data(phi, -y)
    ab_neg_line.set_3d_properties(x)
    xy_line.set_data(x, y)
    xy_neg_line.set_data(x, -y)
    
    if i+1 == n_frames:
        global animation_ended
        animation_ended = True

    return tuple(animated_objects)

###############################################################################

if __name__ == "__main__":

    ########## ARGUMENTS ######################################################
    
    parser = argparse.ArgumentParser(
        description="A visual display of a Fourier Synthesis.")
    parser.add_argument('-l', '-e', action="store_true", 
        help="Endless mode, loops the animation, without it stops after one period.")
    parser.add_argument('-r', type=int, default=256,
        help="Resolution of the plots. Default: 256")
    parser.add_argument('-c', type=complex, nargs='+', 
        help="Fourier-Coefficients, takes precedence over -s.")
    parser.add_argument('-s', type=str, default="cos", choices=["cos", "sin", \
        "tri", "rect"], help="Shape of the Function. Default: cos")
    parser.add_argument('-n', type=int, default=9,
        help="Order of Fourier Synthesis. Default: 9")
    parser.add_argument('-w', action="store_true",
        help="If set, the animation does not start until a button is pressed.")
    parser.add_argument('-i', type=int, default=20,
        help="Interval between frames in ms. When reduced, animation will " \
        + "speed up. Default: 20 (Actual speed of animation will depend on " \
        + "your machine's power!)")
    parser.add_argument('-neg', action="store_true",
        help="Add vectors for the negative frequencies.")
    
    args = parser.parse_args()
    
    n = args.r        # resolution of plot
    endless = args.l  # wether to loop (True) or animate only one period (False)
    
    if args.c == None:
        shape = args.s.lower()
        if shape == "cos":
            c = [0, 1]
        elif shape == "sin":
            c = [0, -1j]
        elif shape == "rect":
            c = []
            for i in range(args.n + 1):
                if i % 2 == 0:
                    c.append(0)
                else:
                    c.append(-1j/i)
        elif shape == "tri":
            c = []
            for i in range(args.o + 1):
                if i % 2 == 0:
                    c.append(0)
                else:
                    c.append(1/i**2)
    else:
        c = args.c
        
    ########## VARIABLES ######################################################
    
    r = [abs(z) for z in c]  # absolute values of c / radius
    phi = np.zeros(0)
    x = np.zeros(0)  # real
    y = np.zeros(0)  # imag
    x_pf = [0] * (len(c)+1)  # the pf (per frequency) vars are for the pointers
    y_pf = [0] * (len(c)+1)  # of each frequency, x and y only store the sum
    
    if endless:
        n_frames = None
    else:
        n_frames = n+1
    
    animation_ended = False
    
    ########## MAIN ###########################################################
    
    create_axes()
    
    fig.show()
    
    if args.w:
        plt.waitforbuttonpress()
    
    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=n_frames, 
                                   interval=args.i, blit=True, repeat=endless)

    # loop detects when animation has ended to redraw everything
    # without redrawing, all lines vanish when trying to adjust the axes
    while not animation_ended:
        try:
            plt.waitforbuttonpress()
        except Exception:  # the actual exception depends on matplotlibs backend
            print("Figure closed, ending program.")
            quit()
        
    print("Switching to static view.")
    init()
    
    plt.show()
    print("Figure closed, ending program.")
