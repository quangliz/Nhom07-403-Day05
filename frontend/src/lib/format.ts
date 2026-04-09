/**
 * Formats a number as Vietnamese currency (e.g. 49000 → "49.000đ")
 */
export function formatVND(amount: number): string {
  return amount.toLocaleString("vi-VN") + "đ";
}

/** Alias for formatVND — used in merchant pages */
export const formatCurrency = formatVND;

/**
 * Returns star display string (e.g. 4.9)
 */
export function formatRating(rating: number): string {
  return rating.toFixed(1);
}
