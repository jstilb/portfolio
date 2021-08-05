from selenium import webdriver
from time import sleep
import gzip

job_title_to_search = 'Data Analyst'
location_to_search = 'Denver, Colorado'


class JobBot():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless') # negates visual of interaction
        chrome_options.add_argument('--no-sandbox') # bypasses OS security
        chrome_options.add_argument("--disable-dev-shm-usage") # overcome limited resources problem
        chrome_options.add_argument('incognito') # opens incognito window
        self.driver = webdriver.Chrome(executable_path='/Users/jmsitunes/Desktop/projects/auto_grocery/chromedriver',
                                       options=chrome_options)
        self.driver.delete_all_cookies()

    def get_website(self):
        sleep(5)
        self.driver.get('https://www.linkedin.com/jobs')
        sleep(5)

    def search(self):
        # fills out search for desired job and location indicated in lines 5 & 6

        sleep(1)

        # variables
        job_title_input = self.driver.find_element_by_xpath('//*[@id="JOBS"]/section[1]/input')
        location_input = self.driver.find_element_by_xpath('//*[@id="JOBS"]/section[2]/input')
        exit_autocomplete = self.driver.find_element_by_xpath('/html/body/main/section[1]')
        search_btn = self.driver.find_element_by_xpath('/html/body/main/section[1]/section/div[2]/button[2]')

        job_title_input.send_keys(job_title_to_search)
        sleep(3)

        location_input.clear()
        location_input.send_keys(location_to_search)
        sleep(2)

        exit_autocomplete.click()
        sleep(2)
        search_btn.click()

    def scrape_web_links(self):

        # scrolls down page to load all results
        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # collect all job links in search result
        links = self.driver.find_elements_by_xpath("//*[@href]")
        clean_links = [x.get_attribute('href') for x in links if "jobs/view" in x.get_attribute('href')]
        job_titles = []
        jobs_txt = ''
        cnt = 0

        # searches each job link and scrapes information
        for link in clean_links:
            try:
                # pull up webpage & full job description
                self.driver.get(str(link))
                sleep(2)
                show_more_btn = self.driver.find_element_by_xpath(
                    '/html/body/main/section[1]/section[3]/div[1]/section/button[1]')
                show_more_btn.click()
                sleep(2)

                # scrape job info
                job_title = self.driver.find_element_by_xpath(
                    '/html/body/main/section[1]/section[2]/div[1]/div[1]/h1')
                job_titles.append(job_title.text)

                txt = self.driver.find_element_by_class_name('description').text
                jobs_txt = jobs_txt + ' ' + txt

            except:
                pass
        self.driver.quit()

        # download file
        if not jobs_txt:
            print('string is empty. Error occurring in scraping.')
        else:
            with gzip.open('/Users/jmsitunes/Desktop/projects/job_bot/' + job_title_to_search + '.txt.gz', 'wb') as f:
                f.write(jobs_txt.encode())




bot = JobBot()
bot.get_website()
bot.search()
bot.scrape_web_links()
