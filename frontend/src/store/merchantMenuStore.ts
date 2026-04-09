import { create } from "zustand";
import type { MerchantItemStatus } from "@/types";

interface MerchantMenuState {
  setItemStatus: (categoryId: string, itemId: string, status: MerchantItemStatus) => void;
  deleteItem: (categoryId: string, itemId: string) => void;
}

export const useMerchantMenuStore = create<MerchantMenuState>(() => ({
  setItemStatus: () => {},
  deleteItem: () => {},
}));
