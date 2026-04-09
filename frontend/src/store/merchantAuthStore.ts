import { create } from "zustand";

interface MerchantAuthState {
  isLoggedIn: boolean;
  phone: string | null;
  login: (phone: string) => void;
  logout: () => void;
}

export const useMerchantAuthStore = create<MerchantAuthState>((set) => ({
  isLoggedIn: false,
  phone: null,
  login: (phone) => set({ isLoggedIn: true, phone }),
  logout: () => set({ isLoggedIn: false, phone: null }),
}));
