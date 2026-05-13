"use client";

import { useState } from "react";

export default function Home() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState<null | {price: string; status: string} > (null);
  const [loading, setLoading] = useState(false);

  const scrape = async () => {
      setLoading(true);
      const response = await fetch(`http://localhost:8000/scrape?url=${encodeURIComponent(url)}`);
      const data = await response.json();
      setResult(data);
      setLoading(false);
  };

  return (
    <main className="min-h-screen bg-grey-950 text-white flex flex-col items-center justify-center p-8">
      <h1 className="text-4x1 font-bold mb-2">🔔 Price Tracker</h1>
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
    </main>
);

}
