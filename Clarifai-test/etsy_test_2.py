from etsy import Etsy
import json
import pprint

e = Etsy('w31e04vuvggcsv6iods79ol7', 'dgicdc7qts') # gotten from signing up at etsy.com/developers

#magenta_listings = e.show_listings(color='#FF00FF') -- this works
wedding = e.findBrowseSegmentListings(keywords='wedding')

# pprint.pprint(magenta_listings)

#method_table = e.getMethodTable()
print wedding