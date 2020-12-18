import argparse
from urllib.parse import urlparse

import quantifier

# Parse command line arguments
clarg_parser = argparse.ArgumentParser(description="Quantify the content located at a given URL.")
clarg_parser.add_argument("url")
clargs = clarg_parser.parse_args()

# Validate URL
parsed_url = urlparse(clargs.url)
if not (parsed_url.scheme and parsed_url.netloc):
    raise Exception("Invalid URL.")

# Instance Hypertext class
hyper = quantifier.Hypertext(clargs.url)
quants = hyper.quantify()