import Foundation

// MARK: - Data Models

struct SearchResult: Codable {
    let query: String
    let card: CardMetadata?
    let listings: [Listing]
    let totalResults: Int
    let marketStats: [String: GradeStats]?
    let comparisonData: ComparisonData?
    
    enum CodingKeys: String, CodingKey {
        case query
        case card
        case listings
        case totalResults = "total_results"
        case marketStats = "market_stats"
        case comparisonData = "comparison_data"
    }
}

struct GradeStats: Codable {
    let average: Double
    let count: Int
    let min: Double
    let max: Double
}

struct ComparisonData: Codable {
    let stockX: StockXData?
    let tcgPlayer: TCGPlayerData?
    let pwcc: PWCCData?
    
    enum CodingKeys: String, CodingKey {
        case stockX = "StockX"
        case tcgPlayer = "TCGPlayer"
        case pwcc = "PWCC"
    }
}

struct StockXData: Codable {
    let source: String
    let type: String
    let lowestAsk: Double
    let lastSale: Double
    let highestBid: Double
    let url: String
    
    enum CodingKeys: String, CodingKey {
        case source
        case type
        case lowestAsk = "lowest_ask"
        case lastSale = "last_sale"
        case highestBid = "highest_bid"
        case url
    }
}

struct TCGPlayerData: Codable {
    let source: String
    let rawMarketPrice: Double
    let listedMedian: Double?
    let link: String
    
    enum CodingKeys: String, CodingKey {
        case source
        case rawMarketPrice = "raw_market_price"
        case listedMedian = "listed_median"
        case link
    }
}

struct PWCCData: Codable {
    let source: String
    let marketPrice: Double
    let url: String
    
    enum CodingKeys: String, CodingKey {
        case source
        case marketPrice = "market_price"
        case url
    }
}

struct CardMetadata: Codable {
    let name: String
    let id: String
    let imageUrl: String?
    let setName: String
    let setSeries: String
    let number: String
    let rarity: String
    
    enum CodingKeys: String, CodingKey {
        case name
        case id
        case imageUrl = "image_url"
        case setName = "set_name"
        case setSeries = "set_series"
        case number
        case rarity
    }
}

struct Listing: Codable, Identifiable {
    let id = UUID()
    let title: String
    let price: Double
    let currency: String
    let url: String
    let company: String
    let grade: Double
    let imageUrl: String?
    let condition: String
    let location: String
    let isSteal: Bool
    let source: String?
    let arbitrageOpportunity: Bool?
    let dealScore: Int?
    
    enum CodingKeys: String, CodingKey {
        case title
        case price
        case currency
        case url
        case company
        case grade
        case imageUrl = "image_url"
        case condition
        case location
        case isSteal = "is_steal"
        case source
        case arbitrageOpportunity = "arbitrage_opportunity"
        case dealScore = "deal_score"
    }
}
