import re  # ✅ Regex for price cleanup
import time

import pandas as pd
from openpyxl import load_workbook  # ✅ Added for Excel column auto-adjustment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scrape_flipkart():
    url = "https://www.flipkart.com/search?q=iphone+16"

    # Initialize Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Open browser for manual checks
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(5)  # Allow page to load

    data = []

    try:
        # ✅ Corrected product container XPath
        products = driver.find_elements(By.XPATH, "//*[@id='container']//div[contains(@class, 'KzDlHZ')]/../../..")

        if not products:
            print("⚠️ No iPhone products found. Check the XPath again!")

        for product in products:
            try:
                # ✅ Name and Price XPaths (Confirmed Correct)
                name_element = product.find_element(By.XPATH, ".//div[@class='KzDlHZ']")
                price_element = product.find_element(By.XPATH, ".//div[@class='Nx9bqj _4b5DiR']")

                name = name_element.text.strip()
                price = price_element.text.strip()

                # ✅ CHANGED: Fix encoding issue and clean the price
                price = price.encode("ascii", "ignore").decode()  # Removes non-ASCII characters
                price = re.sub(r"[^\d]", "", price)  # Keeps only digits

                print(f"✅ {name} | {price}")  # Debugging output
                data.append([name, price])

            except Exception as e:
                print(f"⚠️ Skipping an item due to error: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # ✅ CHANGED: Save data as CSV
    df = pd.DataFrame(data, columns=["Product Name", "Price"])
    csv_path = "data/iphone_prices.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # ✅ CHANGED: Save data as Excel (.xlsx) for auto-adjusting column width
    excel_path = "data/iphone_prices.xlsx"
    df.to_excel(excel_path, index=False, engine="openpyxl")

    # ✅ Auto-adjust column width in Excel
    wb = load_workbook(excel_path)
    ws = wb.active
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter  # Get column letter (A, B, etc.)
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2  # Add padding

    wb.save(excel_path)

    print(f"✅ Data saved to {csv_path} and auto-formatted {excel_path}")
    driver.quit()

# Run the scraper
# scrape_flipkart()
