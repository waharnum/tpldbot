from lxml import etree
from random import randint

result_feed_URL = "http://www.torontopubliclibrary.ca/rss.jsp?N=38550&Erp=0"

# Get the feed without records to make finding the total records faster
tree = etree.parse(result_feed_URL)

# Get the total results
total_results = tree.find('channel').find('results').find('total-results').text

# print(total_results)

# Generate a random number from the total results

image_number = randint(1, int(total_results))

print ("You should get image #" + str(image_number))

# Get the record associated with that random number

record_feed_URL = "http://www.torontopubliclibrary.ca/rss.jsp?N=38550&Erp=1&No=" + str(image_number)

record_tree = etree.parse(record_feed_URL)

item = record_tree.find('channel').find('item')

item_title = item.find('title').text

item_record = item.find('record')

item_id = item_record.find('recordId').text

item_image_file_name = item_record.xpath("./attributes/attr[@name='p_file_name']/text()")

# http://static.torontopubliclibrary.ca/da/images/MC/pcr-473.jpg

# We have to convert the file name to lowercase

item_image_URL = "http://static.torontopubliclibrary.ca/da/images/MC/" + item_image_file_name[0].lower()

print("Title: " + item_title)
print("Record ID: " + item_id)
print("Image URL:" + item_image_URL)

# Make a tweet from it
