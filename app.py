import streamlit as st
import pandas as pd
import numpy as np

def calculate_bmr(w, h_cm, age, gender):
    val = (10 * w) + (6.25 * h_cm) - (5 * age)
    return val + 5 if gender == 'M' else val - 161

st.set_page_config(page_title="目標體重達成模擬器", layout="wide")
st.title("🎯 目標體重達成規劃器")

with st.sidebar:
    st.header("👤 基本資料")
    gender = st.selectbox("性別", ["M", "F"])
    h = st.number_input("身高 (cm)", value=175.0)
    curr_w = st.number_input("目前體重 (kg)", value=70.0)
    age = st.number_input("年齡", value=25)
    
    st.divider()
    st.header("🏁 設定目標")
    target_w = st.number_input("目標體重 (kg)", value=65.0)
    target_days = st.number_input("預計達成時間 (天)", value=60, min_value=1)
    
    activity_map = {"久坐": 1.2, "輕度": 1.375, "中度": 1.55, "高度": 1.725, "極高": 1.9}
    act_val = activity_map[st.selectbox("活動量", list(activity_map.keys()), index=1)]

# --- 計算邏輯 ---
bmr = calculate_bmr(curr_w, h, age, gender)
tdee = bmr * act_val

# 總共需要減少/增加的熱量 (1kg = 7700 kcal)
total_diff_needed = (target_w - curr_w) * 7700
daily_diff_needed = total_diff_needed / target_days
recommended_intake = tdee + daily_diff_needed

# --- 顯示結果 ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("您的 TDEE", f"{tdee:.0f} kcal")

with col2:
    diff_color = "normal" if recommended_intake >= 1200 else "inverse"
    st.metric("建議每日攝取", f"{recommended_intake:.0f} kcal", 
              f"{daily_diff_needed:.0f} kcal/日", delta_color=diff_color)

with col3:
    status = "減重" if target_w < curr_w else "增重"
    st.metric(f"預計總{status}", f"{abs(target_w - curr_w):.1f} kg")

# --- 安全警告 ---
st.divider()
if recommended_intake < 1200:
    st.error(f"⚠️ **警告：** 為了達成目標，您的每日攝取量低於 1200 kcal。這可能會損害基礎代謝與健康，建議延長達成天數。")
elif recommended_intake < bmr:
    st.warning(f"💡 **提醒：** 您的攝取量低於基礎代謝率 (BMR: {bmr:.0f} kcal)。長期如此可能導致肌肉流失。")
else:
    st.success(f"✅ **計畫可行：** 每天攝取 {recommended_intake:.0f} kcal，配合目前活動量，您可以在 {target_days} 天後達到目標！")

# --- 圖表預測 ---
days_idx = np.arange(target_days + 1)
weight_trend = curr_w + (daily_diff_needed * days_idx / 7700)
st.subheader("📅 體重達成路徑預測")
st.line_chart(pd.DataFrame({"體重 (kg)": weight_trend}))
