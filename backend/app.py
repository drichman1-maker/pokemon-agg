from flask import Flask, request, jsonify
from flask_cors import CORS
from pokemontcgsdk import Card
from pokemontcgsdk import RestClient
from ebaysdk.finding import Connection as Finding
import re
import os
import asyncio
from typing import List, Dict, Optional, Tuple

# Import the new agents
from stockx_scraper import get_stockx_data
from tcgplayer_analyst import get_tcgplayer_data
from pwcc_agent import get_pwcc_data

app = Flask(__name__)
CORS(app)

# Configure API keys
POKEMONTCG_API_KEY = os.environ.get('POKEMONTCG_API_KEY', '')
EBAY_APP_ID = os.environ.get('EBAY_APP_ID', 'YOUR_EBAY_APP_ID')
EBAY_DEV_ID = os.environ.get('EBAY_DEV_ID', 'YOUR_EBAY_DEV_ID')
EBAY_CERT_ID = os.environ.get('EBAY_CERT_ID', 'YOUR_EBAY_CERT_ID')

if POKEMONTCG_API_KEY:
    RestClient.configure(POKEMONTCG_API_KEY)


class GradeParser:
    GRADING_PATTERNS = {
        'PSA': r'PSA\s*(\d+(?:\.\d+)?)',
        'BGS': r'BGS\s*(\d+(?:\.\d+)?)',
        'CGC': r'CGC\s*(\d+(?:\.\d+)?)',
        'SGC': r'SGC\s*(\d+(?:\.\d+)?)',
        'TAG': r'TAG\s*(\d+(?:\.\d+)?)',
        'ACE': r'ACE\s*(\d+(?:\.\d+)?)',
        'PCA': r'PCA\s*(\d+(?:\.\d+)?)',
    }
    
    @staticmethod
    def parse_grade(title: str) -> Tuple[Optional[str], Optional[float]]:
        title_upper = title.upper()
        for company, pattern in GradeParser.GRADING_PATTERNS.items():
            match = re.search(pattern, title_upper)
            if match:
                try:
                    grade = float(match.group(1))
                    if 1 <= grade <= 10:
                        return company, grade
                except ValueError:
                    continue
        return None, None


async def fetch_card_metadata_async(query: str) -> Optional[Dict]:
    # Running in a thread since pokemontcgsdk is synchronous
    return await asyncio.to_thread(_fetch_card_metadata, query)

def _fetch_card_metadata(query: str) -> Optional[Dict]:
    try:
        cards = Card.where(q=f'name:{query}')
        if cards:
            card = cards[0]
            return {
                'name': card.name,
                'id': card.id,
                'image_url': card.images.large if hasattr(card, 'images') else None,
                'set_name': card.set.name if hasattr(card, 'set') else 'Unknown Set',
                'set_series': card.set.series if hasattr(card, 'set') else 'Unknown Series',
                'number': card.number if hasattr(card, 'number') else '',
                'rarity': card.rarity if hasattr(card, 'rarity') else 'Unknown',
                'release_date': card.set.releaseDate if hasattr(card, 'set') and hasattr(card.set, 'releaseDate') else None,
            }
    except Exception as e:
        print(f"Error fetching card metadata: {str(e)}")
    return None


async def fetch_ebay_listings_async(query: str) -> List[Dict]:
    return await asyncio.to_thread(_fetch_ebay_listings, query)

def _fetch_ebay_listings(query: str) -> List[Dict]:
    try:
        api = Finding(
            appid=EBAY_APP_ID,
            devid=EBAY_DEV_ID,
            certid=EBAY_CERT_ID,
            config_file=None,
            siteid='EBAY-US'
        )
        search_query = f"{query} graded pokemon card"
        response = api.execute('findItemsAdvanced', {
            'keywords': search_query,
            'itemFilter': [
                {'name': 'ListingType', 'value': 'FixedPrice'},
                {'name': 'Condition', 'value': 'New'},
            ],
            'sortOrder': 'PricePlusShippingLowest',
            'paginationInput': {'entriesPerPage': 50, 'pageNumber': 1}
        })
        
        listings = []
        if response.reply.ack == 'Success':
            search_result = response.reply.searchResult
            if hasattr(search_result, 'item'):
                for item in search_result.item:
                    title = item.title
                    company, grade = GradeParser.parse_grade(title)
                    if company and grade:
                        try:
                            price = float(item.sellingStatus.currentPrice.value)
                            listings.append({
                                'title': title,
                                'price': price,
                                'currency': item.sellingStatus.currentPrice._currencyId,
                                'url': item.viewItemURL,
                                'company': company,
                                'grade': grade,
                                'image_url': item.galleryURL if hasattr(item, 'galleryURL') else None,
                                'condition': item.condition.conditionDisplayName if hasattr(item, 'condition') else 'N/A',
                                'location': item.location if hasattr(item, 'location') else 'N/A',
                                'source': 'eBay'
                            })
                        except Exception:
                            continue
        return listings
    except Exception as e:
        print(f"Error fetching eBay listings: {repr(e)}")
        return []


def normalize_and_calculate_arbitrage(listings, stockx_results, tcg_results, pwcc_results):
    """The Brain: Match apples-to-apples and find arbitrage opportunities."""
    
    # 1. Calculate Standard Market Stats (eBay-based)
    grade_prices = {}
    for l in listings:
        key = str(l['grade'])
        if key not in grade_prices: grade_prices[key] = []
        grade_prices[key].append(l['price'])
        
    market_stats = {}
    for gk, p in grade_prices.items():
        market_stats[gk] = {'average': sum(p)/len(p), 'count': len(p), 'min': min(p), 'max': max(p)}

    # 2. Enrich with StockX and TCGPlayer data & Check Arbitrage
    # Target common grades for comparison
    comparison_data = {
        'StockX': stockx_results,
        'TCGPlayer': tcg_results,
        'PWCC': pwcc_results
    }

    for listing in listings:
        listing['arbitrage_opportunity'] = False
        listing['deal_score'] = 50 # Base score
        
        # Match with StockX (if grade matches)
        # Assuming stockx_results is a dict of grade -> data or a single call result
        # For this implementation, we assume stockx_results is the best match for the searched card/grade
        if stockx_results and stockx_results.get('lowest_ask'):
            # Only compare if it's the right grade (StockX specialist was targeted)
            # Logic: If eBay Price < StockX Lowest Ask * 0.85, flag as arbitrage
            if listing['price'] < stockx_results['lowest_ask'] * 0.85:
                listing['arbitrage_opportunity'] = True
                listing['deal_score'] = 90
            
        # Deal Score adjustments
        grade_key = str(listing['grade'])
        avg_price = market_stats.get(grade_key, {}).get('average', 0)
        if avg_price > 0:
            if listing['price'] < avg_price * 0.80:
                listing['is_steal'] = True
                listing['deal_score'] += 20
            else:
                listing['is_steal'] = False

    return listings, market_stats, comparison_data


@app.route('/search', methods=['GET'])
async def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    # Run heavy operations in parallel
    # 1. Fetch metadata and eBay listings first to get details for specialized agents
    metadata, ebay_listings = await asyncio.gather(
        fetch_card_metadata_async(query),
        fetch_ebay_listings_async(query)
    )
    
    if not metadata:
        return jsonify({'error': 'No card metadata found for this query'}), 404

    # 2. Prepare specialized agent tasks based on metadata
    stockx_task = get_stockx_data(metadata['name'], metadata['set_name'], "PSA 10")
    tcg_task = get_tcgplayer_data(metadata['name'], metadata['set_name'])
    pwcc_task = get_pwcc_data(metadata['name'], metadata['set_name'])
    
    # Run Source Agents in parallel
    results = await asyncio.gather(stockx_task, tcg_task, pwcc_task)
    stockx_data, tcg_data, pwcc_data = results
    
    # 3. Normalize and calculate Arbitrage
    final_listings, market_stats, compare_sources = normalize_and_calculate_arbitrage(
        ebay_listings, stockx_data, tcg_data, pwcc_data
    )
    
    # 4. Sort by Deal Score (High to Low)
    final_listings = sorted(final_listings, key=lambda x: (-x.get('deal_score', 0), x['price']))
    
    response = {
        'query': query,
        'card': metadata,
        'listings': final_listings,
        'market_stats': market_stats,
        'comparison_data': compare_sources,
        'total_results': len(final_listings)
    }
    
    return jsonify(response)




@app.route('/featured', methods=['GET'])
def featured():
    """Return featured/popular cards for homepage display"""
    featured_cards = [
        {"name": "Charizard", "set": "Base Set", "image": "https://images.pokemontcg.io/base1/4_hires.png"},
        {"name": "Pikachu", "set": "Base Set", "image": "https://images.pokemontcg.io/base1/58_hires.png"},
        {"name": "Mewtwo", "set": "Base Set", "image": "https://images.pokemontcg.io/base1/10_hires.png"},
        {"name": "Blastoise", "set": "Base Set", "image": "https://images.pokemontcg.io/base1/2_hires.png"},
        {"name": "Venusaur", "set": "Base Set", "image": "https://images.pokemontcg.io/base1/15_hires.png"},
        {"name": "Gyarados", "set": "Base Set", "image": "https://images.pokemontcg.io/base1/6_hires.png"},
    ]
    return jsonify({"featured": featured_cards})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'PokeAggregator Multi-Source API'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
