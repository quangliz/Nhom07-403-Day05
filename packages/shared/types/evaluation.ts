// ⚠️  FILE NÀY LÀ CONTRACT CHUNG — chỉ sửa qua PR + review
// Owner: Evaluation Team

import type { Confidence } from "./chat";

export interface EvalLog {
  log_id: string;
  session_id: string;
  user_id: string;
  store_id: string;
  timestamp: string;              // ISO 8601
  query: string;
  intent: string;                 // "menu_query" | "recommendation" | "out_of_scope"
  tools_called: string[];
  response_text: string;
  confidence: Confidence;
  latency_ms: number;
  outcome?: OutcomeType;          // Ghi sau khi user action
}

export type OutcomeType = "converted" | "reported_wrong" | "ignored";

export interface EvalOutcome {
  log_id: string;
  outcome: OutcomeType;
}

export interface EvalCorrection {
  log_id: string;
  item_id: string;
  reason: string;                 // "wrong_allergen" | "wrong_price" | "out_of_stock" | "other"
  user_note?: string;
}
