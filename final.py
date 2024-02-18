from db import *
from post_process import *

# Pass the query type, window, start date, end date and category
df = execute_query('demand', 'daily', '2010-08-01', '2010-08-30', 'T-shirt')

post_process(df)
