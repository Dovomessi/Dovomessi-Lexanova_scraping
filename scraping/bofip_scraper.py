import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

class BofipScraper:
    def __init__(self, base_url='https://bofip.impots.gouv.fr'):
        self.base_url = base_url

    async def scrape_bofip(self, search_terms):
        results = {
            'metadata': {'source': 'BOFiP', 'query': search_terms, 'scrape_date': datetime.now().isoformat()},
            'results': []
        }

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(self.base_url, timeout=60000)
                await page.fill("input[name='tx_bofip_pi1[search_text]']", search_terms)
                await page.click("button[type='submit']")
                await page.wait_for_selector("a.bofip-lien-texte", timeout=30000)
                links = await page.query_selector_all("a.bofip-lien-texte")

                for link in links[:5]:
                    title = await link.inner_text()
                    href = await link.get_attribute("href")
                    full_url = self.base_url + href
                    new_page = await browser.new_page()
                    await new_page.goto(full_url)
                    await new_page.wait_for_selector(".corpsTexte", timeout=30000)
                    content = await new_page.inner_text(".corpsTexte")
                    await new_page.close()
                    results['results'].append({'title': title.strip(), 'url': full_url, 'content': content.strip()})
                await browser.close()
        except Exception as e:
            results['error'] = str(e)

        return results
