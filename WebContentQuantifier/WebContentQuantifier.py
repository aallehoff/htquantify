from urllib.request import urlopen

class WebContent():
    # Initialize object
    def __init__(self, url):
        self.url = url
    
    # Send HTTP request and store response
    def __fetch_content(self):
        with urlopen(self.url) as response:
            # Check for HTTP errors
            if response.code not in range(200, 300):
                raise Exception(f'Encountered HTTP Error: {response.code}, {response.msg}.')

            # Store relevent information
            self.date = response.getheader('Date')
            self.type = response.getheader('Content-Type')
            self.content = response.read()

    # Parse content