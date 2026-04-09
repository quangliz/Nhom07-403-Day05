"use client";

import { useState, useRef, useEffect } from "react";
import type { ChatResponse, ActionButton } from "@/types";
import { post } from "@/lib/api";

interface Message {
  role: "user" | "ai";
  content: string;
  logId?: string;
  actionButtons?: ActionButton[];
  latencyMs?: number;
  totalTokens?: number;
  toolDebugInfo?: { name: string; args: any; output: string }[];
}

interface ChatInterfaceProps {
  merchantId: string;
  merchantName: string;
  onClose: () => void;
}

/**
 * Lightweight Markdown-style formatter for AI messages.
 * Handles **bold**, *italics*, and line breaks.
 */
function MessageContent({ content, role }: { content: string; role: "user" | "ai" }) {
  const lines = content.split('\n');

  // Regex for bold (**text**), italics (*text*), and links (http://...)
  // We use a non-capturing group (?:...) for alternatives
  const mdRegex = /(\*\*.*?\*\*|\*.*?\*|https?:\/\/[^\s]+)/g;

  return (
    <div className={`space-y-1.5 whitespace-pre-wrap ${role === "user" ? "text-white" : "text-slate-800"}`}>
      {lines.map((line, i) => {
        const parts = line.split(mdRegex).filter(Boolean);

        return (
          <p key={i}>
            {parts.map((part, j) => {
              if (part.startsWith('**') && part.endsWith('**')) {
                return <strong key={j} className="font-extrabold text-brand-dark">{part.slice(2, -2)}</strong>;
              }
              if (part.startsWith('*') && part.endsWith('*')) {
                return <em key={j} className="italic text-slate-600">{part.slice(1, -1)}</em>;
              }
              if (part.startsWith('http')) {
                return <a key={j} href={part} target="_blank" rel="noopener noreferrer" className="underline text-blue-600 hover:text-blue-800">{part}</a>;
              }
              return <span key={j}>{part}</span>;
            })}
          </p>
        );
      })}
    </div>
  );
}

export default function ChatInterface({
  merchantId,
  merchantName,
  onClose,
}: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const [feedbackState, setFeedbackState] = useState<Record<string, string>>({});
  const [expandedDebug, setExpandedDebug] = useState<Record<string, boolean>>({});

  // Auto-scroll to bottom
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const data = await post<ChatResponse>("/chat", {
        merchant_id: merchantId,
        message: userMessage,
        session_id: "session_" + merchantId,
      });
      setMessages((prev) => [...prev, { 
        role: "ai", 
        content: data.message,
        logId: data.log_id,
        actionButtons: data.action_buttons,
        latencyMs: data.latency_ms,
        totalTokens: data.total_tokens,
        toolDebugInfo: data.tool_debug_info
      }]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "ai", content: "Xin lỗi, tôi đang gặp chút sự cố kết nối. Bạn vui lòng thử lại sau nhé!" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAction = async (button: ActionButton, logId?: string) => {
    if (!logId || feedbackState[logId]) return;

    let signalType = "";
    if (button.action === "like") signalType = "positive";
    else if (button.action === "dislike") signalType = "explicit_negative";
    else signalType = "implicit_negative";

    setFeedbackState((prev) => ({ ...prev, [logId]: button.action }));

    try {
      await post("/feedback", {
        log_id: logId,
        merchant_id: merchantId,
        signal_type: signalType,
        details: `User clicked ${button.label}`,
      });
    } catch (error) {
      console.error("Feedback error:", error);
      setFeedbackState((prev) => {
        const next = { ...prev };
        delete next[logId];
        return next;
      });
    }
  };

  const toggleDebug = (logId: string) => {
    setExpandedDebug((prev) => ({ ...prev, [logId]: !prev[logId] }));
  };

  const [isClosing, setIsClosing] = useState(false);

  const handleClose = () => {
    setIsClosing(true);
    setTimeout(() => onClose(), 300);
  };

  return (
    <div className={`fixed inset-y-0 inset-x-0 mx-auto w-full max-w-[480px] z-[60] flex flex-col bg-white shadow-2xl ${isClosing ? "chat-exit" : "chat-enter"}`}>
      {/* Header */}
      <header className="bg-brand bg-brand-gradient text-white p-4 flex items-center justify-between shadow-md">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center overflow-hidden border-2 border-white/20">
            <span className="text-brand font-black italic tracking-tighter text-lg">AI</span>
          </div>
          <div>
            <h2 className="text-xs font-black leading-tight uppercase tracking-tight italic">Trợ lý {merchantName}</h2>
            <div className="flex items-center gap-1">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
              <span className="text-[9px] text-white/80 uppercase font-black tracking-widest">Đang trực tuyến</span>
            </div>
          </div>
        </div>
        <button 
          onClick={handleClose}
          className="p-2 hover:bg-white/20 rounded-full transition"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </header>

      {/* Message List */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-5 space-y-6 bg-slate-50/50"
      >
        {messages.length === 0 && (
          <div className="text-center py-12">
            <div className="w-20 h-20 bg-brand/5 text-brand rounded-full flex items-center justify-center mx-auto mb-5 shadow-inner">
              <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <p className="text-slate-400 text-xs font-black uppercase tracking-widest px-10 leading-relaxed italic">
              Chào bạn! Tôi có thể giúp gì cho bạn về {merchantName}?
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div 
            key={i} 
            className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"}`}
          >
            <div 
              className={`max-w-[85%] p-4 rounded-[24px] text-sm leading-relaxed shadow-sm ${
                msg.role === "user" 
                  ? "bg-brand bg-brand-gradient rounded-br-none" 
                  : "bg-white rounded-bl-none border border-slate-100"
              }`}
            >
              <MessageContent content={msg.content} role={msg.role} />
            </div>
            
            {/* Render Action Buttons for AI messages */}
            {msg.role === "ai" && msg.actionButtons && msg.actionButtons.length > 0 && !feedbackState[msg.logId || ""] && (
              <div className="mt-2 flex gap-2">
                {msg.actionButtons.map((btn, btnIdx) => (
                  <button
                    key={btnIdx}
                    onClick={() => handleAction(btn, msg.logId)}
                    className="text-base p-1.5 rounded-full border bg-white hover:bg-slate-50 transition-colors"
                  >
                    {btn.label}
                  </button>
                ))}
                {/* Debug Button */}
                {msg.logId && msg.toolDebugInfo && msg.toolDebugInfo.length > 0 && (
                    <button 
                        onClick={() => toggleDebug(msg.logId!)}
                        className="text-xs p-1.5 rounded-full border bg-white hover:bg-slate-50 text-slate-500"
                    >
                        ⚙️
                    </button>
                )}
              </div>
            )}
            
            {/* Display Debug Info */}
            {msg.logId && expandedDebug[msg.logId] && msg.toolDebugInfo && (
                <div className="mt-2 p-3 bg-slate-800 text-white text-[10px] rounded-lg w-full max-w-[85%] overflow-x-auto font-mono">
                    <p className="font-bold mb-1 underline">Tools Used:</p>
                    {msg.toolDebugInfo.map((tool, idx) => (
                        <div key={idx} className="mb-3">
                            <p className="text-blue-300 font-bold">[{tool.name}]</p>
                            <p className="text-slate-300">Args: {JSON.stringify(tool.args)}</p>
                            <p className="text-green-300 break-words">Output: {tool.output}</p>
                        </div>
                    ))}
                </div>
            )}
            
            {/* Display Latency & Token Usage */}
            {msg.role === "ai" && msg.latencyMs !== undefined && (
                <div className="mt-1 text-[10px] text-slate-400 font-mono">
                    {msg.latencyMs}ms • {msg.totalTokens} tokens
                </div>
            )}
            
            {/* Optional: Show feedback summary after click */}
            {msg.role === "ai" && feedbackState[msg.logId || ""] && (
                <div className="mt-2 text-xs text-slate-400 italic">
                    Đã ghi nhận phản hồi!
                </div>
            )}
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white p-4 rounded-[24px] rounded-bl-none border border-slate-100 flex gap-1.5 items-center">
              <span className="w-2 h-2 bg-brand/40 rounded-full animate-bounce [animation-delay:-0.3s]" />
              <span className="w-2 h-2 bg-brand/40 rounded-full animate-bounce [animation-delay:-0.15s]" />
              <span className="w-2 h-2 bg-brand/40 rounded-full animate-bounce" />
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-5 bg-white border-t border-slate-50 shadow-[0_-10px_30px_rgba(0,0,0,0.03)]">
        <div className="flex items-center gap-2 bg-slate-50 rounded-[24px] px-5 py-3 border border-slate-100 focus-within:ring-2 focus-within:ring-brand/30 transition-all shadow-inner">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Bạn muốn hỏi gì về quán?"
            className="flex-1 bg-transparent border-none focus:ring-0 text-sm font-medium placeholder:text-slate-300"
          />
          <button 
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className={`p-2 rounded-full transition-all ${
              input.trim() && !isLoading ? "text-brand scale-110" : "text-slate-200"
            }`}
          >
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
