from urllib.request import urlopen

class WebContent():
    # Initialize object
    def __init__(self, url):
        self.url = url
    
    # Send HTTP request and store response
    # Parse content