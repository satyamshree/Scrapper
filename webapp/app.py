import os
import sys

from flask import Flask, request, send_file, render_template
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.scraper import scrape_data  # Ensure correct import

app = Flask(__name__)

# ✅ Update the path to match your project structure
DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        name_xpath = request.form["name_xpath"]
        price_xpath = request.form["price_xpath"]
        container_xpath = request.form["container_xpath"]

        # ✅ Run scraper and get file paths
        csv_path, excel_path = scrape_data(url, container_xpath, name_xpath, price_xpath)

        # ✅ Ensure the correct absolute path
        excel_path = os.path.join(DATA_FOLDER, os.path.basename(excel_path))

        if os.path.exists(excel_path):
            return send_file(
                excel_path,
                as_attachment=True,
                download_name="scraped_data.xlsx",
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            return "File not found", 404

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
