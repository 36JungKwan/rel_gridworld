# REL301m Mini Lab: Gridworld AI

Ứng dụng Streamlit minh họa bài toán Gridworld trong học tăng cường (Reinforcement Learning). Người dùng có thể xem bảng giá trị tối ưu và chơi thử bằng tay với một agent trên lưới 5x5.

## Tính năng

- Hiển thị bài toán Gridworld MDP với 2 ô đặc biệt (A và B)
- Giải bài toán bằng thuật toán Value Iteration
- Trực quan hóa bảng giá trị $V^*$ và chính sách tối ưu $\pi_*$
- Giao diện tương tác cho người chơi kiểm tra nước đi và điểm số

## Yêu cầu

- Python 3.8+
- Streamlit
- NumPy
- pandas

## Cài đặt

1. Tạo môi trường ảo (khuyến nghị):

```bash
python -m venv .venv
```

2. Kích hoạt môi trường:

- Windows PowerShell:
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- Windows CMD:
  ```cmd
  .\.venv\Scripts\activate.bat
  ```

3. Cài đặt phụ thuộc:

```bash
pip install -r requirements.txt
```

## Chạy ứng dụng

```bash
streamlit run rel_gridworld.py
```

Sau đó mở trình duyệt theo địa chỉ được Streamlit cung cấp (thường là `http://localhost:8501`).

## Cấu trúc tệp

- `rel_gridworld.py`: mã chính của ứng dụng Streamlit
- `requirements.txt`: danh sách phụ thuộc Python
- `.gitignore`: các tệp/thư mục không nên đưa lên Git

## Ghi chú

Ứng dụng sử dụng thuật toán Value Iteration để tìm bảng giá trị tối ưu và chính sách cho mọi trạng thái trên lưới.
