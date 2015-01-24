# netfm
In-browser file manager with advanced features

# Running Net-FM
Please note that this is under heavy development and is by no means ready for production (or for testing).
If you're still curious about this, here's how to run it in a nutshell:

```
virtualenv ~/netfm-test
cd ~/netfm-test
source bin/activate
python -m netfm
```
This will start a Flask webserver in debug mode on port 8080 and you can login via http://localhost:8080
As of 24.01.2015 it can only display files (supported by your browser), folders and create folders.

