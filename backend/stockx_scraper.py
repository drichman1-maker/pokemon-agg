import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth
import random

async def get_stockx_data(card_name, set_name, grade):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # User agents to rotate
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        
        context = await browser.new_context(user_agent=random.choice(user_agents))
        page = await context.new_page()
        await stealth(page)
        
        # Construct search query
        search_query = f"{card_name} {set_name} {grade}"
        search_url = f"https://stockx.com/search?s={search_query.replace(' ', '+')}"
        
        try:
            print(f"StockX Agent: Navigating to {search_url}")
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            
            # Find the first product link
            # StockX search results usually have product cards with links
            product_selector = 'a[data-testid="product-card-link"]'
            await page.wait_for_selector(product_selector, timeout=10000)
            
            product_link = await page.query_selector(product_selector)
            if not product_link:
                print("StockX Agent: No product found.")
                return None
                
            href = await product_link.get_attribute('href')
            product_url = f"https://stockx.com{href}"
            
            print(f"StockX Agent: Found product page: {product_url}")
            await page.goto(product_url, wait_until="networkidle", timeout=30000)
            
            # Extract data
            # Selectors might need adjustment as StockX changes frequently
            last_sale = 0.0
            lowest_ask = 0.0
            highest_bid = 0.0
            
            # Example selectors (subject to change)
            try:
                last_sale_text = await page.inner_text('.pdp-main-market-data__last-sale-value', timeout=5000)
                last_sale = float(last_sale_text.replace('$', '').replace(',', ''))
            except:
                pass
                
            try:
                lowest_ask_text = await page.inner_text('.pdp-main-market-data__lowest-ask-value', timeout=5000)
                lowest_ask = float(lowest_ask_text.replace('$', '').replace(',', ''))
            except:
                pass
                
            try:
                highest_bid_text = await page.inner_text('.pdp-main-market-data__highest-bid-value', timeout=5000)
                highest_bid = float(highest_bid_text.replace('$', '').replace(',', ''))
            except:
                pass
            
            return {
                "source": "StockX",
                "type": "Market Ticker",
                "lowest_ask": lowest_ask,
                "last_sale": last_sale,
                "highest_bid": highest_bid,
                "url": product_url
            }
            
        except Exception as e:
            print(f"StockX Agent Error: {str(e)}")
            return None
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test
    data = asyncio.run(get_stockx_data("Charizard", "Base Set", "PSA 10"))
    print(data)
