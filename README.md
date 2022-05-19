# PyIPCAM

Stream a webcam in a self hosted webapp. 

### Disclaimer
*This is currently under development
Currently only tested on Windows.

### Usage
PyIPCamServer.py (or PyIPCamServer.exe) -port *tcp port,default = 8000* -index *camera index, default=0* -width *image width, default = 640*, -height *image height, default = 400*

Example:
PyIPCamServer -index 0 -width 1280 -height 720
*Use camera 0 with resoltion 1280x720*
