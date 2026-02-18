import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://pokemon-agg.onrender.com';

const GRADING_COMPANIES = ['PSA', 'BGS', 'CGC', 'SGC', 'TAG', 'ACE', 'PCA'];

const sampleFeatured = [
  { name: 'Charizard', set: 'Base Set', avg_price: 2900, price_change: 15.2, image_url: 'https://images.pokemontcg.io/base1/4.png' },
  { name: 'Pikachu', set: 'Base Set', avg_price: 245, price_change: 8.1, image_url: 'https://images.pokemontcg.io/base1/25.png' },
  { name: 'Mewtwo', set: 'Base Set', avg_price: 1200, price_change: -3.4, image_url: 'https://images.pokemontcg.io/base1/96.png' },
  { name: 'Blastoise', set: 'Base Set', avg_price: 880, price_change: 5.7, image_url: 'https://images.pokemontcg.io/base1/9.png' },
  { name: 'Venusaur', set: 'Base Set', avg_price: 714, price_change: 2.3, image_url: 'https://images.pokemontcg.io/base1/3.png' },
  { name: 'Gyarados', set: 'Base Set', avg_price: 490, price_change: -1.2, image_url: 'https://images.pokemontcg.io/base1/130.png' },
];

function App() {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('featured');
  const [selectedCompanies, setSelectedCompanies] = useState(['PSA', 'BGS', 'CGC']);
  const [featuredCards, setFeaturedCards] = useState(sampleFeatured);

  useEffect(() => {
    axios.get(`${API_BASE_URL}/featured`)
      .then(res => {
        if (res.data.featured && res.data.featured.length > 0) {
          setFeaturedCards(res.data.featured);
        }
      })
      .catch(err => console.error('Failed to load featured:', err));
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    setActiveTab('results');
    try {
      const response = await axios.get(`${API_BASE_URL}/search`, { params: { q: query } });
      setSearchResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to fetch results. Check backend connection.');
    } finally {
      setLoading(false);
    }
  };

  const toggleCompany = (company) => {
    setSelectedCompanies(prev => 
      prev.includes(company) 
        ? prev.filter(c => c !== company) 
        : [...prev, company]
    );
  };

  const getProcessedListings = () => {
    if (!searchResults?.listings) return [];
    return searchResults.listings.filter(listing => 
      selectedCompanies.includes(listing.company) && listing.grade >= 1
    );
  };

  const listings = getProcessedListings();
  const avgPrice = listings.length > 0 
    ? (listings.reduce((sum, l) => sum + l.price, 0) / listings.length)
    : 0;

  const getPriceChange = (price) => {
    if (!avgPrice || avgPrice === 0) return 0;
    return ((price - avgPrice) / avgPrice * 100).toFixed(1);
  };

  return (
    <div className="min-h-screen pb-20">
      {/* Header */}
      <header className="py-8 px-4 border-b border-gray-800/50">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-400 via-teal-500 to-purple-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <span className="text-2xl">⚡</span>
            </div>
            <div>
              <h1 className="text-3xl font-bold gradient-text">MintCondition</h1>
              <p className="text-xs text-gray-500 uppercase tracking-[0.2em]">Multi-Source Market Intelligence</p>
            </div>
          </div>
          <nav className="flex gap-6 text-sm text-gray-400">
            <span className="cursor-pointer hover:text-cyan-400 transition">API Data</span>
            <span className="cursor-pointer hover:text-cyan-400 transition">Community</span>
            <span className="cursor-pointer hover:text-cyan-400 transition">Privacy</span>
          </nav>
        </div>
      </header>

      {/* Search */}
      <section className="px-4 py-10">
        <div className="max-w-3xl mx-auto">
          <form onSubmit={handleSearch} className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for any card... (e.g., Charizard Base Set)"
              className="search-input text-lg"
            />
            <button type="submit" className="btn-primary text-lg px-8">
              Hunt Deals
            </button>
          </form>
        </div>
      </section>

      {/* Tabs */}
      <section className="px-4 pb-6">
        <div className="max-w-7xl mx-auto flex justify-center gap-3">
          <button
            onClick={() => setActiveTab('featured')}
            className={`grade-pill text-base px-6 py-3 ${activeTab === 'featured' ? 'active' : ''}`}
          >
            Featured Cards
          </button>
          <button
            onClick={() => setActiveTab('results')}
            className={`grade-pill text-base px-6 py-3 ${activeTab === 'results' ? 'active' : ''}`}
          >
            Search Results
          </button>
        </div>
      </section>

      {/* Grade Filters */}
      <section className="px-4 pb-8">
        <div className="max-w-7xl mx-auto">
          <p className="text-xs text-gray-500 uppercase tracking-wider mb-3">Filter by Grading Company</p>
          <div className="flex flex-wrap gap-2">
            {GRADING_COMPANIES.map(company => (
              <button
                key={company}
                onClick={() => toggleCompany(company)}
                className={`grade-pill ${selectedCompanies.includes(company) ? 'active' : ''}`}
              >
                {company} {selectedCompanies.includes(company) && '✓'}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content */}
      <main className="px-4">
        <div className="max-w-7xl mx-auto">
          {loading && (
            <div className="flex justify-center py-20">
              <div className="spinner"></div>
            </div>
          )}

          {error && (
            <div className="glass-card p-8 text-center max-w-md mx-auto">
              <p className="text-red-400 text-lg">{error}</p>
            </div>
          )}

          {!loading && !error && activeTab === 'featured' && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">Trending Collections</h2>
              <p className="text-gray-400 mb-8 max-w-2xl">Start your hunt with these popular cards tracked by our real-time market engine.</p>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {featuredCards.map((card, idx) => (
                  <div 
                    key={idx} 
                    className="glass-card p-4 cursor-pointer group"
                    onClick={() => { setQuery(card.name); setActiveTab('results'); }}
                  >
                    <div className="relative mb-3">
                      {card.image_url && (
                        <img 
                          src={card.image_url} 
                          alt={card.name} 
                          className="w-full h-32 object-contain group-hover:scale-105 transition-transform duration-300" 
                        />
                      )}
                      <div className={`absolute -top-2 -right-2 badge ${
                        (card.price_change || 0) >= 0 ? 'badge-up' : 'badge-down'
                      }`}>
                        {(card.price_change || 0) >= 0 ? '+' : ''}{card.price_change || 0}%
                      </div>
                    </div>
                    <h3 className="font-bold text-white text-lg">{card.name}</h3>
                    <p className="text-sm text-gray-400">{card.set}</p>
                    <div className="mt-3">
                      <span className="text-xl font-bold gradient-text">${card.avg_price?.toLocaleString() || 'N/A'}</span>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}

          {!loading && !error && activeTab === 'results' && searchResults && (
            <>
              <div className="flex items-center justify-between mb-8">
                <div>
                  <h2 className="text-2xl font-bold text-white">Search Results</h2>
                  <p className="text-gray-400">{listings.length} listings found • Avg: ${avgPrice.toFixed(2)}</p>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
                {listings.map((listing, idx) => {
                  const priceChange = getPriceChange(listing.price);
                  const isDeal = parseFloat(priceChange) < -10;
                  const isSteal = parseFloat(priceChange) < -20;
                  return (
                    <div 
                      key={idx} 
                      className={`glass-card p-5 relative overflow-hidden ${
                        isDeal ? 'border-red-500/50' : ''
                      } ${isSteal ? 'border-red-500 animate-pulse' : ''}`}
                    >
                      {isDeal && (
                        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-red-500 to-orange-500"></div>
                      )}
                      <div className="flex items-start justify-between mb-3">
                        <span className="badge badge-grade text-sm">{listing.company} {listing.grade}</span>
                        {isDeal && (
                          <span className="badge bg-red-500/20 text-red-400 text-xs">
                            {isSteal ? '🔥 STEAL' : 'DEAL'}
                          </span>
                        )}
                      </div>
                      <h3 className="font-bold text-white text-lg mb-1">{searchResults.card_name}</h3>
                      <p className="text-sm text-gray-400 mb-4 line-clamp-2">{listing.title?.substring(0, 80)}...</p>
                      
                      <div className="flex items-end justify-between">
                        <div>
                          <span className="text-2xl font-bold gradient-text">${listing.price?.toFixed(2)}</span>
                          {avgPrice > 0 && (
                            <p className={`text-sm ${parseFloat(priceChange) < 0 ? 'price-up' : 'price-down'}`}>
                              {priceChange > 0 ? '+' : ''}{priceChange}% vs avg
                            </p>
                          )}
                        </div>
                      </div>
                      
                      {listing.buy_url && (
                        <a 
                          href={listing.buy_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="block mt-4 text-center btn-secondary text-sm py-2"
                        >
                          View Deal →
                        </a>
                      )}
                    </div>
                  );
                })}
              </div>
              {listings.length === 0 && (
                <div className="glass-card p-12 text-center">
                  <p className="text-gray-400 text-lg">No listings match your filters. Try adjusting the grading company filters.</p>
                </div>
              )}
            </>
          )}

          {!loading && !error && activeTab === 'results' && !searchResults && (
            <div className="glass-card p-12 text-center">
              <p className="text-gray-400 text-lg">Search for a card to see results</p>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="py-10 px-4 border-t border-gray-800/50 mt-20">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-gray-500">© 2026 MintCondition • Multi-Source Market Intelligence</p>
          <div className="flex justify-center gap-6 mt-4 text-sm text-gray-600">
            <span className="cursor-pointer hover:text-cyan-400 transition">API Data</span>
            <span className="cursor-pointer hover:text-cyan-400 transition">Community</span>
            <span className="cursor-pointer hover:text-cyan-400 transition">Terms</span>
            <span className="cursor-pointer hover:text-cyan-400 transition">Privacy</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
