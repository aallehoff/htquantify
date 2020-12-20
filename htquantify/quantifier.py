import re
from urllib.request import urlopen

from bs4 import BeautifulSoup # pylint: disable=import-error
from rich.console import Console # pylint: disable=import-error
from rich.table import Table # pylint: disable=import-error

class Hypertext():
    """Gathers and stores a representation of a Hypertext document."""

    def __init__(self, url):
        self.url = url

        # Fetch, parse, clean, load, tokenize
        self.__fetch_content()
        self.__parse_content()
        self.__clean_content()
        self.__load_content()
        self.__tokenize_text()

    def __fetch_content(self):
        """Opens a URL and saves its content and metadata to the object."""

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

    def __parse_content(self):
        """Parses HTML"""

        self.soup = BeautifulSoup(self.raw, 'html.parser')
        
    def __clean_content(self):
        """Removes CSS and JavaScript from parsed document"""

        for code in self.soup(['style', 'script']):
            code.decompose() # remove without storing

    def __load_content(self):
        """Loads elements and text nodes into object for later use"""

        # Load all elements into a list
        self.tags = []
        for element in self.soup.findAll():
            self.tags.append(element.name)

        # Load all text nodes into a list
        self.text = self.soup.findAll(text=True)

    def __tokenize_text(self):
        """Convert text node data into easily countable format"""

        # Naive whitespace and punctuation tokenizer
        tokenizer = re.compile(r'[\s,.!?/;:"()[\]{}<>]+')

        # Setup buffer
        dirty = self.text
        clean = []

        # Tokenize
        for item in dirty:
            clean.extend(tokenizer.split(item))

        # Remove empty strings from results
        clean = [item for item in clean if item]

        # Write results to object
        self.text = clean

    def quantify(self):
        """Return results of counting tags and tokens"""

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

        return HypertextQuantities(quantities)

    def __counter(self, category, attribute, buffer):
        """Counts the contents of an attribute on the object"""

        for item in attribute:
            buffer['overall'][category] += 1
            try:
                buffer[category][item] += 1
            except KeyError:
                buffer[category][item] = 1


class HypertextQuantities():
    """Stores and provides methods for manipulating the results of quantification"""
    def __init__(self, q):
        # Seperate overall stats from category stats
        self.__overall = q.pop('overall')

        # Extract list of categories
        self.__cats = list(q.keys())

        # Load categories directly into object
        self.__dict__.update(q)

        # Generate inverted categories
        new_cats = []
        for name in self.__cats:
            new_cat = f'{name}_by_count'
            self.__dict__[new_cat] = self.__invert_dictionary(self.__dict__[name])
            new_cats.append(new_cat)
        self.__cats.extend(new_cats)

    def __invert_dictionary(self, d):
        """Non-destructively flips keys and values in a given dictionary"""

        inversion = {}

        # Loop through the items in the given dictionary
        for key, value in d.items():
            
            # Convert old values into new keys that store lists of old keys
            if value in inversion.keys():
                # Append old key to new values
                inversion[value].append(key)
            else:
                # Set old value as new key
                inversion[value] = [key]

        # Sort tokens in list in place
        for key, value in inversion.items():
            value.sort()

        return inversion

    def get_categories(self):
        """Accessor method for self.__cats"""
        return self.__cats
    
    def get_overall(self):
        """Accessor method for self.__overall"""
        return self.__overall


class Display():
    """Provides methods for displaying output"""

    def __init__(self, site, data, opts):
        self.site = site
        self.data = data
        self.opts = opts
    
    def output(self):
        """Performs the output of results"""

        # Create a table with striped rows
        self.table = Table(title=self.site.url, row_styles=['', 'grey50'])

        # Build and fill table
        self.__build_columns()
        self.__fill_rows()

        # Print to STDOUT
        console = Console()
        console.print(self.table)

    def __build_columns(self):
        """Builds the columns in a rich table"""
        
        # QUANTITY
        if self.opts.sort_by == 'quantity':
            self.table.add_column('Quantity', justify='right')
            self.table.add_column('Token', justify='left')
        # TOKEN
        elif self.opts.sort_by == 'token':
            self.table.add_column('Token', justify='right')
            self.table.add_column('Quantity', justify='left')

    def __fill_rows(self):
        """Fills the rows in a rich table"""

        # QUANTITY
        if self.opts.sort_by == 'quantity':
            # TEXT
            if self.opts.include == 'text':
                for k, v in sorted(self.data.text_by_count.items(), reverse=True):
                    self.table.add_row(str(k), ', '.join(v))
            # TAGS
            elif self.opts.include == 'tags':
                for k, v in sorted(self.data.tags_by_count.items(), reverse=True):
                    self.table.add_row(str(k), ', '.join(v))
        # TOKEN
        elif self.opts.sort_by == 'token':
            # TEXT
            if self.opts.include == 'text':
                for k, v in sorted(self.data.text.items()):
                    self.table.add_row(k, str(v))
            # TAGS
            elif self.opts.include == 'tags':
                for k, v in sorted(self.data.tags.items()):
                    self.table.add_row(k, str(v))