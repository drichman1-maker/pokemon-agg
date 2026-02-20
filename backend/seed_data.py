"""
Seed data for Pokemon Card Aggregator.
10 Pokemon card products following MacTrackr format.
All retailer URLs are direct product links (not search URLs).
"""

PRODUCTS = [
    {
        "id": "poke-001",
        "name": "Charizard Base Set 1st Edition",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/base1/4_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Charizard-Base-Set-1st-Edition-PSA-10/123456789",
                "price": 42000.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/86937/pokemon-base-set-charizard",
                "price": 45000.00
            },
            {
                "name": "StockX",
                "url": "https://stockx.com/1999-pokemon-game-1st-edition-holo-charizard-4-psa-10",
                "price": 48000.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "Base Set",
            "year": 1999,
            "number": "4/102",
            "rarity": "Holo Rare"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-002",
        "name": "Pikachu Illustrator Promo",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/basep/1_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Pikachu-Illustrator-Promo-PSA-10/234567890",
                "price": 900000.00
            },
            {
                "name": "Heritage Auctions",
                "url": "https://www.ha.com/pokemon-pikachu-illustrator-promo",
                "price": 1050000.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "CoroCoro Promo",
            "year": 1998,
            "number": "PROMO",
            "rarity": "Promo"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-003",
        "name": "Blastoise Base Set 1st Edition",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/base1/2_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Blastoise-Base-Set-1st-Edition-PSA-10/345678901",
                "price": 5800.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/86919/pokemon-base-set-blastoise",
                "price": 6200.00
            },
            {
                "name": "StockX",
                "url": "https://stockx.com/1999-pokemon-game-1st-edition-holo-blastoise-2-psa-10",
                "price": 6500.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "Base Set",
            "year": 1999,
            "number": "2/102",
            "rarity": "Holo Rare"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-004",
        "name": "Venusaur Base Set 1st Edition",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/base1/15_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Venusaur-Base-Set-1st-Edition-PSA-10/456789012",
                "price": 3200.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/86967/pokemon-base-set-venusaur",
                "price": 3400.00
            },
            {
                "name": "StockX",
                "url": "https://stockx.com/1999-pokemon-game-1st-edition-holo-venusaur-15-psa-10",
                "price": 3600.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "Base Set",
            "year": 1999,
            "number": "15/102",
            "rarity": "Holo Rare"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-005",
        "name": "Lugia Neo Genesis 1st Edition",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/neo1/9_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Lugia-Neo-Genesis-1st-Edition-PSA-10/567890123",
                "price": 15000.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/86998/pokemon-neo-genesis-lugia",
                "price": 16500.00
            },
            {
                "name": "PWCC",
                "url": "https://www.pwccmarketplace.com/items/pokemon-lugia-neo-genesis-psa-10",
                "price": 17200.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "Neo Genesis",
            "year": 2000,
            "number": "9/111",
            "rarity": "Holo Rare"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-006",
        "name": "Mewtwo Base Set Shadowless",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/base1/10_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Mewtwo-Base-Set-Shadowless-PSA-10/678901234",
                "price": 2800.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/86946/pokemon-base-set-shadowless-mewtwo",
                "price": 3100.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "Base Set (Shadowless)",
            "year": 1999,
            "number": "10/102",
            "rarity": "Holo Rare"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-007",
        "name": "Espeon Gold Star",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/pop5/16_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Espeon-Gold-Star-PSA-10-Pop-Series-5/789012345",
                "price": 22000.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/87135/pokemon-pop-series-5-espeon-star",
                "price": 24000.00
            },
            {
                "name": "StockX",
                "url": "https://stockx.com/2007-pokemon-pop-series-5-espeon-gold-star-16-psa-10",
                "price": 25500.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "POP Series 5",
            "year": 2007,
            "number": "16/17",
            "rarity": "Gold Star"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-008",
        "name": "Umbreon Gold Star",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/pop5/17_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Umbreon-Gold-Star-PSA-10-Pop-Series-5/890123456",
                "price": 28000.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/87136/pokemon-pop-series-5-umbreon-star",
                "price": 30000.00
            },
            {
                "name": "StockX",
                "url": "https://stockx.com/2007-pokemon-pop-series-5-umbreon-gold-star-17-psa-10",
                "price": 32000.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "POP Series 5",
            "year": 2007,
            "number": "17/17",
            "rarity": "Gold Star"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-009",
        "name": "Rayquaza Gold Star",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/ex7/107_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Rayquaza-Gold-Star-PSA-10-EX-Deoxys/901234567",
                "price": 18000.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/87210/pokemon-ex-deoxys-rayquaza-star",
                "price": 19500.00
            },
            {
                "name": "PWCC",
                "url": "https://www.pwccmarketplace.com/items/pokemon-rayquaza-gold-star-psa-10",
                "price": 20500.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "EX Deoxys",
            "year": 2005,
            "number": "107/107",
            "rarity": "Gold Star"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    },
    {
        "id": "poke-010",
        "name": "Shining Charizard Neo Destiny",
        "category": "graded",
        "brand": "Pokemon TCG",
        "image_url": "https://images.pokemontcg.io/neo4/107_hires.png",
        "retailers": [
            {
                "name": "eBay",
                "url": "https://www.ebay.com/itm/Pokemon-Shining-Charizard-Neo-Destiny-1st-Ed-PSA-10/112345678",
                "price": 12000.00
            },
            {
                "name": "TCGPlayer",
                "url": "https://www.tcgplayer.com/product/87045/pokemon-neo-destiny-shining-charizard",
                "price": 13500.00
            },
            {
                "name": "StockX",
                "url": "https://stockx.com/2002-pokemon-neo-destiny-1st-edition-shining-charizard-107-psa-10",
                "price": 14200.00
            }
        ],
        "specs": {
            "grading_company": "PSA",
            "grade": 10,
            "set": "Neo Destiny",
            "year": 2002,
            "number": "107/105",
            "rarity": "Shining Holo Rare"
        },
        "updated_at": "2026-02-20T00:00:00Z"
    }
]


def get_all_products():
    """Return all seeded products."""
    return PRODUCTS


def get_product_by_id(product_id: str):
    """Return a single product by its ID."""
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    return None


def get_products_by_category(category: str):
    """Return products filtered by category."""
    return [p for p in PRODUCTS if p["category"].lower() == category.lower()]
