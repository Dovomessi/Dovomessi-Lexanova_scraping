from flask import Flask, request, jsonify
from scraping.bofip_scraper import BofipScraper
from scraping.legifrance_scraper import LegifranceScraper
import asyncio

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Lexanova Scraping API est en ligne."

@app.route("/scrape")
def scrape():
    site = request.args.get("site")
    query = request.args.get("query")

    if not site or not query:
        return jsonify({"error": "Paramètres 'site' et 'query' requis."}), 400

    if site == "bofip":
        scraper = BofipScraper()
        results = asyncio.run(scraper.scrape_bofip(query))
        return jsonify(results)
    elif site == "legifrance":
        scraper = LegifranceScraper()
        results = asyncio.run(scraper.scrape_legifrance(query))
        return jsonify(results)
    else:
        return jsonify({"error": "Site non supporté. Utilisez 'bofip' ou 'legifrance'."}), 400

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)