/**
 * Service grid on merchant home — shows the 6 quick-access tiles:
 * Orders, Menu, Opening Hours, Wallet, Store Status, Rate.
 */
"use client";
import Link from "next/link";
import { useMerchantOrderStore } from "@/store/merchantOrderStore";

const SERVICES = [
  {
    href: "/merchant/orders",
    bg: "bg-orange-50",
    iconBg: "bg-orange-400",
    label: "Đơn hàng",
    icon: (
      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
    ),
  },
  {
    href: "/merchant/menu",
    bg: "bg-green-50",
    iconBg: "bg-green-500",
    label: "Thực đơn",
    icon: (
      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
      </svg>
    ),
  },
  {
    href: "/merchant/hours",
    bg: "bg-blue-50",
    iconBg: "bg-blue-500",
    label: "Giờ mở cửa",
    icon: (
      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    href: "/merchant/wallet",
    bg: "bg-purple-50",
    iconBg: "bg-purple-500",
    label: "Ví cửa hàng",
    icon: (
      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
      </svg>
    ),
  },
  {
    href: "#",
    bg: "bg-yellow-50",
    iconBg: "bg-yellow-400",
    label: "Tỷ lệ",
    icon: (
      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
  },
  {
    href: "#",
    bg: "bg-teal-50",
    iconBg: "bg-teal-400",
    label: "Đánh giá",
    icon: (
      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
      </svg>
    ),
  },
];

export default function ServiceGrid() {
  const orders = useMerchantOrderStore((s) => s.orders);
  const newCount = orders.filter((o) => o.status === "new").length;

  return (
    <div className="grid grid-cols-3 gap-3 p-4">
      {SERVICES.map((svc) => (
        <Link
          key={svc.label}
          href={svc.href}
          className={`relative flex flex-col items-center gap-2 rounded-xl p-3 ${svc.bg} active:opacity-70 transition-opacity`}
        >
          {/* Badge for new orders */}
          {svc.label === "Đơn hàng" && newCount > 0 && (
            <span className="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold rounded-full min-w-[18px] h-[18px] flex items-center justify-center px-1">
              {newCount}
            </span>
          )}
          <div className={`w-11 h-11 rounded-xl flex items-center justify-center ${svc.iconBg}`}>
            {svc.icon}
          </div>
          <span className="text-xs font-medium text-gray-700 text-center leading-tight">{svc.label}</span>
        </Link>
      ))}
    </div>
  );
}
