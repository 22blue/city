import pandas as pd
import streamlit as st
import base64

# 读取数据
file_path = "景点.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

# 初始化优先级列
if '优先级' not in df.columns:
    df['优先级'] = 0

# 页面配置
st.set_page_config(
    page_title="城市景点查询系统",
    page_icon="🏙️",
    layout="wide"
)

# 背景处理
def get_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        st.error("背景图片未找到")
        return ""

background_image = get_base64("a.jpg")

# 优化后的CSS样式
st.markdown(f"""
<style>
.stApp {{
    background-image: url(data:image/jpeg;base64,{background_image});
    background-size: cover;
    background-attachment: fixed;
    padding: 0 !important;
}}

.search-header {{
    background: rgba(255, 255, 255, 0.95);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
    margin: 1rem auto;
    max-width: 800px;
}}

.search-row {{
    display: flex;
    gap: 1rem;
    justify-content: center;
}}

.result-card {{
    background-color: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
    margin-bottom: 1.5rem;
}}
</style>
""", unsafe_allow_html=True)

# 主界面
st.markdown("<h1 style='text-align: center; color: #2c3e50; margin: 1rem 0;'>🏛️ 城市景点查询系统</h1>", unsafe_allow_html=True)

# 常驻搜索栏
with st.container():
    st.markdown("<div class='search-header'>", unsafe_allow_html=True)

    # 双列搜索布局
    col1, col2 = st.columns([2, 3])
    with col1:
        city = st.text_input(
            "城市名称",
            placeholder="输入城市（可选）",
            key="city_search"
        )
    with col2:
        attraction_name = st.text_input(
            "景点名称",
            placeholder="输入景点名称关键字（可选）",
            key="name_search"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# 动态筛选逻辑
if city or attraction_name:
    # 构建筛选条件
    condition = pd.Series([True] * len(df))

    if city:
        condition &= df['城市'].str.contains(city, case=False)
    if attraction_name:
        condition &= df['景点名称'].str.contains(attraction_name, case=False)

    filtered_df = df[condition].sort_values('优先级', ascending=False)

    if not filtered_df.empty:
        with st.container():
            st.markdown(f"<div style='text-align: center; margin: 2rem 0; color: #666;'>找到 {len(filtered_df)} 个匹配景点</div>", unsafe_allow_html=True)

            # 双列显示结果
            cols = st.columns(2)
            for idx, row in filtered_df.iterrows():
                with cols[idx % 2]:
                    st.markdown(f"""
                    <div class='result-card'>
                        <h3 style='color: {"#2A79B3" if row["优先级"] else "#333333"}; margin-bottom: 1rem;'>
                            {'⭐ ' if row["优先级"] else ''}{row["景点名称"]}
                            <span style="font-size: 0.8em; color: #888;">（{row["城市"]}）</span>
                        </h3>
                        <div style='line-height: 1.6;'>
                            <p><b>📍 类型：</b>{row["类型"]}</p>
                            <p><b>⏰ 开放时间：</b>{row["开放时间"]}</p>
                            <p><b>🕑 建议时长：</b>{row["游玩时长"]}</p>
                            <p><b>🌐 官网：</b>{row["官网地址"] if row["官网地址"] != '无' else '暂未提供'}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ 未找到符合条件的景点信息")
else:
    st.info("ℹ️ 请在搜索栏输入城市或景点名称开始查询")