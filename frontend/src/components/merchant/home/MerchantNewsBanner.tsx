/**
 * News banner on the merchant home page — static promotional/announcement card.
 */
export default function MerchantNewsBanner() {
  return (
    <div className="mx-4 mb-4 rounded-xl bg-gradient-to-r from-teal-400 to-teal-500 text-white p-4 flex items-center gap-3">
      <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center shrink-0">
        <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
        </svg>
      </div>
      <div className="min-w-0">
        <p className="text-xs font-semibold opacity-90 uppercase tracking-wide">Thông báo</p>
        <p className="text-sm font-medium leading-snug mt-0.5">
          Tháng 5: Miễn phí chiết khấu với đơn hàng trên 100.000đ
        </p>
      </div>
    </div>
  );
}
