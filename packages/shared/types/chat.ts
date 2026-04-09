// ⚠️  FILE NÀY LÀ CONTRACT CHUNG — chỉ sửa qua PR + review
// Owner: Team Lead

export interface ChatRequest {
  session_id: string;
  user_id: string;
  message: string;
  store_id: string;
  context?: {
    current_cart: MenuItem[];
  };
}

export type Confidence = "high" | "low" | "unsure";

export interface MenuCard {
  item_id: string;
  name: string;
  price: number;
  image_url: string;
  tags: string[];          // ["Không cay", "Còn hàng"]
  is_available: boolean;
}

export interface ActionButton {
  label: string;
  action: "add_to_cart" | "report_wrong" | "call_store";
  payload?: Record<string, unknown>;
}

export interface ChatResponse {
  log_id: string;          // Dùng để Evaluation track outcome
  message: string;
  confidence: Confidence;
  disclaimer?: string;     // Bắt buộc với câu allergen
  cards?: MenuCard[];
  action_buttons?: ActionButton[];
}

// Re-export để dùng trong ChatRequest.context
import type { MenuItem } from "./menu";
export type { MenuItem };
