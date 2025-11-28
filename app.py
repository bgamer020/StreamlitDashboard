import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Load CSS Cyberpunk (nếu dùng) ---
with open("cyberpunk.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Tạo thanh tab ngang ---
tab_home, tab_chart, tab_info = st.tabs(["Trang chủ", "Biểu đồ", "Thông tin"])

with tab_home:
    st.title("Chào mừng đến với ứng dụng phân tích YouTube")
    st.write("Bạn có thể xem biểu đồ phân bố subscriber ở tab Biểu đồ.")
    st.write("Tab Thông tin chứa thêm chi tiết về dữ liệu hoặc ứng dụng.")

with tab_chart:
    st.title("Phân bố Subscriber của các kênh YouTube")

    # --- Đọc dữ liệu ---
    df = pd.read_csv("channels.csv")

    subs = df['subscriberCount'].dropna()
    subs = subs[subs > 0]

    max_subs = subs.max()
    bins = np.arange(0, max_subs + 100_000, 100_000)

    def fmt(x):
        if x >= 1_000_000:
            return f"{x/1_000_000:.1f}M"
        else:
            return f"{x/1_000:.0f}K"

    labels = [f"{fmt(bins[i])}-{fmt(bins[i+1])}" for i in range(len(bins)-1)]

    count_per_range = pd.cut(
        subs,
        bins=bins,
        labels=labels,
        right=False
    ).value_counts().sort_index()

    count_per_range = count_per_range[count_per_range > 0]

    fig, ax = plt.subplots(figsize=(14,6))
    count_per_range.plot(kind='bar', color='#1DB954', edgecolor='white', ax=ax)

    ax.set_facecolor('#0a0a0a')
    fig.patch.set_facecolor('#0a0a0a')

    ax.set_title("Phân bố số lượng kênh theo khoảng Subscriber", fontsize=14, color='white')
    ax.set_xlabel("Khoảng Subscriber", fontsize=12, color='white')
    ax.set_ylabel("Số lượng kênh", fontsize=12, color='white')

    plt.xticks(rotation=45, ha='right', color='white')
    plt.yticks(color='white')
    plt.tight_layout()

    st.pyplot(fig)

with tab_info:
    st.title("Thông tin")
    st.write("""
        Đây là ứng dụng demo phân tích dữ liệu các kênh YouTube.
        Dữ liệu được lấy từ file `channels.csv`.
        Ứng dụng sử dụng Streamlit và matplotlib để hiển thị biểu đồ.
    """)
