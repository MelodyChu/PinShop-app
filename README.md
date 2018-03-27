# PinShop

## How it works

Video demo: https://www.youtube.com/watch?v=P_2WOC4xAKw&feature=youtu.be

Pinshop is a full stack web application that enables people to search, discover, and shop for clothing inspired by their pins on Pinterest or photos elsewhere online. The Pinterest API integration allows users to automatically pull their pins given their Pinterest username and filter by a specific board for easier searching. Alternatively, users who choose not to use a Pinterest account can also directly enter in an image URL that they would like to use as the foundation of their image search query.

Once the user selects a pin of interest or enters an image URL, they can start searching for similar clothing styles to shop through and buy. Their top, pant, and shoe sizes are automatically applied by default for each search. 

Once the search query is submitted, the Clarifai image recognition API extracts the primary clothing pieces and colors from the image, and if a pin is used for search, those concepts are combined with the pin's tags and descriptions for additional metadata on clothing style, textures, and colors. Finally, the combined query -- along with the user's sizes -- are passed to the ShopStyle API, which aggregates inventory from major online retailers to serve up the most relevant clothing results that are ready for purchase.

Users can filter their results by price and by brand, and bookmark results to purchase for later.

## Technologies Used

**APIs:** Pinterest, Clarifai Image Recognition, ShopStyle, Etsy

**Frontend:** JS, Jquery, AJAX, React, CSS (Flexbox), HTML

**Backend:** Python, Flask, PostgreSQL

<img src="/static/search_screenshot.png" />

<img src="/static/results_screenshot.png" />

