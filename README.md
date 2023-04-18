# morisimmo
Repository for morisimmo

# Real Estate Data Pipeline for Mauritius

This project aims to create a data pipeline for real estate properties in Mauritius using BeautifulSoup and Pandas. The code scrapes property data from the L'Express Property website and creates a Pandas DataFrame to store and process the information. Additionally, it uses Streamlit Maps and Plotly to visualize the data.

# Dependencies

To run this project, you need to install the following Python libraries:
1.  requests
2.  BeautifulSoup4
3.  Pandas
4.  Numpy
5.  Streamlit
6.  Plotly

You can install these libraries using pip:
1.  pip install requests beautifulsoup4 pandas numpy streamlit plotly

# How to Run

Save the code in a Python file, e.g., mauritius_real_estate.py.

Ensure that you have the mu_city_coordinates.csv file containing the coordinates for cities in Mauritius. Place the CSV file in the same directory as your Python file.

Run the Streamlit app using the following command:
streamlit run mauritius_real_estate.py

This will launch a local web server, and you can access the app in your web browser.

# Code Overview

The code performs the following tasks:

1.  Imports the required libraries and initializes global variables to store property data.
2.  Defines a range of pages to scrape from the L'Express Property website.
3.  Loads a CSV file containing the coordinates of cities in Mauritius.
4.  Scrapes property data from the website, such as title, location, price, and features.
5.  Processes the scraped data and creates a Pandas DataFrame called realestate_db.
6.  Merges the property data with the coordinates data to obtain the corresponding coordinates for each city in realestate_db.
7.  Creates interactive visualizations using Streamlit Maps and Plotly, such as a map showing property locations, bar charts, and box plots.

With this pipeline, you can analyze and visualize real estate properties in Mauritius, allowing you to gain insights into the property market and make informed decisions.



