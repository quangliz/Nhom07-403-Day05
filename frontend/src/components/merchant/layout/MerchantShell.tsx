/**
 * Client-side auth guard for the merchant section.
 * Wraps the main shell: MerchantHeader + MerchantSidebar + MerchantBottomNav.
 * Redirects to /merchant/login if not logged in.
 */
"use client";
import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useMerchantAuthStore } from "@/store/merchantAuthStore";
import MerchantHeader from "@/components/merchant/layout/MerchantHeader";
import MerchantSidebar from "@/components/merchant/layout/MerchantSidebar";
import MerchantBottomNav from "@/components/merchant/layout/MerchantBottomNav";

export default function MerchantShell({ children }: { children: React.ReactNode }) {
  const isLoggedIn = useMerchantAuthStore((s) => s.isLoggedIn);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoggedIn && pathname !== "/merchant/login") {
      router.replace("/merchant/login");
    }
  }, [isLoggedIn, pathname, router]);

  // Show nothing while redirecting
  if (!isLoggedIn && pathname !== "/merchant/login") return null;

  // Do not show shell on the login page
  if (pathname === "/merchant/login") return <>{children}</>;

  return (
    <div className="min-h-screen bg-gray-50">
      <MerchantHeader />
      <MerchantSidebar />
      {/* Content area — offset for header (pt-14) and bottom nav (pb-20) on mobile; sidebar on desktop */}
      <main className="pt-14 pb-20 lg:pb-0 lg:pl-64">
        <div className="max-w-lg mx-auto lg:max-w-none">
          {children}
        </div>
      </main>
      <MerchantBottomNav />
    </div>
  );
}
