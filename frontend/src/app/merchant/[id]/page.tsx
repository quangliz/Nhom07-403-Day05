"use client";

/**
 * Merchant Detail & Menu Screen
 * Displays a single merchant and their categorized items.
 * Includes a "Chat with AI" FAB pre-wired for future backend integration.
 */
import { use, useState, useEffect } from "react";
import Link from "next/link";
import merchantsData from "@/data/merchants.json";
import type { Merchant, MenuItem } from "@/types";
import ChatInterface from "@/components/merchant/ChatInterface";

export default function MerchantDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("XÔI NGON");
  const [scrolled, setScrolled] = useState(false);
  const merchant = (merchantsData as Merchant[]).find((m) => m.id === id);

  // Track scroll for sticky header transitions
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 150);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  if (!merchant) {
    return (
      <div className="p-10 text-center">
        <h1 className="text-xl font-extrabold uppercase italic text-slate-800">Không tìm thấy quán</h1>
        <Link href="/" className="text-brand font-black underline mt-4 block uppercase text-xs tracking-widest">Quay lại trang chủ</Link>
      </div>
    );
  }

  const categories = ["XÔI NGON", "NƯỚC ÉP + TRÀ SỮA", "MATCHA LATTE"];

  return (
    <div className="flex flex-col min-h-screen bg-white pb-20">
      {/* Dynamic Header - Fixed to app container */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-full max-w-[480px] z-[50] pointer-events-none">
        <div className={`p-4 flex items-center justify-between transition-all duration-300 pointer-events-auto ${
          scrolled ? "bg-white shadow-md py-3" : "bg-transparent"
        }`}>
          {/* Back Button */}
          <Link href="/" className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
            scrolled ? "text-slate-800 hover:bg-slate-100" : "bg-black/30 backdrop-blur-md text-white border border-white/10"
          }`}>
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M15 19l-7-7 7-7" /></svg>
          </Link>

          {/* Search Bar / Action Buttons */}
          <div className="flex-1 px-3">
            {scrolled ? (
              <div className="bg-slate-100 rounded-full px-4 py-2 flex items-center gap-2 animate-in fade-in slide-in-from-right-4 duration-300">
                <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                <span className="text-xs text-slate-400 font-bold truncate">Tìm kiếm tại {merchant.name}...</span>
              </div>
            ) : null}
          </div>

          <div className="flex gap-2">
            {!scrolled && (
              <>
                <button className="w-10 h-10 bg-black/30 backdrop-blur-md rounded-full flex items-center justify-center text-white border border-white/10">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" /></svg>
                </button>
                <button className="w-10 h-10 bg-black/30 backdrop-blur-md rounded-full flex items-center justify-center text-white border border-white/10">
                  <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" /></svg>
                </button>
              </>
            )}
            <button className={`w-10 h-10 rounded-full flex items-center justify-center transition-all ${
              scrolled ? "text-slate-800" : "bg-black/30 backdrop-blur-md text-white border border-white/10"
            }`}>
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </button>
          </div>
        </div>
      </div>

      {/* Hero Header Section */}
      <div className="relative h-60 w-full overflow-hidden">
        {/* Banner Image Placeholder */}
        <div className="absolute inset-0 bg-slate-200">
           <div className="absolute inset-0 bg-gradient-to-b from-black/40 via-transparent to-black/20" />
           <div className="w-full h-full flex items-center justify-center">
              <svg className="w-20 h-20 text-white/50" fill="currentColor" viewBox="0 0 24 24">
                <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c0 1.1.9 2 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" />
              </svg>
           </div>
        </div>
      </div>

      {/* Merchant Info Area */}
      <div className="px-5 -mt-6 relative z-10">
        <div className="bg-white rounded-t-[32px] pt-6 pb-4">
           {/* Partner Badge */}
           <div className="flex items-center gap-1.5 mb-2">
              <div className="bg-brand text-white text-[9px] font-black px-2 py-1 rounded-md flex items-center gap-1">
                 <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" /></svg>
                 XanhPartner
              </div>
           </div>

           {/* Name */}
           <h1 className="text-2xl font-black text-slate-800 tracking-tight leading-tight mb-4">
              {merchant.name} - Xôi, Mỳ Cay & Nem Nướng Nha Trang - Trâu Quỳ
           </h1>

           {/* Quick Stats Grid */}
           <div className="flex items-center gap-4 text-xs font-bold text-slate-400 mb-6 overflow-x-auto scrollbar-hide">
              <div className="flex items-center gap-1 shrink-0">
                 <svg className="w-4 h-4 text-yellow-500" fill="currentColor" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" /></svg>
                 <span className="text-slate-800">4.5</span> (26)
              </div>
              <div className="flex items-center gap-1 shrink-0">
                 <div className="w-4 h-4 bg-red-500 rounded-full flex items-center justify-center text-[7px] text-white">G</div>
                 <span className="text-slate-800">5</span> (2)
              </div>
              <div className="flex items-center gap-1 shrink-0">
                 <svg className="w-4 h-4 text-orange-400" fill="currentColor" viewBox="0 0 20 20"><path d="M3 1a1 1 0 000 2h1.22l.305 1.222a.997.997 0 00.01.042l1.358 5.43-.893.892C3.74 11.846 4.632 14 6.414 14H15a1 1 0 000-2H6.414l1-1H14a1 1 0 00.894-.553l3-6A1 1 0 0017 3H6.28l-.31-1.243A1 1 0 005 1H3z" /></svg>
                 <span className="text-slate-800">500+</span>
              </div>
              <div className="flex items-center gap-1 shrink-0">
                 <svg className="w-4 h-4 text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                 <span className="text-slate-800">3.0 km</span>
              </div>
              <svg className="w-4 h-4 ml-auto text-slate-300" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M9 5l7 7-7 7" /></svg>
           </div>

           {/* Voucher Section */}
           <div className="flex gap-3 overflow-x-auto scrollbar-hide mb-8">
              <div className="flex-none w-[180px] bg-brand-light/50 border border-brand/20 rounded-2xl p-3 flex items-start gap-3 relative overflow-hidden">
                 <div className="absolute right-[-10px] top-[-10px] w-12 h-12 bg-brand/10 rounded-full" />
                 <div className="w-10 h-10 bg-white rounded-xl shadow-sm flex items-center justify-center shrink-0">
                    <svg className="w-6 h-6 text-brand" fill="currentColor" viewBox="0 0 20 20"><path d="M4 3a2 2 0 100 4h12a2 2 0 100-4H4z" /><path fillRule="evenodd" d="M3 8h14v7a2 2 0 01-2 2H5a2 2 0 01-2-2V8zm5 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" clipRule="evenodd" /></svg>
                 </div>
                 <div>
                    <span className="text-[8px] bg-brand text-white font-black px-1.5 py-0.5 rounded-full uppercase">Phí giao hàng</span>
                    <p className="text-xs font-black text-slate-700 mt-1">Đến 100.000đ</p>
                 </div>
              </div>
              <div className="flex-none w-[180px] bg-orange-50 border border-orange-200 rounded-2xl p-3 flex items-start gap-3 relative overflow-hidden">
                 <div className="absolute right-[-10px] top-[-10px] w-12 h-12 bg-orange-200/20 rounded-full" />
                 <div className="w-10 h-10 bg-white rounded-xl shadow-sm flex items-center justify-center shrink-0">
                    <svg className="w-6 h-6 text-orange-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732l-3.354 1.935-1.18 4.455a1 1 0 01-1.933 0L9.854 12.8 6.5 10.866a1 1 0 010-1.732l3.354-1.935 1.18-4.455A1 1 0 0112 2z" clipRule="evenodd" /></svg>
                 </div>
                 <div>
                    <span className="text-[8px] bg-orange-400 text-white font-black px-1.5 py-0.5 rounded-full uppercase">Giá món</span>
                    <p className="text-xs font-black text-slate-700 mt-1">Đến 100.000đ</p>
                 </div>
              </div>
           </div>
        </div>
      </div>

      {/* Category Tabs - Sticky */}
      <div className="sticky top-0 z-[40] bg-white border-b border-slate-100 px-5 flex gap-8 overflow-x-auto scrollbar-hide py-3">
         {categories.map((cat) => (
           <button 
             key={cat}
             onClick={() => setActiveTab(cat)}
             className={`shrink-0 text-[11px] font-black uppercase tracking-wider transition-all relative py-2 ${
               activeTab === cat ? "text-slate-800" : "text-slate-400"
             }`}
           >
             {cat}
             {activeTab === cat && (
               <div className="absolute bottom-0 left-0 right-0 h-1 bg-brand rounded-full" />
             )}
           </button>
         ))}
      </div>

      {/* Item Groups */}
      <div className="px-5 pt-8 space-y-10 group">
         <div>
            <h2 className="text-xl font-black text-slate-800 uppercase italic tracking-tight mb-8">
               {activeTab}
            </h2>
            
            <div className="space-y-10">
               {merchant.items.map((item: MenuItem) => (
                 <div key={item.id} className="flex gap-5 items-start">
                    {/* Large Item Image */}
                    <div className="w-32 h-32 bg-slate-100 rounded-3xl shrink-0 overflow-hidden border border-slate-100 relative shadow-sm">
                       <svg className="w-12 h-12 text-slate-300 absolute inset-0 m-auto" fill="currentColor" viewBox="0 0 24 24"><path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c0 1.1.9 2 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" /></svg>
                    </div>

                    {/* Item Info */}
                    <div className="flex-1 min-h-[128px] flex flex-col justify-between py-1 relative">
                       <div>
                          <h3 className="text-lg font-black text-slate-800 leading-tight mb-1.5">{item.name}</h3>
                          {item.description && (
                             <p className="text-xs text-slate-400 font-medium line-clamp-2 leading-relaxed opacity-70">
                                {item.description}
                             </p>
                          )}
                       </div>
                       
                       <div className="flex items-center justify-between mt-4">
                          <div className="text-slate-800 font-extrabold text-lg tracking-tight">
                             {item.price.toLocaleString('vi-VN')} đ
                          </div>
                          <button className="w-10 h-10 bg-brand text-white rounded-full flex items-center justify-center shadow-lg shadow-brand/20 active:scale-90 transition-all border-2 border-white">
                             <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>
                          </button>
                       </div>
                    </div>
                 </div>
               ))}
            </div>
         </div>
      </div>

      {/* Chat FAB (Floating Action Button) - Fixed centered to stay inside the 480px frame while scrolling */}
      {!isChatOpen && (
        <div className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[480px] h-0 z-50 pointer-events-none">
          <button 
            className="absolute bottom-8 right-8 w-14 h-14 bg-brand text-white rounded-full shadow-[0_8px_30px_rgb(45,204,210,0.4)] flex items-center justify-center hover:scale-110 active:scale-95 transition-all pointer-events-auto border-2 border-white"
            onClick={() => setIsChatOpen(true)}
          >
            <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
            <span className="absolute -top-1 -right-1 flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-light opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
            </span>
          </button>
        </div>
      )}

      {/* Chat Overlay */}
      {isChatOpen && (
        <ChatInterface 
          merchantId={merchant.id} 
          merchantName={merchant.name} 
          onClose={() => setIsChatOpen(false)} 
        />
      )}
    </div>
  );
}
