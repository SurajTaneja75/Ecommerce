The repo has these files

-db.py
-final.py
-post_process.py
-requirements.txt
-README.txt

-db.py contains database related code (user need to update the credentials to make it work)
-final.py fetches functions from db and postprocess and run the query
- post_process.py contains code for processing the data after runnung the query in db
-requirements.txt - file containing package info. Install this file before running the code

How to run?

Open final.py file
Pass the parameters including query type, window, start date, end date and category 
Query name currently has 3 options (demand/price/customer) 

I have not included command line parsing in the current code


------------------------------------------------------
How will you manage this code? Design a SDLC process :
(a)	Code versioning and standards -We can do version control using Git to push changes either in main branch or parallel branch. We can track the changes in code as and when needed.
(b)	Product feature tracking - We need to document the feature and their updates. (We use excel to do this. Not sure how else it can be done)
(c)	Deployment - We can use CI/CD pipelines for a smoother deployment
(d)	Monitoring - We can use azure log stream or similar mechanisms to monitor the functioning of code.
(e)	Datasets - Data preprocessing is must to ensure quatlity data is used for processing.
(f)	Upstream and downstream Dependencies - We can keep dependencies in requirements.txt file


