import SwiftUI

struct ContentView: View {
    @StateObject private var networkManager = NetworkManager.shared
    @State private var searchQuery = ""
    @State private var searchResults: SearchResult?
    @State private var isSearching = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 0) {
                // Search Bar
                HStack {
                    Image(systemName: "magnifyingglass")
                        .foregroundColor(.gray)
                    
                    TextField("Search for a Pokémon card...", text: $searchQuery)
                        .textFieldStyle(PlainTextFieldStyle())
                        .onSubmit {
                            performSearch()
                        }
                    
                    if !searchQuery.isEmpty {
                        Button(action: {
                            searchQuery = ""
                            searchResults = nil
                        }) {
                            Image(systemName: "xmark.circle.fill")
                                .foregroundColor(.gray)
                        }
                    }
                }
                .padding()
                .background(Color(.systemGray6))
                .cornerRadius(10)
                .padding()
                
                // Content
                if isSearching {
                    Spacer()
                    ProgressView("Searching...")
                        .progressViewStyle(CircularProgressViewStyle())
                    Spacer()
                } else if let error = networkManager.errorMessage {
                    Spacer()
                    VStack(spacing: 16) {
                        Image(systemName: "exclamationmark.triangle")
                            .font(.system(size: 50))
                            .foregroundColor(.orange)
                        
                        Text("Error")
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text(error)
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                            .padding(.horizontal)
                        
                        Button("Try Again") {
                            performSearch()
                        }
                        .buttonStyle(.borderedProminent)
                    }
                    Spacer()
                } else if let results = searchResults {
                    SearchResultsView(results: results)
                } else {
                    Spacer()
                    VStack(spacing: 16) {
                        Image(systemName: "magnifyingglass")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        
                        Text("Search for Graded Pokémon Cards")
                            .font(.title2)
                            .fontWeight(.bold)
                        
                        Text("Enter a Pokémon name above to find graded cards on eBay")
                            .multilineTextAlignment(.center)
                            .foregroundColor(.secondary)
                            .padding(.horizontal)
                    }
                    Spacer()
                }
            }
            .navigationTitle("Pokémon Cards")
            .navigationBarTitleDisplayMode(.large)
        }
    }
    
    private func performSearch() {
        guard !searchQuery.isEmpty else { return }
        
        isSearching = true
        
        Task {
            do {
                let results = try await networkManager.search(query: searchQuery)
                searchResults = results
            } catch {
                // Error is already set in networkManager
                print("Search error: \(error)")
            }
            isSearching = false
        }
    }
}

// MARK: - Search Results View

struct SearchResultsView: View {
    let results: SearchResult
    @State private var selectedCompany = "ALL"
    @State private var minGrade = 0.0
    
    var filteredListings: [Listing] {
        var listings = results.listings
        
        if selectedCompany != "ALL" {
            listings = listings.filter { $0.company == selectedCompany }
        }
        
        if minGrade > 0 {
            listings = listings.filter { $0.grade >= minGrade }
        }
        
        return listings
    }
    
    var body: some View {
        List {
            // Card Metadata Section
            if let card = results.card {
                Section {
                    CardMetadataView(card: card)
                } header: {
                    Text("Card Details")
                }
            }
            
            // Market Pulse
            if let stats = results.marketStats, !stats.isEmpty {
                Section {
                    MarketPulseView(stats: stats)
                } header: {
                    Text("Market Stats")
                }
            }
            
            // Source Comparison
            if let comparisonData = results.comparisonData {
                Section {
                    SourceComparisonView(comparisonData: comparisonData)
                } header: {
                    Text("Multi-Source Comparison")
                }
            }

            // Filters Section
            Section {
                 VStack(alignment: .leading, spacing: 12) {
                     // Company Filter
                     ScrollView(.horizontal, showsIndicators: false) {
                         HStack {
                             ForEach(["ALL", "PSA", "BGS", "CGC", "SGC"], id: \.self) { company in
                                 FilterChip(title: company, isSelected: selectedCompany == company) {
                                     selectedCompany = company
                                 }
                             }
                         }
                     }
                     
                     // Grade Filter
                     ScrollView(.horizontal, showsIndicators: false) {
                         HStack {
                             Text("Min Grade:")
                                 .font(.caption)
                                 .fontWeight(.semibold)
                                 .foregroundColor(.secondary)
                             
                             ForEach([0, 10, 9, 8, 7], id: \.self) { grade in
                                 FilterChip(title: grade == 0 ? "Any" : "\(grade)+", isSelected: Int(minGrade) == grade) {
                                     minGrade = Double(grade)
                                 }
                             }
                         }
                     }
                 }
                 .padding(.vertical, 8)
                 .listRowInsets(EdgeInsets())
                 .padding(.horizontal)
            } header: {
                Text("Filters")
            }
            
            // Listings Section
            Section {
                if filteredListings.isEmpty {
                    Text("No listing found for this filter")
                        .foregroundColor(.secondary)
                        .italic()
                } else {
                    ForEach(filteredListings) { listing in
                        NavigationLink(destination: ListingDetailView(listing: listing)) {
                            ListingRowView(listing: listing)
                        }
                    }
                }
            } header: {
                Text("Active Listings (\(filteredListings.count))")
            }
        }
        .listStyle(InsetGroupedListStyle())
    }
}

struct FilterChip: View {
    let title: String
    let isSelected: Bool
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            Text(title)
                .font(.system(size: 14, weight: .semibold))
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(isSelected ? Color.blue : Color(.systemGray5))
                .foregroundColor(isSelected ? .white : .primary)
                .cornerRadius(16)
        }
        .buttonStyle(PlainButtonStyle())
    }
}

// MARK: - Card Metadata View

struct CardMetadataView: View {
    let card: CardMetadata
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            if let imageUrl = card.imageUrl, let url = URL(string: imageUrl) {
                AsyncImage(url: url) { phase in
                    switch phase {
                    case .empty:
                        ProgressView()
                            .frame(maxWidth: .infinity)
                            .frame(height: 300)
                    case .success(let image):
                        image
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(maxWidth: .infinity)
                            .cornerRadius(12)
                    case .failure:
                        Image(systemName: "photo")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                            .frame(maxWidth: .infinity)
                            .frame(height: 300)
                    @unknown default:
                        EmptyView()
                    }
                }
            }
            
            VStack(alignment: .leading, spacing: 8) {
                Text(card.name)
                    .font(.title2)
                    .fontWeight(.bold)
                
                InfoRow(label: "Set", value: card.setName)
                InfoRow(label: "Series", value: card.setSeries)
                InfoRow(label: "Number", value: card.number)
                InfoRow(label: "Rarity", value: card.rarity)
            }
        }
        .padding(.vertical, 8)
    }
}

// MARK: - Listing Row View

struct ListingRowView: View {
    let listing: Listing
    
    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            // Grade Badge
            VStack(spacing: 4) {
                Text(String(format: "%.1f", listing.grade))
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(gradeColor(for: listing.grade))
                
                Text(listing.company)
                    .font(.caption)
                    .fontWeight(.semibold)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(companyColor(for: listing.company).opacity(0.2))
                    .foregroundColor(companyColor(for: listing.company))
                    .cornerRadius(8)
            }
            .frame(width: 60)
            
            // Listing Info
            VStack(alignment: .leading, spacing: 4) {
                Text(listing.title)
                    .font(.subheadline)
                    .lineLimit(2)
                
                HStack {
                    Text(String(format: "$%.2f", listing.price))
                        .font(.headline)
                        .foregroundColor(.primary)
                    
                    if listing.arbitrageOpportunity == true {
                        Text("⚡ ARBITRAGE")
                            .font(.caption)
                            .fontWeight(.bold)
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color.indigo)
                            .foregroundColor(.white)
                            .cornerRadius(4)
                    }
                    
                    if listing.isSteal {
                        Text("🔥 STEAL")
                            .font(.caption)
                            .fontWeight(.bold)
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(Color.green)
                            .foregroundColor(.white)
                            .cornerRadius(4)
                    }
                }
                
                Text(listing.location)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
    
    private func gradeColor(for grade: Double) -> Color {
        switch grade {
        case 10:
            return .yellow // Gold
        case 9..<10:
            return .gray // Silver
        case 8..<9:
            return .orange // Bronze
        default:
            return .secondary
        }
    }
    
    private func companyColor(for company: String) -> Color {
        switch company {
        case "PSA":
            return .blue
        case "BGS":
            return .green
        case "CGC":
            return .purple
        case "SGC":
            return .black
        default:
            return .gray
        }
    }
}

// MARK: - Listing Detail View

struct ListingDetailView: View {
    let listing: Listing
    
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Grade Display
                HStack {
                    Spacer()
                    VStack(spacing: 8) {
                        Text(String(format: "%.1f", listing.grade))
                            .font(.system(size: 60, weight: .bold))
                            .foregroundColor(gradeColor(for: listing.grade))
                        
                        Text(listing.company)
                            .font(.title3)
                            .fontWeight(.semibold)
                            .padding(.horizontal, 16)
                            .padding(.vertical, 8)
                            .background(companyColor(for: listing.company).opacity(0.2))
                            .foregroundColor(companyColor(for: listing.company))
                            .cornerRadius(12)
                    }
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(gradeColor(for: listing.grade), lineWidth: 3)
                    )
                    Spacer()
                }
                
                // Price
                VStack(alignment: .leading, spacing: 8) {
                    Text("Price")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    HStack {
                        Text(String(format: "$%.2f", listing.price))
                            .font(.system(size: 32, weight: .bold))
                        
                        if listing.isSteal {
                            Text("🔥 STEAL ALERT")
                                .font(.caption)
                                .fontWeight(.bold)
                                .padding(.horizontal, 8)
                                .padding(.vertical, 4)
                                .background(Color.green)
                                .foregroundColor(.white)
                                .cornerRadius(8)
                        }
                    }
                }
                .padding()
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(Color(.systemGray6))
                .cornerRadius(12)
                
                // Title
                VStack(alignment: .leading, spacing: 8) {
                    Text("Listing Title")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    Text(listing.title)
                        .font(.body)
                }
                
                // Details
                VStack(alignment: .leading, spacing: 12) {
                    Text("Details")
                        .font(.headline)
                        .foregroundColor(.secondary)
                    
                    InfoRow(label: "Condition", value: listing.condition)
                    InfoRow(label: "Location", value: listing.location)
                    InfoRow(label: "Currency", value: listing.currency)
                }
                
                // View on eBay Button
                Link(destination: URL(string: listing.url)!) {
                    HStack {
                        Spacer()
                        Text("View on eBay")
                            .font(.headline)
                            .foregroundColor(.white)
                        Image(systemName: "arrow.up.right")
                            .foregroundColor(.white)
                        Spacer()
                    }
                    .padding()
                    .background(Color.blue)
                    .cornerRadius(12)
                }
                .padding(.top)
            }
            .padding()
        }
        .navigationTitle("Listing Details")
        .navigationBarTitleDisplayMode(.inline)
    }
    
    private func gradeColor(for grade: Double) -> Color {
        switch grade {
        case 10:
            return .yellow
        case 9..<10:
            return .gray
        case 8..<9:
            return .orange
        default:
            return .secondary
        }
    }
    
    private func companyColor(for company: String) -> Color {
        switch company {
        case "PSA":
            return .blue
        case "BGS":
            return .green
        case "CGC":
            return .purple
        case "SGC":
            return .black
        default:
            return .gray
        }
    }
}

// MARK: - Helper Views

struct InfoRow: View {
    let label: String
    let value: String
    
    var body: some View {
        HStack {
            Text(label)
                .fontWeight(.semibold)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
        }
    }
}

// MARK: - Preview

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

struct MarketPulseView: View {
    let stats: [String: GradeStats]
    
    var sortedGrades: [String] {
        stats.keys.sorted { Double($0) ?? 0 > Double($1) ?? 0 }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("📊 Market Pulse")
                    .font(.headline)
                Spacer()
                Text("Source: eBay")
                    .font(.caption2)
                    .fontWeight(.semibold)
                    .foregroundColor(.secondary)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 2)
                    .background(Color(.systemGray5))
                    .cornerRadius(4)
            }
            .padding(.bottom, 4)
            
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 12) {
                    ForEach(sortedGrades.prefix(7), id: \.self) { grade in
                        if let stat = stats[grade] {
                            VStack(alignment: .leading, spacing: 4) {
                                HStack {
                                    Text(grade)
                                        .font(.title3)
                                        .fontWeight(.bold)
                                        .foregroundColor(gradeColor(for: Double(grade) ?? 0))
                                    
                                    Text("\(stat.count) sold")
                                        .font(.caption)
                                        .foregroundColor(.secondary)
                                        .padding(.horizontal, 6)
                                        .padding(.vertical, 2)
                                        .background(Color.white)
                                        .cornerRadius(4)
                                }
                                
                                Text(String(format: "$%.2f", stat.average))
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                
                                Text("Low: $\(Int(stat.min))")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            .padding(12)
                            .background(Color(.systemGray6))
                            .cornerRadius(12)
                            .frame(minWidth: 140)
                        }
                    }
                }
            }
        }
        .padding(.vertical, 8)
    }
    
    private func gradeColor(for grade: Double) -> Color {
        switch grade {
        case 10: return .yellow
        case 9..<10: return .gray
        case 8..<9: return .orange
        default: return .secondary
        }
    }
}

// MARK: - Source Comparison View

struct SourceComparisonView: View {
    let comparisonData: ComparisonData
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Cross-Platform Price Spread (PSA 10)")
                .font(.caption)
                .fontWeight(.semibold)
                .foregroundColor(.secondary)
            
            // StockX Data
            if let stockX = comparisonData.stockX {
                SourceDataCard(
                    title: "StockX Ticker",
                    color: .black,
                    items: [
                        ("Last Sale", "$\(String(format: "%.2f", stockX.lastSale))"),
                        ("Lowest Ask", "$\(String(format: "%.2f", stockX.lowestAsk))"),
                        ("Highest Bid", "$\(String(format: "%.2f", stockX.highestBid))")
                    ],
                    url: stockX.url
                )
            }
            
            // TCGPlayer Data
            if let tcgPlayer = comparisonData.tcgPlayer {
                SourceDataCard(
                    title: "TCGPlayer Analyst",
                    color: .green,
                    items: [
                        ("Market Price", "$\(String(format: "%.2f", tcgPlayer.rawMarketPrice))"),
                        ("Listed Median", tcgPlayer.listedMedian != nil ? "$\(String(format: "%.2f", tcgPlayer.listedMedian!))" : "N/A")
                    ],
                    url: tcgPlayer.link
                )
            }
            
            // PWCC Data
            if let pwcc = comparisonData.pwcc {
                SourceDataCard(
                    title: "PWCC Specialist",
                    color: .orange,
                    items: [
                        ("Sale History", "$\(String(format: "%.2f", pwcc.marketPrice))")
                    ],
                    url: pwcc.url
                )
            }
        }
        .padding(.vertical, 4)
    }
}

struct SourceDataCard: View {
    let title: String
    let color: Color
    let items: [(String, String)]
    let url: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(title)
                    .font(.subheadline)
                    .fontWeight(.bold)
                    .foregroundColor(color)
                
                Spacer()
                
                Link(destination: URL(string: url)!) {
                    Text("View")
                        .font(.caption)
                        .fontWeight(.semibold)
                        .foregroundColor(.blue)
                }
            }
            
            ForEach(items, id: \.0) { item in
                HStack {
                    Text(item.0)
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Spacer()
                    Text(item.1)
                        .font(.caption)
                        .fontWeight(.semibold)
                }
            }
        }
        .padding(12)
        .background(Color(.systemGray6))
        .cornerRadius(8)
    }
}
