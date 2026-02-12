import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth
import random

async def get_tcgplayer_data(card_name, set_name):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        ]
        
        context = await browser.new_context(user_agent=random.choice(user_agents))
        page = await context.new_page()
        await stealth(page)
        
        # Construct search query
        search_query = f"{card_name} {set_name}"
        search_url = f"https://www.tcgplayer.com/search/all/product?q={search_query.replace(' ', '+')}"
        
        try:
            print(f"TCGPlayer Agent: Navigating to {search_url}")
            await page.goto(search_url, wait_until="networkidle", timeout=30000)
            
            # Find the first product link
            product_selector = '.search-result__title a'
            await page.wait_for_selector(product_selector, timeout=10000)
            
            product_link = await page.query_selector(product_selector)
            if not product_link:
                print("TCGPlayer Agent: No product found.")
                return None
                
            href = await product_link.get_attribute('href')
            product_url = f"https://www.tcgplayer.com{href}"
            
            print(f"TCGPlayer Agent: Found product page: {product_url}")
            await page.goto(product_url, wait_until="networkidle", timeout=30000)
            
            # Extract data
            market_price = 0.0
            listed_median = 0.0
            
            # TCGPlayer often has price labels
            try:
                # Market Price
                market_price_text = await page.inner_text('.price-guide__table tr:has-text("Market Price") .price', timeout=5000)
                market_price = float(market_price_text.replace('$', '').replace(',', ''))
            except:
                pass
                
            try:
                # Listed Median
                median_price_text = await page.inner_text('.price-guide__table tr:has-text("Listed Median") .price', timeout=5000)
                listed_median = float(median_price_text.replace('$', '').replace(',', ''))
            except:
                pass
            
            return {
                "source": "TCGPlayer",
                "raw_market_price": market_price,
                "listed_median": listed_median,
                "link": product_url
            }
            
        except Exception as e:
            print(f"TCGPlayer Agent Error: {str(e)}")
            return None
        finally:
            await browser.close()

if __name__ == "__main__":
    # Test
    data = asyncio.run(get_tcgplayer_data("Charizard", "Base Set"))
    print(data)
