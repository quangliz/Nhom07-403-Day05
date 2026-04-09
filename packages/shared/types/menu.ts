// ⚠️  FILE NÀY LÀ CONTRACT CHUNG — chỉ sửa qua PR + review
// Owner: Team Lead

export interface MenuItem {
  id: string;
  store_id: string;
  name: string;
  price: number;                    // VND
  category: string;                 // "cơm" | "bún" | "mì" | ...
  description: string;
  allergens: string[] | null;       // null = chưa có data từ merchant
  ingredients: string[] | null;     // null = chưa có data
  is_available: boolean;
  image_url: string;
  spicy_level: 0 | 1 | 2 | 3;     // 0=không cay, 3=rất cay
  updated_at: string;               // ISO 8601
}

export interface MenuStore {
  store_id: string;
  store_name: string;
  phone: string;
  address: string;
  items: MenuItem[];
}
