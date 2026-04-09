import os
import logging
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from agent.tools import get_faq, list_items, check_stock, create_order, _get_merchant, get_all_merchants

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("agent")

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def get_system_prompt(merchant_id: str) -> str:
    merchant = _get_merchant(merchant_id)
    name = merchant["name"] if merchant else "Unknown Merchant"
    description = merchant["description"] if merchant else "No description available."
    
# 6. BẢO MẬT & DỊ ỨNG: Giữ bí mật nguyên liệu (chỉ trả lời Có/Không) và luôn nhắc nhở về an toàn dị ứng khi tư vấn món.

    return f"""<persona>
Bạn là trợ lý ảo AI chuyên gia của quán ăn {name}. Bạn không chỉ am hiểu thực đơn mà còn là "tổng đài viên" chuyên nghiệp chuyên giải đáp mọi thắc mắc (FAQ) về chính sách, vận chuyển, đóng gói và quy trình của quán. Phong cách nói chuyện của bạn cực kỳ thân thiện, lễ phép (dùng 'dạ', 'vâng', 'ạ') và tràn đầy năng lượng.
</persona>

<rules>
1. Trả lời bằng tiếng Việt.
2. PHẢI ƯU TIÊN FAQ: Khi người dùng hỏi bất kỳ câu hỏi nào về "quy định", "giờ giấc", "đóng gói", "ship", "hâm nóng", hoặc "lưu ý", bạn PHẢI gọi ngay công cụ `get_faq` để có câu trả lời chính xác nhất từ chủ quán.
3. Chuyên nghiệp & Chi tiết: Khi trả lời FAQ, hãy trình bày rõ ràng, có thể dùng bullet points để khách dễ theo dõi.
4. Tuyệt đối không tự bịa ra bất kỳ thông tin mà không có tham chiếu; mọi câu trả lời phải dựa trên dữ liệu từ công cụ.
5. Quy trình suy luận (Thought):
   a. Luôn ưu tiên GỌI TOOL NGAY LẬP TỨC.
   b. Không hỏi lại những gì đã có trong FAQ.
6. LƯU TRỮ THÔNG TIN (MEMORY): Khi người dùng cung cấp thông tin về bản thân (như bị dị ứng, sở thích ăn uống, thói quen), bạn PHẢI lập tức gọi công cụ `save_user_memory` để lưu lại.
</rules>

<tools_instruction>
Bạn có các công cụ sau sử dụng `merchant_id` là "{merchant_id}":
- get_faq: (QUAN TRỌNG NHẤT) Dùng cho mọi câu hỏi về chính sách, đóng gói, giờ mở cửa, lưu ý chung.
- list_items: Dùng để tra cứu thực đơn, giá cả và món ăn, chỉ nên lấy cái trường cần thiết trừ khi người dùng hỏi kỹ hơn.
- check_stock: Kiểm tra hàng trước khi khách chốt đơn.
- create_order: Hỗ trợ khách đặt món.
- save_user_memory: Dùng để lưu lại thông tin quan trọng về sở thích, dị ứng của người dùng.
</tools_instruction>

<response_format>
- Luôn chào hỏi thân thiện ở đầu hội thoại.
- Khi trả lời FAQ: "Dạ, về vấn đề [vấn đề], quán xin được thông tin đến mình như sau: ..."
- Khi giới thiệu món: Trình bày đẹp mắt, dùng icon 🍜🍱🥤 để tăng tính sinh động.
</response_format>

Mô tả / Lưu ý từ quán: {description}
"""

USER_MEMORIES = {}

@tool
def save_user_memory(memory: str, config: RunnableConfig) -> str:
    """Sử dụng công cụ này để lưu thông tin về người dùng (ví dụ: bị dị ứng đậu phộng, thích ăn cay, không ăn hành)."""
    user_id = config.get("configurable", {}).get("user_id", "default_user")
    if user_id not in USER_MEMORIES:
        USER_MEMORIES[user_id] = []
    USER_MEMORIES[user_id].append(memory)
    return f"Đã lưu thông tin: {memory}"

class MerchantAgent:
    def __init__(self, merchant_id: str, checkpointer=None):
        self.merchant_id = merchant_id
        self.checkpointer = checkpointer
        
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.tools = [list_items, get_faq, check_stock, create_order, save_user_memory]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        self.system_prompt_base = get_system_prompt(merchant_id)
        
        self.graph = self._build_graph()

    def _build_graph(self):
        graph_builder = StateGraph(State)
        
        graph_builder.add_node("chatbot", self.chatbot)
        tool_node = ToolNode(tools=self.tools)
        graph_builder.add_node("tools", tool_node)
        
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,
        )
        graph_builder.add_edge("tools", "chatbot")
        
        return graph_builder.compile(checkpointer=self.checkpointer)

    def chatbot(self, state: State, config: RunnableConfig):
        messages = state["messages"]
        user_id = config.get("configurable", {}).get("user_id", "default_user")
        
        memories = USER_MEMORIES.get(user_id, [])
        dynamic_prompt = self.system_prompt_base
        if memories:
            memory_str = "\n".join([f"- {m}" for m in memories])
            dynamic_prompt += f"\n<user_memory>\nNhững thông tin cần nhớ về người dùng:\n{memory_str}\n</user_memory>"
            
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=dynamic_prompt)] + messages
        elif isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=dynamic_prompt)] + messages[1:]
            
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}
        
    def invoke(self, state_input, config=None):
        return self.graph.invoke(state_input, config=config)
        
    def stream(self, state_input, stream_mode="values", config=None):
        return self.graph.stream(state_input, stream_mode=stream_mode, config=config)

def chat_loop():
    merchants = get_all_merchants()
    if not merchants:
        logger.error("Không có dữ liệu quán ăn.")
        return
        
    logger.info("=== CHỌN QUÁN ===")
    for idx, merchant in enumerate(merchants, 1):
        logger.info(f"{idx}. {merchant['name']} (ID: {merchant['id']})")
        
    merchant_choice = None
    while not merchant_choice:
        try:
            choice = input("\nNhập số thứ tự quán (1 - {}): ".format(len(merchants)))
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(merchants):
                merchant_choice = merchants[choice_idx]
            else:
                logger.warning("Lựa chọn không hợp lệ. Vui lòng thử lại.")
        except ValueError:
            logger.error("Vui lòng nhập một số hợp lệ.")
        except EOFError:
            return
            
    merchant_id = merchant_choice['id']

    logger.info("="*50)
    logger.info(f"--- Bắt đầu chat với AI của quán: {merchant_choice['name']} ---")
    logger.info("Gõ 'quit' hoặc 'exit' để thoát.\n")
    
    agent = MerchantAgent(merchant_id)
    messages = []
    
    # We will use a default session for terminal chat
    config = {"configurable": {"thread_id": "terminal_session"}}
    
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break
            
        if user_input.lower() in ['quit', 'exit']:
            break
            
        messages.append(HumanMessage(content=user_input))
        
        for state in agent.stream({"messages": messages}, stream_mode="values", config=config):
            latest_msg = state["messages"][-1]
            if latest_msg.type == "ai" and hasattr(latest_msg, "tool_calls") and latest_msg.tool_calls:
                tool_calls_str = ", ".join([f"{tc['name']}({tc['args']})" for tc in latest_msg.tool_calls])
                logger.info(f"> tool([{tool_calls_str}])")
                    
            messages = state["messages"]
        
        ai_msg = messages[-1]
        logger.info(f"\nAI: {ai_msg.content}\n")
        logger.info("="*50)

if __name__ == "__main__":
    chat_loop()
