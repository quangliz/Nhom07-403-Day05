import { create } from "zustand";

interface Order {
  id: string;
  status: "new" | "preparing" | "ready" | "completed";
}

interface MerchantOrderState {
  orders: Order[];
  setOrders: (orders: Order[]) => void;
}

export const useMerchantOrderStore = create<MerchantOrderState>((set) => ({
  orders: [],
  setOrders: (orders) => set({ orders }),
}));
