import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PriceComparisonChart = ({ data, ebayAvg }) => {
    if (!data) return null;

    const chartData = [
        {
            name: 'eBay (Avg)',
            price: ebayAvg || 0,
            fill: '#4F46E5', // Indigo
        },
        {
            name: 'StockX (Ask)',
            price: data.StockX?.lowest_ask || 0,
            fill: '#000000', // Black
        },
        {
            name: 'TCGPlayer',
            price: data.TCGPlayer?.raw_market_price || 0,
            fill: '#22C55E', // Green
        },
        {
            name: 'PWCC (Hist)',
            price: data.PWCC?.market_price || 0,
            fill: '#F59E0B', // Amber
        },
    ].filter(item => item.price > 0);

    if (chartData.length === 0) return (
        <div className="text-center py-8 text-gray-500 italic">
            Insufficient data for price comparison
        </div>
    );

    return (
        <div className="w-full h-64 mt-4">
            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">
                Cross-Platform Price Spread (PSA 10 Benchmark)
            </h3>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} />
                    <YAxis axisLine={false} tickLine={false} tickFormatter={(value) => `$${value}`} />
                    <Tooltip
                        formatter={(value) => [`$${value.toFixed(2)}`, 'Price']}
                        contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)' }}
                    />
                    <Bar dataKey="price" radius={[8, 8, 0, 0]} barSize={50} />
                </BarChart>
            </ResponsiveContainer>
            <div className="mt-4 text-xs text-gray-400 text-center">
                Comparing current lowest asks and market averages across primary sources.
            </div>
        </div>
    );
};

export default PriceComparisonChart;
