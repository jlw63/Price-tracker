"use client";

import { useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<null | {price: string; status: string} > (null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<{price: string; scraped_at: string}[]>([]);


  const scrape = async () => {
      //fetch current price
      setLoading(true);
      const response = await fetch(`http://localhost:8000/scrape?url=${encodeURIComponent(url)}`);
      const data = await response.json();
      setResult(data);

      //fetch histroy
      const historyResponse = await fetch(`http://localhost:8000/history?url=${encodeURIComponent(url)}`);
      const historyData = await historyResponse.json();
      setHistory(historyData);

      setLoading(false);
  };

  return (
    <main className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center p-8">
      <h1 className="text-4xl font-bold mb-2">🔔 Price Tracker</h1>
      <p className="text-gray-400 mb-8">Paste a PB Tech product URL to track its price</p>
<div className="w-full max-w-xl flex gap-2">
  <input
    type="text"
    placeholder="https://www.pbtech.co.nz/product/..."
    value={url}
    onChange={(e) => setUrl(e.target.value)}
    className="flex-1 bg-gray-800 rounded-lg px-4 py-3 text-white outline-none"
  />
  <button
    onClick={scrape}
    disabled={loading}
    className="bg-blue-600 hover:bg-blue-800 px-6 py-3 rounded-lg font-semibold"
  >
    {loading ? "Checking..." : "Track"}
  </button>
</div>
{result && (
  <div className="mt-8 bg-gray-800 rounded-xl p-6 w-full max-w-xl">
    <p className="text-gray-400 text-sm mb-1">Current Price</p>
    <p className="text-4xl font-bold text-green-400">{result.price}</p>
    <p className="text-gray-500 text-sm mt-2">Status: {result.status}</p>
  </div>
)}
{history.length > 1 && (
  <div className="mt-8 bg-gray-800 rounded-xl p-6 w-full max-w-xl">
    <p className="text-gray-400 text-sm mb-4">Price History</p>
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={history
        .filter(h => h.price !== null)
        .map(h => ({
          price: parseFloat(h.price.replace("$", "")),
          date: new Date(h.scraped_at).toLocaleDateString()
        }))}>
        <XAxis dataKey="date" stroke="#6b7280" />
        <YAxis stroke="#6b7280" />
        <Tooltip />
        <Line type="monotone" dataKey="price" stroke="#34d399" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  </div>
)}
    </main>
);

}
