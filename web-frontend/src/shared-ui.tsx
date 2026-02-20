import React from 'react';

// ─── Types ───────────────────────────────────────────────────────────────────

export interface Retailer {
    name: string;
    url: string;
    price: number;
}

export interface ProductSpecs {
    grading_company?: string;
    grade?: number;
    set?: string;
    year?: number;
    number?: string;
    rarity?: string;
}

export interface Product {
    id: string;
    name: string;
    category: string;
    brand: string;
    image_url: string;
    retailers: Retailer[];
    specs: ProductSpecs;
    updated_at: string;
}

// ─── Badge Component ─────────────────────────────────────────────────────────

interface BadgeProps {
    label: string;
    variant?: 'grade' | 'category' | 'deal' | 'default';
    className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ label, variant = 'default', className = '' }) => {
    const variantStyles: Record<string, string> = {
        grade:
            'bg-gradient-to-r from-yellow-500/20 to-amber-500/20 text-yellow-300 border border-yellow-500/30 shadow-[0_0_10px_rgba(234,179,8,0.15)]',
        category:
            'bg-cyan-500/15 text-cyan-300 border border-cyan-500/20',
        deal:
            'bg-green-500/15 text-green-300 border border-green-500/30 shadow-[0_0_10px_rgba(34,197,94,0.15)]',
        default:
            'bg-white/5 text-gray-400 border border-white/10',
    };

    return (
        <span
            className={`inline-flex items-center px-2.5 py-1 rounded-lg text-[11px] font-black uppercase tracking-wider ${variantStyles[variant]} ${className}`}
        >
            {label}
        </span>
    );
};

// ─── RetailerLink Component ──────────────────────────────────────────────────

interface RetailerLinkProps {
    retailer: Retailer;
}

const retailerColors: Record<string, { bg: string; hover: string; text: string }> = {
    eBay: { bg: 'bg-blue-500/10', hover: 'hover:bg-blue-500/25', text: 'text-blue-400' },
    TCGPlayer: { bg: 'bg-green-500/10', hover: 'hover:bg-green-500/25', text: 'text-green-400' },
    StockX: { bg: 'bg-emerald-500/10', hover: 'hover:bg-emerald-500/25', text: 'text-emerald-400' },
    PWCC: { bg: 'bg-orange-500/10', hover: 'hover:bg-orange-500/25', text: 'text-orange-400' },
    'Heritage Auctions': { bg: 'bg-purple-500/10', hover: 'hover:bg-purple-500/25', text: 'text-purple-400' },
};

export const RetailerLink: React.FC<RetailerLinkProps> = ({ retailer }) => {
    const colors = retailerColors[retailer.name] || {
        bg: 'bg-white/5',
        hover: 'hover:bg-white/10',
        text: 'text-gray-300',
    };

    return (
        <a
            href={retailer.url}
            target="_blank"
            rel="noopener noreferrer"
            className={`flex items-center justify-between px-4 py-3 rounded-xl ${colors.bg} ${colors.hover} border border-white/5 hover:border-white/15 transition-all duration-200 group`}
        >
            <span className={`font-bold text-sm ${colors.text}`}>{retailer.name}</span>
            <div className="flex items-center gap-2">
                <span className="font-mono font-bold text-white text-sm">
                    ${retailer.price.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                </span>
                <span className="text-gray-600 group-hover:text-white/50 transition-colors text-xs">→</span>
            </div>
        </a>
    );
};

// ─── SearchBar Component ─────────────────────────────────────────────────────

interface SearchBarProps {
    value: string;
    onChange: (value: string) => void;
    onSubmit: () => void;
    loading?: boolean;
    placeholder?: string;
}

export const SearchBar: React.FC<SearchBarProps> = ({
    value,
    onChange,
    onSubmit,
    loading = false,
    placeholder = 'Search products...',
}) => {
    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onSubmit();
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-4xl mx-auto">
            <div className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-50 transition duration-1000 group-hover:duration-200" />
                <div className="relative flex gap-3 p-2 bg-gray-900/80 backdrop-blur-xl rounded-2xl border border-white/10 shadow-2xl">
                    <div className="flex-1 relative flex items-center">
                        <span className="absolute left-4 text-cyan-500">
                            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path
                                    strokeLinecap="round"
                                    strokeLinejoin="round"
                                    strokeWidth={2}
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                                />
                            </svg>
                        </span>
                        <input
                            type="text"
                            value={value}
                            onChange={(e) => onChange(e.target.value)}
                            placeholder={placeholder}
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
                                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                                <span>Scanning...</span>
                            </div>
                        ) : (
                            'Search'
                        )}
                    </button>
                </div>
            </div>
        </form>
    );
};

// ─── PriceTable Component ────────────────────────────────────────────────────

interface PriceTableProps {
    retailers: Retailer[];
}

export const PriceTable: React.FC<PriceTableProps> = ({ retailers }) => {
    if (!retailers || retailers.length === 0) return null;

    const sorted = [...retailers].sort((a, b) => a.price - b.price);
    const lowestPrice = sorted[0].price;

    return (
        <div className="bg-gray-800/30 backdrop-blur-md rounded-2xl border border-white/5 overflow-hidden">
            <div className="px-5 py-4 border-b border-white/5">
                <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider flex items-center gap-2">
                    <span className="text-cyan-400">💰</span> Price Comparison
                </h3>
            </div>
            <div className="divide-y divide-white/5">
                {sorted.map((retailer, idx) => {
                    const isLowest = retailer.price === lowestPrice;
                    return (
                        <a
                            key={`${retailer.name}-${idx}`}
                            href={retailer.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center justify-between px-5 py-3.5 hover:bg-white/5 transition-colors group"
                        >
                            <div className="flex items-center gap-3">
                                {isLowest && (
                                    <span className="text-[10px] font-black text-green-400 bg-green-500/10 px-2 py-0.5 rounded border border-green-500/20">
                                        BEST
                                    </span>
                                )}
                                <span className="font-bold text-gray-300 group-hover:text-white transition-colors">
                                    {retailer.name}
                                </span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className={`font-mono font-bold ${isLowest ? 'text-green-400' : 'text-white'}`}>
                                    ${retailer.price.toLocaleString('en-US', { minimumFractionDigits: 2 })}
                                </span>
                                <span className="text-gray-600 group-hover:text-cyan-400 transition-colors">→</span>
                            </div>
                        </a>
                    );
                })}
            </div>
        </div>
    );
};

// ─── ProductCard Component ───────────────────────────────────────────────────

interface ProductCardProps {
    product: Product;
    onClick?: (product: Product) => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onClick }) => {
    const lowestPrice = product.retailers.length
        ? Math.min(...product.retailers.map((r) => r.price))
        : 0;
    const highestPrice = product.retailers.length
        ? Math.max(...product.retailers.map((r) => r.price))
        : 0;

    return (
        <div
            onClick={() => onClick?.(product)}
            className="group cursor-pointer relative bg-gray-800/40 backdrop-blur-md rounded-2xl border border-white/5 hover:border-cyan-500/30 transition-all duration-300 hover:-translate-y-1 hover:shadow-[0_10px_40px_-10px_rgba(6,182,212,0.25)] overflow-hidden"
        >
            {/* Image */}
            <div className="relative aspect-[2.5/3.5] overflow-hidden bg-gray-900/50">
                <div className="absolute inset-0 bg-gradient-to-tr from-cyan-500/10 to-purple-600/10 opacity-0 group-hover:opacity-100 transition-opacity z-10" />
                <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-full h-full object-contain p-4 transform group-hover:scale-105 transition-transform duration-500"
                />
                {/* Grade Badge Overlay */}
                {product.specs.grade && (
                    <div className="absolute top-3 right-3 z-20">
                        <Badge
                            label={`${product.specs.grading_company} ${product.specs.grade}`}
                            variant="grade"
                        />
                    </div>
                )}
            </div>

            {/* Info */}
            <div className="p-4 space-y-3">
                <div>
                    <h3 className="font-bold text-white text-sm leading-tight group-hover:text-cyan-400 transition-colors line-clamp-2">
                        {product.name}
                    </h3>
                    <p className="text-xs text-gray-500 mt-1">
                        {product.specs.set} • {product.specs.year}
                    </p>
                </div>

                {/* Price Range */}
                <div className="flex items-baseline gap-2">
                    <span className="font-mono font-bold text-lg text-white">
                        ${lowestPrice.toLocaleString('en-US')}
                    </span>
                    {highestPrice > lowestPrice && (
                        <span className="text-xs text-gray-500">
                            – ${highestPrice.toLocaleString('en-US')}
                        </span>
                    )}
                </div>

                {/* Retailer Count */}
                <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">
                        {product.retailers.length} retailer{product.retailers.length !== 1 ? 's' : ''}
                    </span>
                    <Badge label={product.specs.rarity || product.category} variant="category" />
                </div>
            </div>
        </div>
    );
};
