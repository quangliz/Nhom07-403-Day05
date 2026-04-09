// Types aligned with backend API: GET /merchants
// Mirrors the JSON schema from data/mock/menus/store_001.json

export interface FAQ {
  question: string;
  answer: string;
}

export interface MenuItem {
  id: string;
  name: string;
  price: number;
  description: string | null;
  ingredients: string[];
  is_avaiable: boolean;  // Note: matches backend typo intentionally
  quantity: number;
}

export interface Merchant {
  id: string;           // e.g. "M001"
  name: string;
  description: string;
  faqs: FAQ[];
  items: MenuItem[];
}

// Merchant menu item (used by merchant dashboard components)
export type MerchantItemStatus = "available" | "stopped_today" | "suspended";

export interface MerchantItem {
  id: string;
  name: string;
  price: number;
  description?: string;
  image?: string;
  status: MerchantItemStatus;
}

// POST /chat request/response
export interface ChatRequest {
  merchant_id: string;
  message: string;
  session_id?: string;
}

export interface ActionButton {
  label: string;
  action: string;
  payload?: Record<string, unknown>;
}

export interface ChatResponse {
  log_id: string;
  message: string;
  merchant_name: string;
  confidence: string;
  action_buttons?: ActionButton[];
  latency_ms: number;
  total_tokens: number;
  tool_debug_info?: { name: string; args: any; output: string }[];
}
