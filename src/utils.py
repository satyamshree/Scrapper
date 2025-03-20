import re
import pandas as pd

def clean_price(price_text):
    """
    Cleans price text by removing non-numeric characters.
    Example: 'â‚¹79,999' → '79,999'
    """
    return re.sub(r"[^\d,]", "", price_text)

def adjust_excel_column_width(writer, df, sheet_name="Sheet1"):
    """
    Adjusts column width in the Excel sheet for better readability.
    """
    worksheet = writer.sheets[sheet_name]
    for col_num, value in enumerate(df.columns.values):
        worksheet.set_column(col_num, col_num, max(df[value].astype(str).map(len).max(), len(value)))

def save_data(df, csv_path="data/iphone_prices.csv", excel_path="data/iphone_prices.xlsx"):
    """
    Saves the DataFrame as CSV and Excel files.
    """
    # Save as CSV
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # Save as Excel with column width adjustment
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="iPhone Prices", index=False)
        adjust_excel_column_width(writer, df, "iPhone Prices")

    print(f"Data saved successfully: {csv_path} & {excel_path}")

print("Utils loaded successfully!")
