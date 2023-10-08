from dataclasses import dataclass
import os

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import streamlit as st

@dataclass
class RequestFirst():
    age_range: str
    gender: str
    hobbies_interests: str
    personality_type: str
    holiday_preference: str


class Main:
    
    def __init__(self) -> None:
        api_key = os.environ["OPENAI_API_KEY"]
        self.llm = OpenAI(openai_api_key=api_key)
        self.chat_model = ChatOpenAI(openai_api_key=api_key)

    def request_first(self, req: RequestFirst) -> str:
        template = (
            "年齢希望範囲: {age_range} 性別: {gender} 趣味・興味: {hobbies_interests} 性格: {personality_type} 休日の過ごし方: {holiday_preference}"
            f"age_range = 20-30 gender = 女 hobbies_interests = ゲーム personality_type = ほんわかしている holiday_preference = 映画館に行くことが多い。 "
            
            "--- あなたは私の恋人です。 あなたは{age_range}の間の年齢で、性別は{gender}です。 趣味は{hobbies_interests}で性格は{personality_type}です。 休日はいつも{holiday_preference}をしています。"
            " この情報を元に口調を作って会話してください。 この人物の会話以外は出力しないでください"
        )
        prompt = PromptTemplate.from_template(template)
        format_pronpt = prompt.format(age_range="20-30", gender="女", hobbies_interests="ゲーム", personality_type="ほんわかしている",holiday_preference="映画館に行くことが多い。")
        return self.llm.predict(format_pronpt)

    def _main(self):
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
        
        # Todo: バリデーション
        st.write("考え中")
        result = self.request_first(RequestFirst(
            age_range=age_range,
            gender=gender,
            hobbies_interests=hobbies_interests,
            personality_type=personality_type,
            holiday_preference=holiday_preference
        ))
        st.write(result)
    
    @staticmethod
    def main():
        main = Main()
        main._main()

if __name__ == "__main__":
    Main.main()
