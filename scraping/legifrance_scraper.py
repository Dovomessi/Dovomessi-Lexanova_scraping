import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

class LegifranceScraper:
    def __init__(self):
        self.base_url = "https://www.legifrance.gouv.fr/recherche"

    async def scrape_legifrance(self, search_terms):
        results = {
            'metadata': {'source': 'Légifrance', 'query': search_terms, 'scrape_date': datetime.now().isoformat()},
            'results': []
        }

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(
    headless=True,
    args=["--no-sandbox", "--disable-dev-shm-usage"]
)
                page = await browser.new_page()
                url = f"{self.base_url}?searchField=ALL&query={search_terms}"
                await page.goto(url, timeout=60000)
                await page.wait_for_selector("a.titreArt", timeout=30000)
                links = await page.query_selector_all("a.titreArt")

                for link in links[:5]:
                    title = await link.inner_text()
                    href = await link.get_attribute("href")
                    full_url = "https://www.legifrance.gouv.fr" + href
                    doc_page = await browser.new_page()
                    await doc_page.goto(full_url)
                    await doc_page.wait_for_selector("section.main-container", timeout=30000)
                    content = await doc_page.inner_text("section.main-container")
                    await doc_page.close()
                    results['results'].append({'title': title.strip(), 'url': full_url, 'content': content.strip()})
                await browser.close()
        except Exception as e:
            results['error'] = str(e)

        return results
