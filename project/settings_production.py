from .settings import *

# Update SITE infos to use the common port 80 to publish the webapp
# Edit to another port if you dont want to serve the webapp on another port
SITE_FIXED = {
    'name': "Recalbox Manager",
    'ip': None, # If None find the ip automatically, else use a string to define another hostname
    'port': None, # If None no port is appended to hostname, so the server have to be reachable from port 80
}
