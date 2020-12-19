import argparse
import sys
from urllib.parse import urlparse

import quantifier

# Parse command line arguments
clarg_parser = argparse.ArgumentParser(description="Quantify the contents of a hypertext document from a URL.")
clarg_parser.add_argument("url", help='Must include protocol, and address')
clarg_parser.add_argument('--debug', action='store_true')
clarg_parser.add_argument('-s', '--sort-by', dest='sort_by', choices=['quantity', 'token'], default='quantity')
clarg_parser.add_argument('-i', '--include', dest='include', choices=['tags', 'text'], default='text')
clargs = clarg_parser.parse_args()

# Set debug level
if not clargs.debug:
    # Suppress tracebacks
    sys.tracebacklimit = 0

# Validate URL
parsed_url = urlparse(clargs.url)
# If either protocol or address is missing
if not (parsed_url.scheme and parsed_url.netloc):
    # Missing protocol
    if not parsed_url.scheme:
        raise ValueError("Invalid URL; missing protocol.")
    # Missing address
    elif not parsed_url.netloc:
        raise ValueError("Invalid URL; missing address.")

# Instance Hypertext class, and quantify
hyper = quantifier.Hypertext(clargs.url)
quants = hyper.quantify()

# Display results
display = quantifier.Display(hyper, quants, clargs)
display.output()