# About the project
- There are three directories in the "FirstWindow", in which "Part One" & "Part Two" record the process I learnt PyQt6. And in the rest is the main code of the project.
> Part Nine
> > The main programs 
> > > multimedia.py: the main function module
> > >
> > > DrawingBoard.py: the main test module
> > >
> > > color.py: include some color definition
> > >
> > > MATRIX.py: include the transform matrix to be used
> > > 
> > > UDP.py: include the UDP settings information
> > > 
> > Tools & Test
> > > camera calibration.py
> > > 
> > > transformationMatrix.py
> > >
> > > UDPsocket.py

# Learn Process Record
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

## Fri. 20th, Oct
### Learing Progress
- Learnt about basic qt widget, label, button, layout
- had seen the 2.7 episode of the course

### The problems I encountered
- no 

## Sun. 22nd, Oct
### The problems I encountered
1. the class "QPushbutton.clicked" doesn't have the method "connect" 
    - Cause: Not found yet. I guess it's related to pycharm IDE.
    - Solution: Emmm....Actually, it solved itself.

### Learning Progress
- Learnt about all the basic widgets in PyQt6
- had seen the 3.9 episode of the course

## Mon. 23rd, Oct
### Learning Progress
- built up a stream client
- learnt about socket udp and opencv

### No Problems Occured

## Nov. 25th, Sat

 It's been a long time since I updated this markdown last time. I'm getting lazier and lazier(TAT). Now that the mid-term examination has finished, it's necessary for me to regain my dream and be busy with my study

 ### Learning Progress
 - finished the camera calibration
 - created a drawing board where a transformation matrix need to be found

 ### Problems I encountered
 - At first, the result of calibration and undistort was a piece of shit, and I asked some predecessors but found no answer. Therefore, I scanned the code carefully, and found that even if I fed the program plenty of images, it only "digest" three of them. It didn't find chessboard on the rest. So, I photoed more images, and finally got adequate data to complete the calibration.
 
 ## Nov. 28th, Tue

 ### Learning Progress
 - solved the problem that Qpainter cannot draw on the Qlabel. Solution: use QPainter to create a pixmap which is used to fill a new Qlabel created.
 
## Dec. 3rd, Sun
### Learning Progress
- created a drawing board successfully.
### Problems
- have no figured out how to use the function/method Qpixmap.transformed() yet. 

## Dec. 17th, Sun
### Learning Progress
- figured out how to use the class Qtransform

## Jan 6th, Sat. 2024
It's been a long day ~~without you my friend ~~ since I upgraded this README last time. During the time, I lay down a lot. Sometimes, I was confused by the protobuf, while ohter times I was busy with OOP. Anyhow, now I finally worked it out, but still left some bugs in the demo to be solved.

### Bugs remaining
- Process finished with exit code 139 (interrupted by signal 11:SIGSEGV). It's a buffer overflow ERROR, but I have not figured out where is it.
- While the program running, it stuck the Athena somehow, I don't know why.