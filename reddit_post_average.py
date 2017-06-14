from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

options = webdriver.ChromeOptions()
#options = webdriver.Firefox()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://reddit.com/')
assert "reddit: the front page of the internet" in driver.title


# This gets average vote count per subreddit
#
#
def get_avg_vote(sub_link_name):
	driver.find_element_by_link_text(sub_link_name).click()
	upvote_count = driver.find_elements_by_css_selector(".score.unvoted")

	# Checks if there is a mod post and if so, add to counter to skip
	y = 0
	try:
		moderator = driver.find_element_by_css_selector("a.moderator")
		y += 1
	except NoSuchElementException:
		pass

	# Checks if there is a sponor post and if so, add to counter to skip
	try:
		promote = driver.find_element_by_css_selector("span.promoted-span")
		y += 1
	except NoSuchElementException:
		pass

	# Count all the votes and convert post that are in the thousand range
	avg_post = 0
	for x in range(y, len(upvote_count)):
		up_c = upvote_count[x].text.encode('utf-8').strip()
		if not "k" in up_c:
			try:
				avg_post += float(up_c)
			except:
				pass
		else:
			temp_post = up_c.replace("k", "")
			avg_post += float(temp_post) * 1000

	# Get average vote from the subreddit
	avg_post /= (len(upvote_count) - y)

	# Condition to see if average vote is below a threshold
	min_post_amount = 2000
	if avg_post < min_post_amount:
		print("Subreddit is below minimum up vote count: " + str(avg_post))
		assert False 

	return avg_post

# Contains subreddits to go to and get votes
sub = ['FUNNY', 'PICS', 'NEWS', 'VIDEOS', 'ASKREDDIT']
average_reddit_post = 0

# Loops and calls get_avg_vote to find the subbreddit average post
for x in sub:
	average_reddit_post += get_avg_vote(x)

print("\nThe average votes for the selected subreddits of Reddit is: " + str(average_reddit_post/len(sub)))

assert "No results found." not in driver.page_source
time.sleep(5)
driver.close()
