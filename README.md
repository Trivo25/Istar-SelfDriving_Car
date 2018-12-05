# ISTAR Autonomous

Self-driving car using a Raspberry Pi, OpenCV and a host PC.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Features

```
 - Computer Vision with OpenCV
   - it recognizes contours (a small, black 1cm thick line on a white underground works the best so far - it also works with other colors or contours!)
 - Client sends video stream to the Host PC
 - Host PC receives this stream and does all the Computer Vision based calculations 
 - Host PC sends instructions back to the Client (e.g turn left, turn right, go straight)
```



### Prerequisites

 ```
Python 2.7
 - numpy
 - Mathplotlib
 - OpenCV
```

### Installing

It's simple; all you need to do is..
```
- change both IPs in Server.py and Client.py
- open all ports on both of your machines (RPi and Host-PC)
```

Then you're good to go! Don#t forget to plug in a camera.



