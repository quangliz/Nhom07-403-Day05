/**
 * Top header bar for merchant pages.
 * Teal background, store name, notification bell.
 */
"use client";
import { useMerchantAuthStore } from "@/store/merchantAuthStore";
import storeData from "@/data/merchant/merchant_store.json";

export default function MerchantHeader() {
  const phone = useMerchantAuthStore((s) => s.phone);

  return (
    <header className="fixed top-0 left-0 right-0 lg:left-64 z-40 bg-teal-400 text-white">
      <div className="flex items-center justify-between px-4 py-3">
        <div className="flex items-center gap-2 min-w-0">
          {/* Checkmark badge */}
          <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center shrink-0">
            <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <div className="min-w-0">
            <p className="text-xs opacity-80 truncate">Chào Quý đối tác{phone ? ` • ${phone}` : ""}</p>
            <div className="flex items-center gap-1">
              <p className="text-sm font-semibold truncate">{storeData.shortName}</p>
              <svg className="w-4 h-4 shrink-0 opacity-80" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
        {/* Bell icon */}
        <button className="w-9 h-9 flex items-center justify-center rounded-full bg-white/10 hover:bg-white/20 transition-colors shrink-0">
          <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        </button>
      </div>
    </header>
  );
}
