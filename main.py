import streamlit as st

def main():
    st.title("すききらい")
    # 年齢範囲、性別、趣味興味、性格、休日の過ごし方

    # 年齢範囲
    # Todo: 年齢範囲の入力時、上限と下限の関係性を考慮する
    age_lower = st.slider("年齢上限を選択してください", 20, 60, 20)
    age_upper = st.slider("年齢下限を選択してください", 20, 60, 30)
    age_range = f"{age_lower}-{age_upper}"

    # 性別
    gender = st.radio("性別を選択してください", ["男性", "女性"])

    # 趣味・興味
    hobbies_interests = st.text_input("趣味・興味を入力してください")

    # 性格(自由記述)
    personality_type = st.text_input("性格を入力してください")

    # 休日の過ごし方(自由記述)
    holiday_preference = st.text_input("休日の過ごし方を入力してください")

    # ボタン
    if not st.button("送信"):
        return
    
    # Todo: バリデーションとAI呼ぶ処理
    st.write("考え中")

if __name__ == "__main__":
    main()
