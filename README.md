Titta is a toolbox for using eye trackers from Tobii Pro AB with Python,
specifically offering integration with [PsychoPy](https://www.psychopy.org/). A Matlab version
that integrates with PsychToolbox is also available from
https://github.com/dcnieho/Titta

Cite as:
Niehorster, D.C., Andersson, R., & Nyström, M., (in prep). Titta: A
toolbox for creating Psychtoolbox and Psychopy experiments with Tobii eye
trackers.

For questions, bug reports or to check for updates, please visit
https://github.com/marcus-nystrom/Titta. 

Titta is licensed under the Creative Commons Attribution 4.0 (CC BY 4.0) license.

To get started on Windows:
1. Download [PsychoPy (version 3.1.5 or higher](https://www.psychopy.org)
1. Download and install [git](https://www.git-scm.com/downloads)
1. Open the command window
	1. Go the the PsychoPy folder (e.g., C:\Program Files (x86)\PsychoPy3)
	1. type 'python -m pip install git+https://github.com/marcus-nystrom/Titta.git#egg=Titta' 
1. Download the 'examples' folder and run read_me.py (first change the monitor settings and the eye tracker name in read_me.py).
	
Alternatively:
1. Download [PsychoPy (version 3.1.5 or higher](https://www.psychopy.org)
1. Install websocket-client (for Tobii Pro Lab integration)
	1. Open the command window
	1. Go the the PsychoPy folder (e.g., C:\Program Files (x86)\PsychoPy3)
	1. type 'python -m pip install websocket-client
1. Download or clone the Titta folder
1. Add the downloaded Titta-folder to path in PsychoPy (under file->preferences)
1. Run read_me.py (first change the monitor settings and the eye tracker name in read_me.py).

Tested with PsychoPy v. 3.1.5 on Windows 10 using Python 3.6. Ideally, make sure that the eye tracker is detected and works in 
the [Tobii Eye Tracker Manager](https://www.tobiipro.com/product-listing/eye-tracker-manager/) before trying to use it with Titta.