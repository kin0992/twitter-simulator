######################################################################
######################################################################
##
## PyCX 0.31
## Complex Systems Simulation Sample Code Repository
##
## 2008-2013 (c) Copyright by Hiroki Sayama
## 2012 (c) Copyright by Chun Wong & Hiroki Sayama
##          ("pycxsimulator-old.py", "realtime-simulation-template-old.py")
## 2013 (c) Copyright by Przemyslaw Szufel & Bogumil Kaminski
##          Extensions to GUI module, some revisions
## All rights reserved.
##
## See LICENSE.txt for more details of license information.
##
## Send any correspondences to:
##   Hiroki Sayama, D.Sc.
##   Associate Professor, Departments of Bioengineering &
##   Systems Science and Industrial Engineering
##   Binghamton University, State University of New York
##   P.O. Box 6000, Binghamton, NY 13902-6000, USA
##   Tel: +1-607-777-4439  Fax: +1-607-777-5780
##   Email: sayama@binghamton.edu
##
## http://pycx.sf.net/
##
######################################################################
######################################################################


1. What is PyCX?

The PyCX Project aims to develop an online repository of simple,
crude, yet easy-to-understand Python sample codes for dynamic complex
systems simulations, including iterative maps, cellular automata,
dynamical networks and agent-based models. You can run, read and
modify any of its codes to learn the basics of complex systems
simulation in Python.

The target audiences of PyCX are researchers and students who are
interested in developing their own complex systems simulation software
using a general-purpose programming language but do not have much
experience in computer programming.

The core philosophy of PyCX is therefore placed on the simplicity,
readability, generalizability and pedagogical values of simulation
codes. This is often achieved even at the cost of computational speed,
efficiency or maintainability. For example, PyCX does not use
object-oriented programming paradigms, it does use global variables
frequently, and so on. These choices were intentionally made based on
our experience in teaching complex systems modeling and simulation to
non-computer scientists.

For more information, please see the following open-access article:
Sayama, H. (2013) PyCX: A Python-based simulation code repository for
complex systems education. Complex Adaptive Systems Modeling 1:2.
http://www.casmodeling.com/content/1/1/2


2. What's new in version PyCX 0.3 / 0.31?

* Przemyslaw Szufel & Bogumil Kaminski at the Warsaw School of
  Economics made a substantial improvement to the "pycxsimulator.py"
  GUI module, implementing interactive control of model and
  visualization parameters. This improvement is fully backward
  compatible, so you can run old PyCX 0.2 simulator codes with this
  new GUI module.

* Several new sample simulation codes were added, including:

    Contributions by Przemyslaw Szufel & Bogumil Kaminski:
    - "ca-schelling.py" (Tom Schelling's segregation model)
    - "ca-rumor.py" (Spread of rumor)
    The above two codes show how to use the new interactive parameter
    setting feature.

    Other additions of dynamical network models:
    - "net-randomwalk.py" (Random walk on a network)
    - "net-voter.py" (Voter model of opinion formation on a network)
    - "net-epidemics-adaptive.py" (Epidemics on a network, with adaptive link cutting)
    - "misc-fileio-csv.py" (Example of how to read/write CSV files)

* Revision made to 0.31: ttk is used as a graphics backend instead of
  Tix, so that Mac users can run the sample codes without installing
  Tix.


3. How to use it?

(i) Install Python 2.7, NumPy, SciPy, matplotlib and NetworkX.
Installers are available from the following websites:
  http://python.org/
  http://scipy.org/
  http://matplotlib.org/
  http://networkx.github.io/

(ii) Choose a PyCX sample code of your interest.

(iii) Run it. This should be just double clicking the file in most cases.

(iv) Read the code to learn how the simulation was implemented.

(v) Change the code as you like.


Questions? Comments? Send them to sayama@binghamton.edu.
