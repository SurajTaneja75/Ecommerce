import argparse
from db import *
from post_process import *

# Pass the query type, window, start date, end date and category
df = execute_query('demand', 'daily', '2009-01-01', '2012-01-01', 'T-shirt')

post_process(df)
