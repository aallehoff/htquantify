from urllib.request import urlopen
from bs4 import BeautifulSoup # pylint: disable=import-error

class Hypertext():
    # Initialize object
    def __init__(self, url):
        self.url = url
        self.__fetch_content()
        self.__parse_content()
        self.__clean_content()
        self.__load_content()

    
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
        
    def __clean_content(self):
        # Strip out CSS and JavaScript
        for code in self.soup(['style', 'script']):
            code.decompose()

    def __load_content(self):
        # Load all elements into a list
        self.tags = []
        for element in self.soup.findAll():
            self.tags.append(element.name)

        # Load all text nodes into a list
        self.text = self.soup.findAll(text=True)

    def quantify(self):
        quantities = {
            'overall': {
                'tags': 0,
                'text': 0
            },
            'tags': {},
            'text': {}
        }

        self.__counter('tags', self.tags, quantities)
        self.__counter('text', self.text, quantities)

        return quantities

    def __counter(self, category, attribute, buffer):
        for item in attribute:
            buffer['overall'][category] += 1
            try:
                buffer[category][item] += 1
            except KeyError:
                buffer[category][item] = 1

class HypertextQuantifier():
    def __init__(self, q):
        pass

    def __invert_dictionary(self, d):
        inversion = {}

        # Loop through the items in the given dictionary
        for key, value in d.items():
            
            # Convert old values into new keys that store lists of old keys
            print(value)
            if value in inversion.keys():
                # Append old key to new values
                inversion[value].append(key)
            else:
                # Set old value as new key
                inversion[value] = [key]

        return inversion