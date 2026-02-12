import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth
import random

async def get_pwcc_data(card_name, set_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        
        context = await browser.new_context(user_agent=random.choice(user_agents))
        page = await context.new_page()
        await stealth(page)
        
        # PWCC Marketplace search
        search_query = f"{card_name} {set_name}"
        search_url = f"https://www.pwccmarketplace.com/market-price-research?q={search_query.replace(' ', '+')}"
        
        try:
            print(f"PWCC Agent: Navigating to {search_url}")
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            
            # PWCC often displays results in a grid. We want the market data.
            # This is a simplified extraction of the first result's sale price
            # Selectors for PWCC research are often complex
            sale_price = 0.0
            
            try:
                # Example selector for a price in the results
                price_elements = await page.query_selector_all('.price')
                if price_elements:
                    price_text = await price_elements[0].inner_text()
                    sale_price = float(price_text.replace('$', '').replace(',', ''))
            except:
                pass
            
            return {
                "source": "PWCC",
                "market_price": sale_price,
                "url": search_url
            }
            
        except Exception as e:
            print(f"PWCC Agent Error: {str(e)}")
            return None
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test
    data = asyncio.run(get_pwcc_data("Charizard", "Base Set"))
    print(data)
