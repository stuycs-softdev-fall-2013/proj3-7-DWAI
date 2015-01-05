proj3-7-DWAI
============

###Group Members:
- Alvin Leung
- Vivian Wang
- Michele Lin
- Judy Mai

###Project:
Our project, temporarily dubbed Google Paint, was intended to be a version of Google Docs for artists. Multiple artists could collaborate on a drawing simultaneously, while having most of the basic features of more complex graphics programs available to them.
Although we do not yet have multi-person functionality working, we have a canvas that allows users to drawing, change their pen size and color, as well as undo and redo their strokes. Each user also has a gallery that lets them view images they have saved.
For future prospects, we plan on implementing chat and view/edit settings as well as an option to automatically post to social networks such as Facebook, Tumblr, deviantART, etc. 


###Things to work on
1. multi-user chat functionality using node.js and socket.io 
2. update canvaspg with other paint uses: eraser, fix save, consider adding an File-save thing and a change canvas size
3. update profile page and allow user to customize settings to post to Facebook, Tumblr, etc. with something similar to oauth-google
4. see how we can get multiple users adding in a stroke (check out the server stuff and how we will only be doing the undo/redo stuff to the user who made them, not to the entire canvas and not undoing/redoing other people's stuff.
5. think about new animations and site navigation that will make the site more interactive and interesting


###Bugs I'm noticing / Things we should add
- Quick fixes:
   1. default canvas width is too large
   2. pen size (add a text box to type it in), also slight lag with size-update after scrolling

- Bigger errors:
   1. Undo/redo still don't work
   2. 
