/**
 * Transaction row component for the wallet history list.
 */
import Link from "next/link";
import type { WalletTransaction } from "@/types";
import { formatCurrency } from "@/lib/format";

interface Props {
  tx: WalletTransaction;
}

export default function TransactionRow({ tx }: Props) {
  const isDone = tx.status === "done";
  return (
    <Link href={`/merchant/wallet/history/${tx.id}`} className="flex items-center gap-3 px-4 py-3 bg-white hover:bg-gray-50 active:bg-gray-100 transition-colors">
      {/* Icon */}
      <div className={`w-10 h-10 rounded-full flex items-center justify-center shrink-0 ${isDone ? "bg-teal-100" : "bg-gray-100"}`}>
        <svg className={`w-5 h-5 ${isDone ? "text-teal-500" : "text-gray-400"}`} fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      {/* Details */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-gray-800 truncate">Rút tiền về tài khoản</p>
        <p className="text-xs text-gray-400 mt-0.5">{tx.date}</p>
      </div>
      {/* Amount + status */}
      <div className="text-right shrink-0">
        <p className={`text-sm font-bold ${isDone ? "text-teal-600" : "text-gray-400 line-through"}`}>
          -{formatCurrency(tx.amount)}
        </p>
        <p className={`text-xs font-medium ${isDone ? "text-green-600" : "text-red-400"}`}>
          {isDone ? "Thành công" : "Đã huỷ"}
        </p>
      </div>
    </Link>
  );
}
