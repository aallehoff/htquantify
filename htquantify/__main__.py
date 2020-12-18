import argparse
from urllib.parse import urlparse

from rich.console import Console # pylint: disable=import-error
from rich.table import Table # pylint: disable=import-error

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

# Display results
results = Table(title=hyper.url, row_styles=['', 'grey50'])

results.add_column('Quantity', justify='right')
results.add_column('Token', justify='left')

for k, v in quants.text_by_count.items(): # pylint: disable=no-member
    results.add_row(str(k), ', '.join(v))

console = Console()
console.print(results)