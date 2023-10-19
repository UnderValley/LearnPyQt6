# LearnPyQt6
## Thur. 19th, Oct
### What I've achieved
* created windows and learnt some initialization methods

### The problems I encountered
1. Cannot install pycharm
    - Cause: I have not found yet
    - Solution: Searched on the Google, and used "Ubuntu software" to install
2. Cannot run my code successfully
    - Error Message: t.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.
    This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.
    Available platform plugins are: eglfs, linuxfb, minimal, minimalegl, offscreen, vnc, xcb.
    - Cause: lack of certain dependencies
    - Solution: At first, I tried to follow the error message to reinstall PyQt6, but had no impact. So, I searched the Internet again, and found the spell below 
    '''
    sudo apt-get install '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev
    ''' 
    and it finally solved this problem.
    
### Problems Unsolved

* The directory "venv" in "MyWindows" cannot be pushed to my repository
