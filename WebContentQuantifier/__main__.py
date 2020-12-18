import argparse
from urllib.parse import urlparse

import quantifier

# Parse command line arguments
clarg_parser = argparse.ArgumentParser(description="Quantify the contents of a hypertext document from a URL.")
clarg_parser.add_argument("url")
clarg_parser.add_argument('-s', '--sort-by', dest='sort_by', choices=['quantity', 'token'], default='quantity')
clarg_parser.add_argument('-i', '--include', dest='include', choices=['all', 'tags', 'text'], default='text')
clargs = clarg_parser.parse_args()

# Validate URL
parsed_url = urlparse(clargs.url)
if not (parsed_url.scheme and parsed_url.netloc):
    raise Exception("Invalid URL.")

# Instance Hypertext class
hyper = quantifier.Hypertext(clargs.url)
quants = hyper.quantify()