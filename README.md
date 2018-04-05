# Saaarchasm

Created by: Brian Be, Jonathan Quach, Leslie Liang

### Client
* Browser accessible @ localhost:5000 (fully supported on Chrome)
* Debug: If image/css/js source code updates are not reflected on the webpage, open up the developer tools (opt-cmd-i) and right click the refresh button to clear the cache and hard reload.

### Server
To start the server, use the command:
~~~
$ ./startServer.sh
~~~

To run as a background process, use instead:
~~~
$ ./startServer.sh &
~~~

This will initate a virtual environment to enable Google's text-to-speech api for python 3. To start up the server manually from within a configured virtual environment, use instead:

~~~
$ pip install requirements.txt
$ python main.py 
~~~

### Running Virtual Environment
A virtual environment can be started by executing the following commands:

~~~
$ virtualenv env
$ source env/bin/activate
~~~

### Frameworks and APIs
* Flask for URI routing
* jQuery for AJAX
* Google's text-to-speech API