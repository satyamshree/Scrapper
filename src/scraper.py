import re  # ✅ Regex for price cleanup
import time
import pandas as pd
from openpyxl import load_workbook  # ✅ Added for Excel column auto-adjustment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def scrape_data(url, container_xpath, name_xpath, price_xpath):
    """
    Scrapes product data from a website using user-provided XPaths.
    Saves the data as CSV and Excel files.

    :param url: The target webpage URL
    :param container_xpath: XPath for locating the product containers
    :param name_xpath: XPath for extracting product names (relative to container)
    :param price_xpath: XPath for extracting product prices (relative to container)
    :return: Paths to the saved CSV and Excel files
    """

    # ✅ Initialize Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run browser in the background (optional)
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(5)  # Allow time for page load

    data = []  # ✅ List to store scraped data

    try:
        # ✅ Find product containers using container XPath
        products = driver.find_elements(By.XPATH, container_xpath)

        if not products:
            print("⚠️ No products found. Check the XPath and website structure.")

        for product in products:
            try:
                # ✅ Extract product name (relative to container)
                name_element = product.find_element(By.XPATH, name_xpath)
                name = name_element.text.strip()

                # ✅ Extract product price (relative to container)
                price_element = product.find_element(By.XPATH, price_xpath)
                price = price_element.text.strip()
                price = re.sub(r"[^\d]", "", price)  # ✅ Clean price (keep only digits)

                print(f"✅ {name} | {price}")  # Debug output
                data.append([name, price])

            except Exception as e:
                print(f"⚠️ Skipping an item due to error: {e}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # ✅ Save data as CSV
    df = pd.DataFrame(data, columns=["Product Name", "Price"])
    csv_path = "data/scraped_data.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8")

    # ✅ Save data as Excel
    excel_path = "data/scraped_data.xlsx"
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
        ws.column_dimensions[col_letter].width = max_length + 2  # ✅ Add padding

    wb.save(excel_path)

    print(f"✅ Data saved to {csv_path} and auto-formatted {excel_path}")
    driver.quit()

    return csv_path, excel_path  # ✅ Return file paths for frontend download
