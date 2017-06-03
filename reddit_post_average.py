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



def get_max_vote(sub_link_name):
	driver.find_element_by_link_text(sub_link_name).click()
	(driver.page_source).encode('utf-8')

	upvote_count = driver.find_elements_by_css_selector(".score.unvoted")

	y = 0
	try:
		moderator = driver.find_element_by_css_selector("a.moderator")
		y += 1
	except NoSuchElementException:
		pass

	try:
		promote = driver.find_element_by_css_selector("span.promoted-span")
		y += 1
	except NoSuchElementException:
		pass

	#loop and count post
	avg = 0
	for x in range(y, len(upvote_count)):
		up_c = upvote_count[x].text.encode('utf-8').strip()
		if not "k" in up_c:
			try:
				avg_post += float(up_c)
			except:
				pass
		elif "k" in up_c:
			temp_post = up_c.replace("k", "")
			avg += float(temp_post) * 1000

	avg_post /= 25
	min_post_amount = 10000
	if avg_post > min_post_amount:
		assert "Subreddit is below minimum up vote count"

	return avg_post


sub = ['FUNNY', 'PICS', 'NEWS', 'VIDEOS', 'ASKREDDIT']
average_reddit_post = 0

for x in sub:
	average_reddit_post += get_max_vote(x)

print("\nThe average reddit subreddit of Reddit: " + str(average_reddit_post/len(sub)))

assert "No results found." not in driver.page_source
time.sleep(5)
driver.close()
