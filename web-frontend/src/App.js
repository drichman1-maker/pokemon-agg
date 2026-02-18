import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './index.css';
import PriceComparisonChart from './PriceComparisonChart';

const API_BASE_URL = 'https://pokemon-agg.onrender.com';

function App() {
    const [query, setQuery] = useState('');
    const [searchResults, setSearchResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Advanced Filtering State
    const [selectedCompanies, setSelectedCompanies] = useState(['PSA', 'BGS', 'CGC', 'SGC', 'TAG', 'ACE', 'PCA']);
    const [minGrade, setMinGrade] = useState(0);
    const [sortBy, setSortBy] = useState('DEAL_SCORE'); // DEAL_SCORE, PRICE_ASC, PRICE_DESC, GRADE_DESC, GRADE_ASC

    const [featuredCards, setFeaturedCards] = useState([]);

    // Fetch featured cards on mount
    useEffect(() => {
        axios.get(`${API_BASE_URL}/featured`)
            .then(response => setFeaturedCards(response.data.featured))
            .catch(err => console.error('Failed to load featured cards:', err));
    }, []);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;
        setLoading(true);
        setError(null);
        setSearchResults(null);
        try {
            const response = await axios.get(`${API_BASE_URL}/search`, { params: { q: query } });
            setSearchResults(response.data);

            // Reset filters on new search? Optional. Let's keep them for continuity or reset if needed.
            // For now, let's keep user preferences.
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to fetch results. Check backend connection.');
        } finally {
            setLoading(false);
        }
    };

    const handleFeaturedClick = (card) => {
        setQuery(`${card.name} ${card.set}`);
    };

    const toggleCompany = (company) => {
        setSelectedCompanies(prev => {
            if (prev.includes(company)) {
                // Prevent deselecting the last one? Or allow empty?
                // If we deselect the last one, show nothing? Or All?
                // Let's allow empty to show nothing (strict filter)
                return prev.filter(c => c !== company);
            } else {
                return [...prev, company];
            }
        });
    };

    const getProcessedListings = () => {
        if (!searchResults?.listings) return [];

        // 1. Filter
        let filtered = searchResults.listings.filter(listing => {
            const companyMatch = selectedCompanies.includes(listing.company);
            const gradeMatch = listing.grade >= minGrade;
            return companyMatch && gradeMatch;
        });

        // 2. Sort
        return filtered.sort((a, b) => {
            switch (sortBy) {
                case 'PRICE_ASC':
                    return a.price - b.price;
                case 'PRICE_DESC':
                    return b.price - a.price;
                case 'GRADE_DESC':
                    return b.grade - a.grade; // High grades first
                case 'GRADE_ASC':
                    return a.grade - b.grade;
                case 'DEAL_SCORE':
                default:
                    // Primary: Deal Score (desc), Secondary: Price (asc)
                    const scoreDiff = (b.deal_score || 0) - (a.deal_score || 0);
                    if (scoreDiff !== 0) return scoreDiff;
                    return a.price - b.price;
            }
        });
    };

    const processedListings = getProcessedListings();

    const getGradeColor = (grade) => {
        if (grade === 10) return 'text-yellow-400 font-bold';
        if (grade >= 9) return 'text-gray-300 font-semibold';
        if (grade >= 8) return 'text-orange-400 font-semibold';
        return 'text-gray-400';
    };

    // Helper to format release date
    // e.g., "1999/01/09" -> "1999"
    const getReleaseYear = (dateString) => {
        if (!dateString) return null;
        return dateString.split('/')[0];
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white font-sans selection:bg-cyan-500/30">
            {/* Animated Background Layers */}
            <div className="fixed inset-0 bg-[linear-gradient(to_right,#1f2937_1px,transparent_1px),linear-gradient(to_bottom,#1f2937_1px,transparent_1px)] bg-[size:4rem_4rem] opacity-20 pointer-events-none"></div>
            <div className="fixed inset-0 bg-radial-gradient from-cyan-500/10 via-transparent to-transparent opacity-50 pointer-events-none"></div>

            {/* Header */}
            <header className="relative z-50 bg-black/40 backdrop-blur-xl border-b border-cyan-500/20 shadow-2xl shadow-cyan-500/5">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
                    <div className="flex items-center gap-4">
                        <div className="w-12 h-12 bg-gradient-to-br from-cyan-400 to-blue-600 rounded-xl flex items-center justify-center shadow-lg shadow-cyan-500/40 animate-pulse-slow">
                            <span className="text-2xl drop-shadow-md">⚡</span>
                        </div>
                        <div>
                            <h1 className="text-3xl font-black tracking-tight bg-gradient-to-r from-white via-cyan-200 to-blue-400 bg-clip-text text-transparent">
                                PokeAggregator
                            </h1>
                            <p className="text-xs text-cyan-400/80 font-mono tracking-wider uppercase">Multi-Source Market Intelligence</p>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Search Section */}
                <form onSubmit={handleSearch} className="mb-12 max-w-4xl mx-auto">
                    <div className="relative group">
                        <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200"></div>
                        <div className="relative flex gap-3 p-2 bg-gray-900/80 backdrop-blur-xl rounded-2xl border border-white/10 shadow-2xl">
                            <div className="flex-1 relative flex items-center">
                                <span className="absolute left-4 text-cyan-500">
                                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                                </span>
                                <input
                                    type="text"
                                    value={query}
                                    onChange={(e) => setQuery(e.target.value)}
                                    placeholder="Search cards (e.g., Charizard Base Set)..."
                                    className="w-full pl-12 pr-4 py-3 bg-transparent text-xl font-medium text-white placeholder-gray-500 focus:outline-none"
                                />
                            </div>
                            <button
                                type="submit"
                                disabled={loading}
                                className="px-8 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-bold rounded-xl hover:from-cyan-400 hover:to-blue-500 focus:ring-2 focus:ring-cyan-500/50 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)] hover:shadow-[0_0_30px_rgba(6,182,212,0.5)] active:scale-[0.98]"
                            >
                                {loading ? (
                                    <div className="flex items-center gap-2">
                                        <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                                        <span>Scanning...</span>
                                    </div>
                                ) : 'Hunt Deals'}
                            </button>
                        </div>
                    </div>
                </form>

                {error && (
                    <div className="mb-8 p-4 bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl backdrop-blur-md flex items-start gap-3 animate-fade-in-up">
                        <span className="text-xl">⚠️</span>
                        <div>
                            <h3 className="font-bold">Search Error</h3>
                            <p className="text-sm opacity-80">{error}</p>
                        </div>
                    </div>
                )}

                {/* Featured Cards (Empty State) */}
                {!searchResults && !loading && (
                    <div className="animate-fade-in-up space-y-8">
                        <div className="text-center">
                            <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent mb-3">Trending Collections</h2>
                            <p className="text-gray-400 max-w-2xl mx-auto">Start your hunt with these popular cards tracked by our real-time market engine.</p>
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
                            {featuredCards.map((card, index) => (
                                <div
                                    key={index}
                                    onClick={() => handleFeaturedClick(card)}
                                    className="group cursor-pointer relative bg-gray-800/40 backdrop-blur-md rounded-2xl border border-white/5 hover:border-cyan-500/50 transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_10px_40px_-10px_rgba(6,182,212,0.3)]"
                                >
                                    <div className="p-4">
                                        <div className="relative aspect-[2.5/3.5] mb-4 rounded-lg overflow-hidden shadow-lg group-hover:shadow-cyan-500/20 transition-all">
                                            <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500/20 to-purple-600/20 opacity-0 group-hover:opacity-100 transition-opacity z-10"></div>
                                            <img src={card.image} alt={card.name} className="w-full h-full object-contain transform group-hover:scale-110 transition-transform duration-500" />
                                        </div>
                                        <h3 className="font-bold text-center text-white mb-1 group-hover:text-cyan-400 transition-colors">{card.name}</h3>
                                        <p className="text-xs text-center text-gray-500 group-hover:text-gray-400">{card.set}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {/* Search Results Dashboard */}
                {searchResults && (
                    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-fade-in-up">
                        {/* Sidebar: Card Intel & Analytics */}
                        <div className="lg:col-span-4 space-y-6">
                            {/* Card Intel Card */}
                            {searchResults.card && (
                                <div className="bg-gray-800/40 backdrop-blur-xl rounded-2xl border border-white/10 shadow-2xl overflow-hidden">
                                    <div className="p-6">
                                        <div className="flex items-center justify-between mb-4">
                                            <h2 className="text-lg font-bold text-white flex items-center gap-2">
                                                <span className="text-cyan-400">🎯</span> Asset Intel
                                            </h2>
                                            {searchResults.card.release_date && (
                                                <span className="px-3 py-1 bg-gray-700/50 rounded-full text-xs font-mono text-cyan-300 border border-cyan-500/20">
                                                    Est. {getReleaseYear(searchResults.card.release_date)}
                                                </span>
                                            )}
                                        </div>
                                        <div className="relative mb-6 rounded-xl overflow-hidden bg-gray-900/50 border border-white/5 shadow-inner p-4">
                                            <img src={searchResults.card.image_url} alt={searchResults.card.name} className="w-full h-auto object-contain drop-shadow-2xl" />
                                        </div>
                                        <div className="space-y-4">
                                            <div>
                                                <h3 className="text-2xl font-bold text-white leading-tight">{searchResults.card.name}</h3>
                                                <p className="text-cyan-400 font-medium">{searchResults.card.set_name}</p>
                                            </div>
                                            <div className="grid grid-cols-2 gap-4 pt-4 border-t border-white/10">
                                                <div>
                                                    <span className="text-xs text-gray-500 uppercase tracking-wider">Number</span>
                                                    <p className="font-mono text-gray-300">{searchResults.card.number}</p>
                                                </div>
                                                <div>
                                                    <span className="text-xs text-gray-500 uppercase tracking-wider">Rarity</span>
                                                    <p className="font-mono text-gray-300">{searchResults.card.rarity}</p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* Market Pulse */}
                            {searchResults.market_stats && (
                                <div className="bg-gray-800/40 backdrop-blur-xl rounded-2xl border border-white/10 shadow-xl p-6">
                                    <div className="flex items-center justify-between mb-6">
                                        <h2 className="text-lg font-bold text-white flex items-center gap-2">
                                            <span className="text-cyan-400">📊</span> Market Pulse
                                        </h2>
                                        <span className="text-xs font-bold text-gray-500 bg-black/30 px-2 py-1 rounded">eBay 24h</span>
                                    </div>
                                    <div className="space-y-3">
                                        {['10.0', '9.5', '9.0', '8.5', '8.0'].map(grade => {
                                            const stats = searchResults.market_stats[grade];
                                            if (!stats) return null;
                                            return (
                                                <div key={grade} className="group flex justify-between items-center p-3 bg-gray-700/20 hover:bg-gray-700/40 rounded-xl border border-white/5 transition-colors">
                                                    <span className={`text-lg font-bold ${getGradeColor(parseFloat(grade))}`}>{grade}</span>
                                                    <div className="text-right">
                                                        <div className="font-mono font-bold text-white">${stats.average.toFixed(2)}</div>
                                                        <div className="text-xs text-gray-500">{stats.count} sold</div>
                                                    </div>
                                                </div>
                                            );
                                        })}
                                    </div>
                                </div>
                            )}

                            {/* Source Comparison */}
                            {searchResults.comparison_data && (
                                <div className="bg-gray-800/40 backdrop-blur-xl rounded-2xl border border-white/10 shadow-xl p-6">
                                    <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                                        <span className="text-cyan-400">🌐</span> Cross-Market Data
                                    </h2>
                                    <PriceComparisonChart
                                        data={searchResults.comparison_data}
                                        ebayAvg={searchResults.market_stats?.['10.0']?.average}
                                    />
                                    <div className="mt-6 flex flex-col gap-3">
                                        {searchResults.comparison_data.StockX && (
                                            <a href={searchResults.comparison_data.StockX.url} target="_blank" rel="noreferrer" className="flex justify-between items-center p-3 rounded-xl bg-black/20 hover:bg-green-900/10 border border-white/5 hover:border-green-500/30 transition-all group">
                                                <span className="font-bold text-gray-300 group-hover:text-green-400">StockX</span>
                                                <span className="font-mono text-green-500">${searchResults.comparison_data.StockX.lowest_ask}</span>
                                            </a>
                                        )}
                                        {searchResults.comparison_data.TCGPlayer && (
                                            <a href={searchResults.comparison_data.TCGPlayer.link} target="_blank" rel="noreferrer" className="flex justify-between items-center p-3 rounded-xl bg-black/20 hover:bg-blue-900/10 border border-white/5 hover:border-blue-500/30 transition-all group">
                                                <span className="font-bold text-gray-300 group-hover:text-blue-400">TCGPlayer</span>
                                                <span className="font-mono text-blue-500">${searchResults.comparison_data.TCGPlayer.raw_market_price}</span>
                                            </a>
                                        )}
                                        {searchResults.comparison_data.PWCC && (
                                            <a href={searchResults.comparison_data.PWCC.url} target="_blank" rel="noreferrer" className="flex justify-between items-center p-3 rounded-xl bg-black/20 hover:bg-orange-900/10 border border-white/5 hover:border-orange-500/30 transition-all group">
                                                <span className="font-bold text-gray-300 group-hover:text-orange-400">PWCC</span>
                                                <span className="font-mono text-orange-500">${searchResults.comparison_data.PWCC.market_price}</span>
                                            </a>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Main Listings Feed */}
                        <div className="lg:col-span-8 space-y-6">
                            {/* Filter Bar */}
                            <div className="bg-gray-800/60 backdrop-blur-xl rounded-2xl border border-white/10 shadow-xl p-5 sticky top-24 z-30">
                                <div className="flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">
                                    {/* Multi-Select Companies */}
                                    <div className="space-y-2">
                                        <div className="text-xs font-bold text-gray-500 uppercase tracking-widest">Grading Service</div>
                                        <div className="flex flex-wrap gap-2">
                                            {['PSA', 'BGS', 'CGC', 'SGC', 'TAG', 'ACE', 'PCA'].map(company => {
                                                const isActive = selectedCompanies.includes(company);
                                                return (
                                                    <button
                                                        key={company}
                                                        onClick={() => toggleCompany(company)}
                                                        className={`px-4 py-2 rounded-lg font-bold text-sm transition-all duration-200 border ${isActive
                                                            ? 'bg-cyan-500 text-white border-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.4)]'
                                                            : 'bg-black/20 text-gray-500 border-white/5 hover:bg-white/5 hover:text-gray-300'
                                                            }`}
                                                    >
                                                        {company}
                                                    </button>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    {/* Sort Controls */}
                                    <div className="space-y-2">
                                        <div className="text-xs font-bold text-gray-500 uppercase tracking-widest pl-1">Sort By</div>
                                        <div className="bg-black/20 p-1 rounded-xl border border-white/5 flex gap-1">
                                            <button
                                                onClick={() => setSortBy('DEAL_SCORE')}
                                                className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-all ${sortBy === 'DEAL_SCORE' ? 'bg-indigo-500 text-white shadow-lg' : 'text-gray-500 hover:text-gray-300'}`}
                                            >
                                                Best Value
                                            </button>
                                            <button
                                                onClick={() => setSortBy('PRICE_ASC')}
                                                className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-all ${sortBy === 'PRICE_ASC' ? 'bg-gray-700 text-white' : 'text-gray-500 hover:text-gray-300'}`}
                                            >
                                                Price ↑
                                            </button>
                                            <button
                                                onClick={() => setSortBy('PRICE_DESC')}
                                                className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-all ${sortBy === 'PRICE_DESC' ? 'bg-gray-700 text-white' : 'text-gray-500 hover:text-gray-300'}`}
                                            >
                                                Price ↓
                                            </button>
                                            <button
                                                onClick={() => setSortBy('GRADE_DESC')}
                                                className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-all ${sortBy === 'GRADE_DESC' ? 'bg-gray-700 text-white' : 'text-gray-500 hover:text-gray-300'}`}
                                            >
                                                Grade ↓
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                <div className="mt-4 pt-4 border-t border-white/5 flex items-center justify-between">
                                    <div className="text-xs text-gray-400">
                                        Showing <span className="text-white font-bold">{processedListings.length}</span> results
                                    </div>
                                    <div className="flex gap-1">
                                        {[0, 10, 9, 8, 7, 6].map(grade => (
                                            <button
                                                key={grade}
                                                onClick={() => setMinGrade(grade)}
                                                className={`px-2 py-1 rounded text-xs font-bold transition-all ${minGrade === grade ? 'text-cyan-400 bg-cyan-900/20' : 'text-gray-600 hover:text-gray-400'}`}
                                            >
                                                {grade === 0 ? 'Any Grade' : `${grade}+`}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Listings Grid */}
                            <div className="space-y-4">
                                {processedListings.length > 0 ? (
                                    processedListings.map((listing, index) => (
                                        <div key={index} className="group relative bg-gray-800/40 backdrop-blur-md rounded-2xl border border-white/5 p-[1px] hover:bg-gray-700/50 transition-all duration-300 hover:scale-[1.01] hover:shadow-2xl">
                                            {/* Arbitrage/Steal Gradient Border Overlay */}
                                            {listing.arbitrage_opportunity && <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-indigo-500 to-purple-500 opacity-20 blur-md pointer-events-none"></div>}
                                            {listing.is_steal && !listing.arbitrage_opportunity && <div className="absolute inset-0 rounded-2xl bg-gradient-to-r from-green-500 to-emerald-500 opacity-20 blur-md pointer-events-none"></div>}

                                            <div className="relative bg-gray-900/60 rounded-2xl p-4 flex gap-5 items-center backdrop-blur-sm h-full">
                                                {/* Left: Grade Badge */}
                                                <div className="flex flex-col items-center justify-center w-20 h-20 bg-black/40 rounded-xl border border-white/10 shadow-inner shrink-0 group-hover:border-cyan-500/30 transition-colors">
                                                    <span className={`text-2xl font-black ${getGradeColor(listing.grade)}`}>{listing.grade}</span>
                                                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">{listing.company}</span>
                                                </div>

                                                {/* Middle: Info */}
                                                <div className="flex-1 min-w-0">
                                                    <div className="flex flex-wrap gap-2 mb-2">
                                                        {listing.arbitrage_opportunity && (
                                                            <span className="px-2 py-0.5 rounded-md bg-indigo-500/20 text-indigo-300 text-[10px] font-black uppercase tracking-wide border border-indigo-500/30 shadow-[0_0_10px_rgba(99,102,241,0.2)]">
                                                                ⚡ Arbitrage
                                                            </span>
                                                        )}
                                                        {listing.is_steal && (
                                                            <span className="px-2 py-0.5 rounded-md bg-green-500/20 text-green-300 text-[10px] font-black uppercase tracking-wide border border-green-500/30 shadow-[0_0_10px_rgba(34,197,94,0.2)]">
                                                                🔥 Steal
                                                            </span>
                                                        )}
                                                    </div>
                                                    <h4 className="text-lg font-bold text-white truncate group-hover:text-cyan-400 transition-colors">{listing.title}</h4>
                                                    <div className="flex gap-4 mt-1 text-xs text-gray-500">
                                                        <span>{listing.condition}</span>
                                                        <span>•</span>
                                                        <span>{listing.source}</span>
                                                    </div>
                                                </div>

                                                {/* Right: Price & CTA */}
                                                <div className="text-right shrink-0">
                                                    <div className="text-3xl font-black text-white tracking-tight mb-2 group-hover:text-cyan-300 transition-colors">${listing.price.toFixed(2)}</div>
                                                    <a
                                                        href={listing.url}
                                                        target="_blank"
                                                        rel="noreferrer"
                                                        className="inline-flex items-center gap-1 px-4 py-2 bg-white/5 hover:bg-cyan-500 hover:text-black text-white text-sm font-bold rounded-lg transition-all border border-white/10 hover:border-cyan-400 hover:shadow-[0_0_20px_rgba(6,182,212,0.4)]"
                                                    >
                                                        View Deal <span className="text-xs">→</span>
                                                    </a>
                                                </div>
                                            </div>
                                        </div>
                                    ))
                                ) : (
                                    <div className="text-center py-24 bg-gray-800/20 rounded-3xl border border-white/5 border-dashed">
                                        <div className="text-6xl mb-4 opacity-20">🔍</div>
                                        <h3 className="text-xl font-bold text-gray-400">No listings found</h3>
                                        <p className="text-sm text-gray-600">Try adjusting your filters or search terms.</p>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default App;
