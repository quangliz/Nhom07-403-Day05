"use client";

/**
 * Merchant List Screen
 * Displays all available merchants from the mock data.
 * Aligned with backend GET /merchants contract.
 */
import Link from "next/link";
import merchantsData from "@/data/merchants.json";
import type { Merchant } from "@/types";

export default function MerchantListPage() {
  const merchants = merchantsData as Merchant[];

  const categories = [
    { name: "Bún - Phở - Mỳ", icon: "🍜" },
    { name: "Cơm - Xôi", icon: "🍱" },
    { name: "Đồ Ăn Nhanh", icon: "🍟" },
    { name: "Trà Sữa - Cà Phê", icon: "🧋" },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* App Header - Fixed centered - XanhSM Gradient */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-[480px] z-50">
        <header className="bg-brand bg-brand-gradient text-white p-5 pb-10 rounded-b-[32px] shadow-lg">
          <div className="flex items-center gap-2 mb-6">
            <svg className="w-5 h-5 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
            </svg>
            <div className="flex-1">
              <p className="text-[10px] text-white/70 font-bold uppercase tracking-widest">Giao đến:</p>
              <h1 className="text-sm font-bold truncate">Cổng Phụ - Trường Đại Học VinUni</h1>
            </div>
            <div className="flex gap-3">
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" /></svg>
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20"><path d="M3 3a1 1 0 000 2h11a1 1 0 100-2H3zM3 7a1 1 0 000 2h5a1 1 0 000-2H3zM3 11a1 1 0 100 2h4a1 1 0 100-2H3zM13 16a1 1 0 102 0v-5.586l1.293 1.293a1 1 0 001.414-1.414l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 101.414 1.414L13 10.414V16z" /></svg>
            </div>
          </div>

          {/* Search Bar Placeholder */}
          <div className="bg-white rounded-full p-3.5 shadow-inner flex items-center gap-3 text-slate-400">
            <svg className="w-5 h-5 text-brand" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <span className="text-sm font-medium">Phúc Long - Mua 1 Tặng 1 Chỉ 60K</span>
          </div>
        </header>
      </div>

      {/* Main Content Area */}
      <div className="pt-48 flex-1 overflow-y-auto">
        {/* Promo Slider Placeholder */}
        <div className="px-5 mb-8">
          <div className="bg-brand-light rounded-[32px] p-1 overflow-hidden shadow-sm relative aspect-[21/9] flex flex-col justify-center items-center text-center">
             <div className="absolute inset-0 bg-brand/5 animate-pulse" />
             <h3 className="text-brand font-black text-2xl relative z-10 italic">MUA 1 TẶNG 1</h3>
             <p className="text-brand-dark font-bold text-sm relative z-10">Voucher giảm -50% & Freeship</p>
             <div className="mt-2 bg-brand text-white text-[10px] font-black px-4 py-1 rounded-full relative z-10">NHẬN NGAY</div>
          </div>
        </div>

        {/* Category Grid */}
        <div className="grid grid-cols-4 px-5 gap-y-6 mb-10 text-center">
          {categories.map((cat, i) => (
            <div key={i} className="flex flex-col items-center gap-2">
              <div className="w-14 h-14 bg-slate-50 rounded-2xl flex items-center justify-center text-2xl shadow-sm border border-slate-100 hover:scale-110 transition-transform">
                {cat.icon}
              </div>
              <span className="text-[10px] font-black text-slate-600 leading-tight px-1 uppercase tracking-tight">
                {cat.name}
              </span>
            </div>
          ))}
        </div>

        {/* Section Title */}
        <div className="px-5 mb-4 flex items-center justify-between">
          <h2 className="text-lg font-black text-slate-800 tracking-tight flex items-center gap-2 uppercase italic">
            <span className="w-1 h-5 bg-brand rounded-full" />
            Quán Ngon Gần Bạn
          </h2>
          <span className="text-brand text-xs font-bold px-3 py-1 bg-brand-light rounded-full">Xem thêm</span>
        </div>

        {/* Merchant List */}
        <div className="px-5 pb-24 flex flex-col gap-6">
          {merchants.map((merchant) => (
            <Link
              key={merchant.id}
              href={`/merchant/${merchant.id}`}
              className="bg-white rounded-[32px] p-5 shadow-[0_4px_25px_rgba(0,0,0,0.04)] border border-slate-50 hover:shadow-md transition-all active:scale-[0.98] group"
            >
              <div className="flex justify-between items-start mb-3">
                <h2 className="text-xl font-black text-slate-800 group-hover:text-brand transition-colors tracking-tight">
                  {merchant.name}
                </h2>
                <div className="flex items-center gap-1.5">
                   <span className="text-xs font-bold text-slate-400 flex items-center">
                     <svg className="w-3.5 h-3.5 text-yellow-400 mr-0.5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
                     4.9
                   </span>
                   <span className="text-slate-200">|</span>
                   <span className="bg-brand-light text-brand-dark text-[10px] font-black px-2.5 py-1 rounded-full uppercase tracking-wider">
                     {merchant.items.length} món
                   </span>
                </div>
              </div>
              
              <p className="text-slate-500 text-sm leading-relaxed line-clamp-2 italic mb-4 opacity-75">
                "{merchant.description.split(':').pop()?.trim()}"
              </p>

              <div className="flex items-center justify-between pt-4 border-t border-slate-50">
                <div className="flex items-center text-brand font-black text-xs tracking-widest uppercase">
                  XEM THỰC ĐƠN
                  <svg 
                    className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" 
                    fill="none" 
                    stroke="currentColor" 
                    viewBox="0 0 24 24"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
                <div className="text-[9px] font-black text-slate-400 uppercase tracking-widest opacity-80">
                  15-25 min • 2.4 km
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
