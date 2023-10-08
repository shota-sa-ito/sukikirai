from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
import streamlit as st

from local import api_key


class Page(Enum):
    top = "top"
    quesion = "question"
    answer = "answer"


@dataclass
class RequestFirst:
    age_range: str
    gender: str
    hobbies_interests: str
    personality_type: str
    holiday_preference: str


@dataclass
class MyState:
    answers: Optional[List[str]]
    request_first: Optional[RequestFirst]
    page: Page = Page.top


class Main:
    
    def __init__(self) -> None:
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

    def top_page(self):
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

        st.write('Just a moment!')
        # Todo: バリデーション
        req = RequestFirst(
            age_range=age_range,
            gender=gender,
            hobbies_interests=hobbies_interests,
            personality_type=personality_type,
            holiday_preference=holiday_preference
        )
        self.init_question_page_state(req)
        # ページ遷移のため再実行
        st.rerun()
        # result = self.request_first()
        # st.write(result)

    def init_question_page_state(self, req: RequestFirst):
        st.session_state.my_state.request_first = req
        st.session_state.my_state.page = Page.quesion
        st.session_state.my_state.answer = []

    def question_page(self):
        @st.cache_data()
        def get_from_ai(req: RequestFirst):
            # Todo: implementation
            return self.chat_model.predict("こんにちは")
        result = get_from_ai(st.session_state.my_state.request_first)
        question = "明日の天気は"
        selections = ["晴れ", "くもり", "雨", "雪", "雷"]
        st.text(question)
        answer = [st.button(s) for s in selections]
        if not any(answer):
            return
        # 答えた場合の処理
        # 答えきった場合の処理

    def answer_page(self):
        @st.cache()
        def get_from_ai(req: RequestFirst):
            # Todo: implementation
            return self.chat_model.predict("こんにちは")
        
        result = get_from_ai(st.session_state.my_state.request_first)

    def _main(self):
        # stateの初期化
        if 'my_state' not in st.session_state:
            st.session_state.my_state = MyState(request_first=None, page=Page.top, answers=None)
        # タイトルの設定
        st.title("すききらい")

        # Stateに合わせてページを表示分ける
        page = st.session_state.my_state.page.value
        if page == Page.top.value:
        # 年齢範囲、性別、趣味興味、性格、休日の過ごし方
            self.top_page()
        elif page == Page.quesion.value:
            self.question_page()
        elif page == Page.answer.value:
            self.answer_page()
        else:
            print("Unreachable")

    
    @staticmethod
    def main():
        main = Main()
        main._main()

if __name__ == "__main__":
    Main.main()
