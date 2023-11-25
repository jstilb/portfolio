# Job Bot
In this project, I created a bot to scrape data from LinkedIn job description for aid in skill development.
## Files

### job_bot.py
A python script that takes in a takes in a job title and a location & scrapes data from relevant job postings using a selenium chromedriver bot. It generates a file that can then be run via the nlp_analysis.py script.

### nlp_analysis.py
A script to process the text data generated from job_bot.py. It outputs a sorted list of n_grams to help the user ascertain what companies are looking for. 
