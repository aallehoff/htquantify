from urllib.request import urlopen
from bs4 import BeautifulSoup # pylint: disable=import-error

class WebContent():
    # Initialize object
    def __init__(self, url):
        self.url = url
        self.__fetch_content()
        self.__parse_content()

    
    # Send HTTP request and store response
    def __fetch_content(self):
        with urlopen(self.url) as response:
            # Check for HTTP errors
            if response.code not in range(200, 300):
                raise Exception(f'Encountered HTTP Error: {response.code}, {response.msg}.')
            else:
                self.code = response.code
                self.msg = response.msg

            # Store relevent information
            self.date = response.getheader('Date')
            self.type = response.getheader('Content-Type')
            self.raw = response.read()

    # Parse content
    def __parse_content(self):
        self.soup = BeautifulSoup(self.raw, 'html.parser')
        
        # Strip out CSS and JavaScript
        for code in self.soup(["style, script"]):
            code.decompose()

        # Tokenize textual content
        self.tokens = self.soup.findAll(text=True)