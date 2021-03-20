# A Visualisation of the Fourier-Synthesis

This script is written in Python 3.8.8 and uses the matplotlib and numpy modules.

The figure in which the animation takes place is divided into four axes. 
In the top left, the complex plane is displayed, the top right shows the
imaginary part of the signal, the bottom left shows the real part of the 
signal and the bottom right shows the complex plane in a 3-dimensional 
view over the time. The real and imaginary axes are formatted in way so 
that they share their respective axis with the complex plane in the top left.

The time is normalized to the period of the base frequency where 2 pi equals 
one full period. The signal is plotted into the past, each value along the 
signal starts at t = 0 and moves towards negative time. That means the current 
value to which the pointers in the comlex plane add to is always at t = 0.

The positive frequencies are plotten in red, the negative frequencies are 
plotted in blue with a dotted line. By defaul, only the positive frequencies have their
complex vectors plotted in the comlex plane.

By default the script will animate a cosine for one period. To change this, 
use arguments when calling the script.


## Arguments

The script can be called with numerous arguments. Calling it with `-h` will 
give a quick overview over all possible arguments.

`-l`, `-e` : Endless mode. Loops the animation. Usually only one period of the signal will be animated, 
when called with `-l` or `-e` the animation will loop until the figure is closed.

`-w` : Wait before starting animation. When `-w` is set, the figure will be 
created, but waitforbuttonpress() is called before the animation starts. 
This means, that the animation will only start after pressing a button with 
the figure as the active window.

`-neg` : Add vectors for the negative frequencies. By default, only the vectors
for the positive frequencies are plotted in the complex plane. This option will
also plot vectors for the negative frequencies.

`-s S` : Shape of the signal where `S` is a String chosen from `{cos, sin, tri, rect}`. 
The shapes refer to the shape of the real signal with cos = cosine, sin = sine, 
tri = triangle, and rect = rectangle. The default order for tri and rect is 9, 
but can be changed with `-n`. The default shape is `cos`.

`-n N` : Order of Fourier Synthesis where `N` is an integer value. `N` is the 
order for the tri and rect shape. The default order is 9.

`-c C_0 C_1 C_2 ...` : Fourier-Coefficients where `C_n` is a complex value. 
When `-c` is set, the shape and order will be ignored. `-c` takes precedence 
over `-s`. This allows to use custom coefficients. Remember: `C_0` is the 
DC-offset, `C_1` is for the base frequency.

`-r R` : Resolution of the plots where `R` is an integer value. `R` gives the 
number of points to plot in one period of the signal. For the full display 
from 0 to 2pi, n is increased by one internally. Decreasing `R` speeds up the 
animation but reduces the smoothness of the plotted signal. 
The default resolution is 256.

`-i I` : Animation interval where `I` is an integer value. `I` is the time in 
milliseconds between the frames of the animation. Decreasing `I` will speed up 
the animation. The actual speed depends on the power of your machine! 
The default interval is 20.


## Examples

`python fourier_animation.py -r -c 0.2 1 0.2j` --> This will loop the animation 
of the signal with Fourier-Coefficients [0.2, 1, 0.2j].

`python fourier_animation.py -s rect -w` --> This will animate one period of a 
9th order rectangle signal, but the animation will only start on pressing a button.

`python fourier_animation.py -s tri -c 0 1` --> This will animate one period of 
the cosine defined by `-c`. The shape `-s` has no effect in this case.


## License

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
