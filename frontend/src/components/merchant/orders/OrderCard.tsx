/**
 * Order card component — compact summary row for the orders list.
 */
"use client";
import Link from "next/link";
import type { MerchantOrder } from "@/types";
import { formatCurrency } from "@/lib/format";

interface Props {
  order: MerchantOrder;
  onAccept?: (id: string) => void;
}

const STATUS_BADGE: Record<string, { label: string; color: string }> = {
  new: { label: "Đơn mới", color: "bg-orange-100 text-orange-600" },
  confirmed: { label: "Đã xác nhận", color: "bg-blue-100 text-blue-600" },
  history_done: { label: "Hoàn thành", color: "bg-green-100 text-green-700" },
  history_cancelled: { label: "Đã huỷ", color: "bg-gray-100 text-gray-500" },
};

export default function OrderCard({ order, onAccept }: Props) {
  const badge = STATUS_BADGE[order.status] ?? STATUS_BADGE.new;

  return (
    <Link href={`/merchant/orders/${order.id}`} className="block bg-white rounded-xl shadow-sm p-4 active:opacity-70">
      <div className="flex items-start justify-between gap-2">
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-semibold text-gray-800">#{order.code}</span>
            <span className={`text-xs font-medium px-2 py-0.5 rounded-full ${badge.color}`}>
              {badge.label}
            </span>
          </div>
          <p className="text-xs text-gray-400 mt-0.5">{order.time} · {order.date}</p>
        </div>
        <p className="text-sm font-bold text-teal-600 shrink-0">{formatCurrency(order.total)}</p>
      </div>

      <p className="mt-1.5 text-xs text-gray-500">
        {order.itemCount} món · {order.customer.name}
        {order.driverAssigned && (
          <span className="ml-2 text-green-600 font-medium">Đã có tài xế</span>
        )}
      </p>

      {/* Quick accept button for new orders */}
      {order.status === "new" && onAccept && (
        <button
          onClick={(e) => {
            e.preventDefault();
            onAccept(order.id);
          }}
          className="mt-3 w-full bg-teal-400 hover:bg-teal-500 text-white text-xs font-semibold py-2 rounded-lg transition-colors"
        >
          Xác nhận đơn
        </button>
      )}
    </Link>
  );
}
