  <p align="left">
    Self-driving car based on Python and OpenCV 
    <br /><br />
    <a href="https://opencv.org/"><strong>OpenCV</strong></a>
    <br />
    <a href="https://www.python.org/"><strong>Python</strong></a>
    <br /><br /><br /><br />
    The back and frontend of a custom made self-driving "car".
  <br />
  The frontend is being run on the car itself, using a Raspberry Pi to establish an internet connection (a wifi hotspot established on the backend pc).
  The Python code, once run, connects to the backend - takes input from a usb camera, processes and sends it to the backend. Once data is received from the backend,
  the RPi will execute those commands and control two motors (GPIO pins). 
  
  The backend is being run on a host pc, it receives the camera feed from the frontend (the car) and processes it using OpenCV, before sending commands back to the car. 
  
  </p>

