import streamlit as st
import numpy as np
import pandas as pd

# ================= CẤU HÌNH WEB =================
st.set_page_config(page_title="AI Gridworld Game", layout="wide")
st.title("🗺️ Học Tăng Cường: Trò Chơi Thế Giới Lưới (Gridworld)")
st.write("Hãy tự chọn vị trí xuất phát, tìm đường đi tốt nhất và đọ sức với AI!")

# ================= HIỂN THỊ LUẬT CHƠI =================
with st.expander("📖 Xem Luật Chơi Chi Tiết (Gridworld MDP)", expanded=False):
    st.markdown(r"""
    * **Bản đồ:** Lưới 5x5 (Hàng 0-4, Cột 0-4). Bạn có thể di chuyển 4 hướng.
    * **Ô Đặc Biệt A (Hàng 0, Cột 1):** Bất kể bấm hướng nào, bạn bị hút đến **A' (4, 1)** và nhận **+10 điểm**.
    * **Ô Đặc Biệt B (Hàng 0, Cột 3):** Bất kể bấm hướng nào, bạn bị hút đến **B' (2, 3)** và nhận **+5 điểm**.
    * **Tường rào:** Đi ra ngoài bản đồ bị bật lại ô cũ và **phạt -1 điểm**.
    * **Ô bình thường:** Di chuyển an toàn nhưng được **0 điểm**.
    """)

# ================= THANH TRƯỢT TƯƠNG TÁC =================
st.sidebar.header("🕹️ Cài Đặt AI")
gamma = st.sidebar.slider(r"Hệ số nhìn xa trông rộng ($\gamma$)", 0.0, 0.99, 0.9, 0.05)
st.sidebar.info("Kéo Gamma xuống 0 để thấy AI trở nên thiển cận, mất khả năng tìm đường xa.")

# ================= THUẬT TOÁN VALUE ITERATION =================
def solve_gridworld(gamma):
    V = np.zeros((5, 5))
    actions = {'⬆️ Lên': (-1, 0), '⬇️ Xuống': (1, 0), '⬅️ Trái': (0, -1), '➡️ Phải': (0, 1)}
    
    for _ in range(100):
        V_new = np.copy(V)
        for r in range(5):
            for c in range(5):
                if r == 0 and c == 1:
                    V_new[r, c] = 10 + gamma * V[4, 1]
                elif r == 0 and c == 3:
                    V_new[r, c] = 5 + gamma * V[2, 3]
                else:
                    v_actions = []
                    for act, (dr, dc) in actions.items():
                        nr, nc = r + dr, c + dc
                        if nr < 0 or nr >= 5 or nc < 0 or nc >= 5:
                            v_actions.append(-1 + gamma * V[r, c])
                        else:
                            v_actions.append(0 + gamma * V[nr, nc])
                    V_new[r, c] = max(v_actions)
        V = V_new
        
    policy = np.full((5, 5), '', dtype=object)
    for r in range(5):
        for c in range(5):
            if r == 0 and c == 1:
                policy[r, c] = '🌟 Bất kỳ'
            elif r == 0 and c == 3:
                policy[r, c] = '⭐ Bất kỳ'
            else:
                best_val = -float('inf')
                best_act = ''
                for act, (dr, dc) in actions.items():
                    nr, nc = r + dr, c + dc
                    val = -1 + gamma * V[r, c] if (nr < 0 or nr >= 5 or nc < 0 or nc >= 5) else 0 + gamma * V[nr, nc]
                    if val > best_val:
                        best_val = val
                        best_act = act
                policy[r, c] = best_act
    return V, policy

V_star, Pi_star = solve_gridworld(gamma)

# ================= CHIA TABS GIAO DIỆN =================
tab1, tab2 = st.tabs([ "🎮 Chơi Trực Tiếp (Human Mode)", "🔬 Bản Đồ AI (Toán Học)"])

# --- TAB 1: BẢN ĐỒ AI ---
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(r"1. Bảng Giá Trị $V^*$")
        df_v = pd.DataFrame(V_star, columns=[f"Cột {i}" for i in range(5)], index=[f"Hàng {i}" for i in range(5)])
        st.dataframe(df_v.style.background_gradient(cmap="YlGn", axis=None).format("{:.1f}"), width='stretch', height=220)
    with col2:
        st.subheader(r"2. Chính Sách Tối Ưu $\pi_*$ (La Bàn)")
        df_pi = pd.DataFrame(Pi_star, columns=[f"Cột {i}" for i in range(5)], index=[f"Hàng {i}" for i in range(5)])
        st.dataframe(df_pi, width='stretch', height=220)

# --- TAB 2: CHẾ ĐỘ NGƯỜI CHƠI ---
with tab1:
    st.subheader("Bàn Điều Khiển Agent 🤖")
    
    # Khởi tạo Session State
    if 'gw_r' not in st.session_state: st.session_state.gw_r = 4
    if 'gw_c' not in st.session_state: st.session_state.gw_c = 0
    if 'score' not in st.session_state: st.session_state.score = 0
    if 'steps' not in st.session_state: st.session_state.steps = 0
    if 'gw_logs' not in st.session_state: st.session_state.gw_logs = ["Trò chơi bắt đầu! Hãy dùng bảng điều khiển bên dưới."]

    # === THIẾT LẬP VỊ TRÍ BAN ĐẦU ===
    st.markdown("### 📍 Thay đổi / Thiết lập vị trí xuất phát")
    col_sel1, col_sel2, col_sel3 = st.columns([1, 1, 1.5])
    with col_sel1:
        start_r = col_sel1.selectbox("Chọn Hàng (0-4):", range(5), index=int(st.session_state.gw_r), key="select_row")
    with col_sel2:
        start_c = col_sel2.selectbox("Chọn Cột (0-4):", range(5), index=int(st.session_state.gw_c), key="select_col")
    with col_sel3:
        st.write("") 
        st.write("")
        if st.button("🚀 Đặt Agent vào vị trí này & Reset điểm", width='stretch', type="secondary"):
            st.session_state.gw_r = start_r
            st.session_state.gw_c = start_c
            st.session_state.score = 0
            st.session_state.steps = 0
            st.session_state.gw_logs = [f"🚀 Đã đặt lại Agent tại vị trí mới: Hàng {start_r}, Cột {start_c}!"]
            st.rerun()

    st.markdown("---")

    # === HÀM XỬ LÝ DI CHUYỂN ===
    def move(action_name, dr, dc):
        r, c = st.session_state.gw_r, st.session_state.gw_c
        ai_move = Pi_star[r, c]
        
        if ai_move in ['🌟 Bất kỳ', '⭐ Bất kỳ']:
            msg_ai = "🤖 AI: Dịch chuyển không gian thành công!"
        elif action_name == ai_move:
            msg_ai = f"🤖 AI: Nước đi xuất sắc! Khớp với $\pi_*$ ({ai_move})."
        else:
            msg_ai = f"🤖 AI: Nước đi LỖI! Thuật toán khuyên phải đi {ai_move}."

        if r == 0 and c == 1:
            st.session_state.gw_r, st.session_state.gw_c = 4, 1
            st.session_state.score += 10
            log = f"Dịch chuyển A -> A' (+10 điểm). \n{msg_ai}"
        elif r == 0 and c == 3:
            st.session_state.gw_r, st.session_state.gw_c = 2, 3
            st.session_state.score += 5
            log = f"Dịch chuyển B -> B' (+5 điểm). \n{msg_ai}"
        else:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 5 and 0 <= nc < 5:
                st.session_state.gw_r, st.session_state.gw_c = nr, nc
                log = f"Đi {action_name} an toàn (0 điểm). \n{msg_ai}"
            else:
                st.session_state.score -= 1
                log = f"Đi {action_name} đâm tường! (-1 điểm). \n{msg_ai}"
                
        st.session_state.steps += 1
        st.session_state.gw_logs.insert(0, log)

    # === GIAO DIỆN GAME ===
    col_game, col_ctrl = st.columns([1.5, 1])

    with col_game:
        sub_c1, sub_c2 = st.columns(2)
        sub_c1.metric("🏆 Điểm của bạn", st.session_state.score)
        sub_c2.metric("⏱️ Số bước đã đi", st.session_state.steps)
        
        # ---------------------------------------------------------
        # UPDATE UI: VẼ BÀN CỜ BẰNG HTML/CSS GRID THAY VÌ DATAFRAME
        # ---------------------------------------------------------
        html_grid = "<div style='display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; background-color: #2b3035; padding: 10px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); width: 100%; max-width: 450px; margin: auto;'>"
        
        for r in range(5):
            for c in range(5):
                content = ""
                bg_color = "#f8f9fa" 
                border_color = "#dee2e6"
                
                # Cấu hình màu và icon cho các ô đặc biệt
                if r == 0 and c == 1:
                    content, bg_color = "🅰️", "#cce5ff" 
                elif r == 0 and c == 3:
                    content, bg_color = "🅱️", "#fff3cd" 
                elif r == 4 and c == 1:
                    content, bg_color = "🎯", "#f8d7da" 
                elif r == 2 and c == 3:
                    content, bg_color = "🎯", "#f8d7da" 
                    
                # Vẽ đè Robot lên nếu robot đang đứng ở ô này
                if r == st.session_state.gw_r and c == st.session_state.gw_c:
                    content = "🤖"
                    bg_color = "#d1e7dd"
                        
                # Code HTML cho từng ô không bị thụt lề
                cell_html = f"<div style='background-color: {bg_color}; border: 2px solid {border_color}; border-radius: 8px; aspect-ratio: 1/1; display: flex; align-items: center; justify-content: center; font-size: 2.2rem;'>{content}</div>"
                html_grid += cell_html
                
        html_grid += "</div><br>"
        
        # Render trực tiếp lên màn hình
        st.markdown(html_grid, unsafe_allow_html=True)
        # ---------------------------------------------------------

    with col_ctrl:
        st.write("**🕹️ Bảng Điều Khiển**")
        
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col2: 
            if st.button("⬆️", width='stretch'): 
                move('⬆️ Lên', -1, 0); st.rerun()
        
        btn_col4, btn_col5, btn_col6 = st.columns(3)
        with btn_col4:
            if st.button("⬅️", width='stretch'): 
                move('⬅️ Trái', 0, -1); st.rerun()
        with btn_col5:
            if st.button("⬇️", width='stretch'): 
                move('⬇️ Xuống', 1, 0); st.rerun()
        with btn_col6:
            if st.button("➡️", width='stretch'): 
                move('➡️ Phải', 0, 1); st.rerun()

    # BẢNG NHẬT KÝ BÌNH LUẬN
    st.markdown("### 📜 Bình Luận Của AI:")
    for log in st.session_state.gw_logs[:5]:
        st.info(log)