from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# Specify the path to chromedriver executable
chrome_driver_path = r"C:\Users\ansur\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Initialize WebDriver with the specified path
chrome_service = Service(chrome_driver_path)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Open the Amazon search results page
search_query = "laptops"
url = f"https://www.amazon.com/s?k={search_query}"
driver.get(url)

# Allow some time for the page to load
time.sleep(5)

# Lists to hold scraped data
product_names = []
product_prices = []
product_ratings = []

# Function to extract product information
def extract_product_info():
    # Find the product elements on the page
    products = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    for product in products:
        try:
            # Extract product name
            name = product.find_element(By.XPATH, ".//span[@class='a-size-medium a-color-base a-text-normal']").text
        except:
            name = "N/A"
        try:
            # Extract product price
            price_whole = product.find_element(By.XPATH, ".//span[@class='a-price-whole']").text
            price_fraction = product.find_element(By.XPATH, ".//span[@class='a-price-fraction']").text
            price = f"{price_whole}.{price_fraction}"
        except:
            price = "N/A"
        try:
            # Extract product rating
            rating = product.find_element(By.XPATH, ".//span[@class='a-icon-alt']").text
        except:
            rating = "N/A"

        # Append data to lists
        product_names.append(name)
        product_prices.append(price)
        product_ratings.append(rating)

# Extract product information from the first page
extract_product_info()

# Pagination: navigate to next pages and scrape data
try:
    while True:
        next_page = driver.find_element(By.XPATH, "//li[@class='a-last']/a")
        next_page.click()
        time.sleep(5)
        extract_product_info()
except:
    print("No more pages to load.")

# Close the browser
driver.quit()

# Create a DataFrame from the scraped data
data = {
    "Product Name": product_names,
    "Product Price": product_prices,
    "Product Rating": product_ratings
}
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv("amazon_products.csv", index=False)

print("Scraping completed and data saved to amazon_products.csv")
