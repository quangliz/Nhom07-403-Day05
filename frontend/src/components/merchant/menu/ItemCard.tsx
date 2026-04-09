/**
 * Menu item card — shows image, name, price, status badge,
 * and a dropdown to change status (available / stopped today / suspended).
 */
"use client";
import { useState } from "react";
import type { MerchantItem, MerchantItemStatus } from "@/types";
import { formatCurrency } from "@/lib/format";
import { useMerchantMenuStore } from "@/store/merchantMenuStore";

interface Props {
  item: MerchantItem;
  categoryId: string;
}

const STATUS_LABELS: Record<MerchantItemStatus, string> = {
  available: "Đang bán",
  stopped_today: "Dừng hôm nay",
  suspended: "Tạm ngưng",
};

const STATUS_COLORS: Record<MerchantItemStatus, string> = {
  available: "bg-green-100 text-green-700",
  stopped_today: "bg-yellow-100 text-yellow-700",
  suspended: "bg-red-100 text-red-600",
};

export default function ItemCard({ item, categoryId }: Props) {
  const [showMenu, setShowMenu] = useState(false);
  const { setItemStatus, deleteItem } = useMerchantMenuStore();

  return (
    <div className={`flex items-center gap-3 p-3 ${item.status !== "available" ? "opacity-60" : ""}`}>
      {/* Thumbnail */}
      <div className="w-14 h-14 rounded-lg overflow-hidden bg-gray-100 shrink-0">
        {item.image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-300">
            <svg className="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
        )}
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-800 truncate">{item.name}</p>
        {item.description && (
          <p className="text-xs text-gray-400 truncate">{item.description}</p>
        )}
        <p className="text-sm font-semibold text-teal-600 mt-0.5">{formatCurrency(item.price)}</p>
      </div>

      {/* Status + menu */}
      <div className="relative shrink-0">
        <button
          onClick={() => setShowMenu((v) => !v)}
          className={`px-2 py-1 rounded-md text-xs font-semibold ${STATUS_COLORS[item.status]}`}
        >
          {STATUS_LABELS[item.status]} ▾
        </button>

        {showMenu && (
          <>
            {/* Overlay */}
            <div
              className="fixed inset-0 z-10"
              onClick={() => setShowMenu(false)}
            />
            <div className="absolute right-0 top-full mt-1 z-20 bg-white border border-gray-200 rounded-xl shadow-lg overflow-hidden min-w-[160px]">
              {(["available", "stopped_today", "suspended"] as MerchantItemStatus[]).map((s) => (
                <button
                  key={s}
                  onClick={() => {
                    setItemStatus(categoryId, item.id, s);
                    setShowMenu(false);
                  }}
                  className={`w-full text-left px-4 py-2.5 text-sm hover:bg-gray-50 ${item.status === s ? "font-semibold text-teal-600" : "text-gray-700"}`}
                >
                  {STATUS_LABELS[s]}
                </button>
              ))}
              <hr className="border-gray-100" />
              <button
                onClick={() => {
                  deleteItem(categoryId, item.id);
                  setShowMenu(false);
                }}
                className="w-full text-left px-4 py-2.5 text-sm text-red-500 hover:bg-red-50"
              >
                Xóa món
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
