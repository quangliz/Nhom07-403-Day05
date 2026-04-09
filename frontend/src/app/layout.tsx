import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FoodieGo - Giao đồ ăn nhanh",
  description: "Ứng dụng đặt đồ ăn trực tuyến - Giao hàng nhanh, ưu đãi hấp dẫn",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="vi" className="h-full">
      <body className="min-h-full antialiased selection:bg-brand/30">
        <main className="app-container max-w-[480px] mx-auto relative overflow-x-hidden">
          {children}
        </main>
      </body>
    </html>
  );
}
