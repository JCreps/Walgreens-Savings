from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()  # or 

url = 'https://www.walgreens.com/offers/offers.jsp?ban=dl_dlsp_MegaMenu_Coupons'
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Use CSS selector to find all elements with an id that ends with '-coupon-availablecoupons'
coupons = soup.select('[id$="-coupon-availablecoupons"]')

for coupon in coupons:
    try:
        # Extract the number from the id attribute
        coupon_number = coupon['id'].split('-')[0]

        # Find the card__item element within each coupon
        card_item = coupon.find('div', class_='card__item')

        # Extract the expiration date, savings amount, and product name
        expiration_date = card_item.find('div', class_='font__fourteen text-color__blue').text
        savings = card_item.find('div', class_='wag-txt-elipsis font__eighteen text-color__red').text
        product_name = card_item.find('strong', class_='font__eighteen text-color__blue').text

        print(f'Coupon Number: {coupon_number}, Expiration Date: {expiration_date}, Savings: {savings}, Product Name: {product_name}')
    except AttributeError:
        print(f'Error processing coupon number {coupon_number}, skipping to next coupon.')
        continue
