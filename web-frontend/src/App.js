import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://pokemon-agg.onrender.com';

const GRADING_COMPANIES = ['PSA', 'BGS', 'CGC', 'SGC', 'TAG', 'ACE', 'PCA'];

function App() {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('featured');
  const [selectedCompanies, setSelectedCompanies] = useState(['PSA', 'BGS', 'CGC']);
  const [featuredCards, setFeaturedCards] = useState([]);

  useEffect(() => {
    axios.get(`${API_BASE_URL}/featured`)
      .then(res => setFeaturedCards(res.data.featured || []))
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
    ? (listings.reduce((sum, l) => sum + l.price, 0) / listings.length).toFixed(2)
    : 0;

  const getPriceChange = (price) => {
    if (!avgPrice || avgPrice === 0) return 0;
    return ((price - avgPrice) / avgPrice * 100).toFixed(1);
  };

  return (
    <div className="min-h-screen">
      {/* Header */}
      <header className="py-6 px-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400 to-purple-500 flex items-center justify-center">
              <span className="text-xl">⚡</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold gradient-text">MintCondition</h1>
              <p className="text-xs text-gray-400 uppercase tracking-wider">Multi-Source Market Intelligence</p>
            </div>
          </div>
          <nav className="flex gap-4 text-sm text-gray-400">
            <a href="#" className="hover:text-cyan-400 transition">API Data</a>
            <a href="#" className="hover:text-cyan-400 transition">Community</a>
            <a href="#" className="hover:text-cyan-400 transition">Privacy</a>
          </nav>
        </div>
      </header>

      {/* Search */}
      <section className="px-4 pb-8">
        <div className="max-w-2xl mx-auto">
          <form onSubmit={handleSearch} className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for any card... (e.g., Charizard Base Set)"
              className="search-input"
            />
            <button type="submit" className="btn-primary whitespace-nowrap">
              Hunt Deals
            </button>
          </form>
        </div>
      </section>

      {/* Tabs */}
      <section className="px-4 pb-6">
        <div className="max-w-6xl mx-auto flex justify-center gap-2">
          <button
            onClick={() => setActiveTab('featured')}
            className={`grade-pill ${activeTab === 'featured' ? 'active' : ''}`}
          >
            Featured Cards
          </button>
          <button
            onClick={() => setActiveTab('results')}
            className={`grade-pill ${activeTab === 'results' ? 'active' : ''}`}
          >
            Search Results
          </button>
        </div>
      </section>

      {/* Grade Filters */}
      <section className="px-4 pb-6">
        <div className="max-w-6xl mx-auto">
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
      <main className="px-4 pb-12">
        <div className="max-w-6xl mx-auto">
          {loading && (
            <div className="flex justify-center py-20">
              <div className="spinner"></div>
            </div>
          )}

          {error && (
            <div className="glass-card p-6 text-center">
              <p className="text-red-400">{error}</p>
            </div>
          )}

          {!loading && !error && activeTab === 'featured' && (
            <>
              <h2 className="text-xl font-semibold text-white mb-2">Trending Collections</h2>
              <p className="text-gray-400 mb-6">Start your hunt with these popular cards tracked by our real-time market engine.</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                {featuredCards.length > 0 ? featuredCards.map((card, idx) => (
                  <div key={idx} className="glass-card p-4 cursor-pointer" onClick={() => { setQuery(card.name); setActiveTab('results'); }}>
                    {card.image_url && (
                      <img src={card.image_url} alt={card.name} className="w-full h-40 object-contain mb-3 rounded-lg" />
                    )}
                    <h3 className="font-semibold text-white">{card.name}</h3>
                    <p className="text-sm text-gray-400">{card.set_name}</p>
                    <div className="flex items-center justify-between mt-3">
                      <span className="text-cyan-400 font-bold">${card.avg_price?.toFixed(2) || 'N/A'}</span>
                      {card.price_change && (
                        <span className={`badge ${card.price_change > 0 ? 'badge-up' : 'badge-down'}`}>
                          {card.price_change > 0 ? '+' : ''}{card.price_change}%
                        </span>
                      )}
                    </div>
                  </div>
                )) : (
                  <div className="col-span-full glass-card p-8 text-center">
                    <p className="text-gray-400">Search for a card to see trending data</p>
                  </div>
                )}
              </div>
            </>
          )}

          {!loading && !error && activeTab === 'results' && searchResults && (
            <>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-semibold text-white">Search Results</h2>
                  <p className="text-sm text-gray-400">{listings.length} listings found • Avg: ${avgPrice}</p>
                </div>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {listings.map((listing, idx) => {
                  const priceChange = getPriceChange(listing.price);
                  const isDeal = priceChange < -10;
                  return (
                    <div key={idx} className={`glass-card p-4 ${isDeal ? 'border-red-500/50' : ''}`}>
                      <div className="flex items-start justify-between mb-3">
                        <span className="badge badge-grade">{listing.company} {listing.grade}</span>
                        {isDeal && <span className="badge bg-red-500/20 text-red-400">STEAL ALERT</span>}
                      </div>
                      <h3 className="font-semibold text-white mb-1">{searchResults.card_name}</h3>
                      <p className="text-sm text-gray-400 mb-3">{listing.title?.substring(0, 60)}...</p>
                      <div className="flex items-center justify-between">
                        <span className="text-2xl font-bold text-cyan-400">${listing.price?.toFixed(2)}</span>
                        <span className={`text-sm ${parseFloat(priceChange) < 0 ? 'price-up' : 'price-down'}`}>
                          {priceChange > 0 ? '+' : ''}{priceChange}%
                        </span>
                      </div>
                      {listing.buy_url && (
                        <a 
                          href={listing.buy_url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="block mt-3 text-center btn-secondary text-sm"
                        >
                          View on eBay →
                        </a>
                      )}
                    </div>
                  );
                })}
              </div>
              {listings.length === 0 && (
                <div className="glass-card p-8 text-center">
                  <p className="text-gray-400">No listings match your filters. Try adjusting the grading company filters.</p>
                </div>
              )}
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-gray-800">
        <div className="max-w-6xl mx-auto text-center text-gray-500 text-sm">
          <p>© 2026 MintCondition • Multi-Source Market Intelligence</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
