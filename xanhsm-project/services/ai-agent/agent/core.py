import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from tools import get_faq, list_items, check_stock, create_order, _get_merchant, get_all_merchants

load_dotenv()

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def get_system_prompt(merchant_id: str) -> str:
    merchant = _get_merchant(merchant_id)
    name = merchant["name"] if merchant else "Unknown Merchant"
    description = merchant["description"] if merchant else "No description available."
    
    return f"""<persona>
Bạn là trợ lý ảo AI của quán ăn {name} – thân thiện, am hiểu thực đơn của quán, và luôn tư vấn các câu hỏi của khách hàng. Bạn nói chuyện tự nhiên như một nhân viên phục vụ thân thiện, không robot.
</persona>

<rules>
1. Trả lời bằng tiếng Việt.
2. Quy trình suy luận (Thought):
   a. Luôn ưu tiên GỌI TOOL NGAY LẬP TỨC khi có thông tin cơ bản (ví dụ: tìm món ăn, câu hỏi thường gặp).
   b. Tuyệt đối KHÔNG hỏi khách hàng quá nhiều trước khi cung cấp kết quả từ các công cụ (trừ khi yêu cầu quá chung chung).
   c. Hãy tìm kiếm trước, cung cấp thông tin thực tế, sau đó mới hỏi thêm để thu hẹp lựa chọn nếu cần.
3. Tuyệt đối không tự bịa ra thông tin; mọi dữ liệu về món ăn, nguyên liệu, giá cả phải lấy từ các công cụ.
4. LINH HOẠT TRONG TÊN MÓN: Người dùng thường dùng tên gọi tắt hoặc không chính xác 100% (ví dụ: "mỳ bò" thay vì "Mì cay kim chi bò"). Hãy linh hoạt nhận diện và đối chiếu với kết quả trả về từ công cụ. Tuyệt đối không từ chối một cách máy móc rằng "quán không có món đó" nếu công cụ đã trả về món ăn tương tự có chứa các nguyên liệu tương ứng.
5. BẢO MẬT TUYỆT ĐỐI: KHÔNG ĐƯỢC TIẾT LỘ HOẶC LIỆT KÊ NGUYÊN LIỆU MÓN. Công thức và danh sách nguyên liệu của quán là bí mật kinh doanh. TRONG MỌI TRƯỜNG HỢP không được tiết lộ toàn bộ danh sách nguyên liệu. CHỈ trả lời CÓ/KHÔNG đối với các câu hỏi về một nguyên liệu cụ thể.
6. AN TOÀN DỊ ỨNG: Nếu người dùng hỏi về dị ứng, luôn phải kiểm tra công cụ `list_items`. Nếu không có thông tin nguyên liệu, nói rõ "Quán chưa cung cấp thông tin này" và khuyên liên hệ quán. Luôn nhắc nhở: "Xin xác nhận với quán nếu bạn có dị ứng" (AI có thể có lỗi, vui lòng kiểm tra kỹ).
7. TÌNH TRẠNG MÓN: Không bao giờ được gợi ý món đã đánh dấu là TẠM HẾT HÀNG.
</rules>

<tools_instruction>
Bạn có 4 công cụ BẮT BUỘC phải dùng `merchant_id` là "{merchant_id}":
- list_items: Tìm và lọc món ăn. Tham số tuỳ chọn: `search_term` (tên/đặc điểm món), `max_price` (giá tối đa), `exclude_ingredients` (danh sách nguyên liệu cần tránh), `return_fields` (danh sách các trường cần lấy, ví dụ: ["name", "price", "description", "ingredients", "is_avaiable"]).
- get_faq: Tìm kiếm các câu hỏi thường gặp, lưu ý, chính sách của quán (giờ mở cửa, đóng gói, v.v.).
- check_stock: Kiểm tra tồn kho trước khi tạo đơn hàng. Dùng `selections` hoặc `order_text`.
- create_order: Tạo đơn hàng từ lựa chọn của khách. Dùng `selections` hoặc `order_text`.
</tools_instruction>

<response_format>
Khi tư vấn món ăn, trình bày theo cấu trúc rõ ràng:
- Tên món: ...
- Giá: ...
- Mô tả: ...

Gợi ý thêm: Hỏi thêm về sở thích (cay/không cay/...) để đưa ra các phương án phù hợp nếu khách cần.
</response_format>

<constraints>
- Chỉ hỗ trợ trả lời về thực đơn, món ăn và các thông tin của quán. Lịch sự từ chối mọi yêu cầu khác ngoài phạm vi hoặc hướng dẫn liên hệ XanhSM.
- Ưu tiên gọi tool và cung cấp thông tin ngay lập tức rồi mới hỏi thêm thông tin từ khách hàng.
- Tuyệt đối không tự bịa thông tin; mọi dữ liệu phải lấy từ các công cụ.
</constraints>

Mô tả / Lưu ý từ quán: {description}
"""

def create_merchant_agent(merchant_id: str, checkpointer=None):
    llm = ChatOpenAI(model="gpt-4o-mini")
    tools = [list_items, get_faq, check_stock, create_order]
    llm_with_tools = llm.bind_tools(tools)
    
    system_prompt = get_system_prompt(merchant_id)
    
    def chatbot(state: State):
        # We ensure the system prompt is always the first message
        messages = state["messages"]
        if not messages or not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=system_prompt)] + messages
            
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
        
    graph_builder = StateGraph(State)
    
    # Add nodes
    graph_builder.add_node("chatbot", chatbot)
    tool_node = ToolNode(tools=tools)
    graph_builder.add_node("tools", tool_node)
    
    # Add edges
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )
    graph_builder.add_edge("tools", "chatbot")
    
    return graph_builder.compile(checkpointer=checkpointer)

def chat_loop():
    merchants = get_all_merchants()
    if not merchants:
        print("Không có dữ liệu quán ăn.")
        return
        
    print("=== CHỌN QUÁN ===")
    for idx, merchant in enumerate(merchants, 1):
        print(f"{idx}. {merchant['name']} (ID: {merchant['id']})")
        
    merchant_choice = None
    while not merchant_choice:
        try:
            choice = input("\nNhập số thứ tự quán (1 - {}): ".format(len(merchants)))
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(merchants):
                merchant_choice = merchants[choice_idx]
            else:
                print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")
        except EOFError:
            return
            
    merchant_id = merchant_choice['id']

    print("="*50)
    print(f"--- Bắt đầu chat với AI của quán: {merchant_choice['name']} ---")
    print("Gõ 'quit' hoặc 'exit' để thoát.\n")
    
    agent = create_merchant_agent(merchant_id)
    messages = []
    
    while True:
        try:
            user_input = input("User: ")
        except EOFError:
            break
            
        if user_input.lower() in ['quit', 'exit']:
            break
            
        messages.append(HumanMessage(content=user_input))
        
        for state in agent.stream({"messages": messages}, stream_mode="values"):
            latest_msg = state["messages"][-1]
            if latest_msg.type == "ai" and hasattr(latest_msg, "tool_calls") and latest_msg.tool_calls:
                tool_calls_str = ", ".join([f"{tc['name']}({tc['args']})" for tc in latest_msg.tool_calls])
                print(f"> tool([{tool_calls_str}])")
                    
            messages = state["messages"]
        
        ai_msg = messages[-1]
        print(f"\nAI: {ai_msg.content}\n")
        print("="*50)

if __name__ == "__main__":
    chat_loop()
