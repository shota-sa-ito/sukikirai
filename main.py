import json
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List

from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.llms.openai import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
import streamlit as st

from local import api_key


class Page(Enum):
    top = "top"
    quesion = "question"
    answer = "answer"


@dataclass
class RequestFirst:
    age: str
    gender: str
    hobbies_interests: str
    personality_type: str
    holiday_preference: str
    partner_gender: str
    partner_character: str
    partner_work: str
    partner_hobby: str
    length: str
    weight: str
    work: str


@dataclass
class MyState:
    answers: Optional[List[str]]
    request_first: Optional[RequestFirst]
    page: Page = Page.top


class Main:
    
    def __init__(self) -> None:
        self.llm = OpenAI(openai_api_key=api_key, model_name="gpt-3.5-turbo-0613")
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
        st.header("あなたの情報を記載してください。")
        age = st.slider("年齢を選択してください", 20, 60, 25)
        # 身長
        length = st.slider("身長を入力してください。", 100, 250, 150)
        # 体重
        weight = st.slider("体重を入力してください。", 0, 300, 70)
        # 性別
        gender = st.radio("性別を選択してください", ["男性", "女性"])
        # 職業
        work = st.text_input("職業を入力してください。")

        # 趣味・興味
        hobbies_interests = st.text_input("趣味・興味を入力してください")

        # 性格(自由記述)
        personality_type = st.text_input("性格を入力してください")

        # 休日の過ごし方(自由記述)
        holiday_preference = st.text_input("休日の過ごし方を入力してください")

        st.header("理想の相手の情報を記載してください。")
        partner_gender = st.radio("理想の相手の性別を選択してください", ["男性", "女性"])
        partner_character = st.selectbox("相手の性格は？", ["頼りになる", "可愛らしい", "物静か"])
        partner_hobby = st.selectbox("相手の趣味は？", ["自分と同じ", "別な趣味を持っているが理解してくれる。", "無趣味"])
        partner_work = st.selectbox("仕事は", ["共働き", "専業主婦"])

        # ボタン
        if not st.button("送信"):
            return

        # Todo: バリデーション
        req = RequestFirst(
            age=age,
            gender=gender,
            hobbies_interests=hobbies_interests,
            personality_type=personality_type,
            holiday_preference=holiday_preference,
            partner_gender=partner_gender,
            partner_character=partner_character,
            partner_hobby=partner_hobby,
            partner_work=partner_work,
            length=length,
            weight=weight,
            work=work
        )
        self.init_question_page_state(req)
        # ページ遷移のため再実行
        st.rerun()
        # result = self.request_first()
        # st.write(result)

    def init_question_page_state(self, req: RequestFirst):
        st.session_state.my_state.request_first = req
        st.session_state.my_state.page = Page.quesion
        st.session_state.my_state.answers = []

    def question_page(self):
        max_count = 4
        @st.cache_data()
        def get_from_ai(req: RequestFirst, count: int):
            template = (f"ユーザー情報: (年齢: {req.age}, 性格: {req.personality_type}, 性別: {req.gender}, 休日の過ごし方: {req.holiday_preference}, 趣味: {req.hobbies_interests}, 仕事: {req.work}, 身長: {req.length}, 体重: {req.weight}) "
                        f"ChatGPTのタスク: (ユーザー情報のすべてを使用してそのユーザーの普段の生活で困っていそうなことを予想して1文にまとめてください。)")
            # Todo: 会話履歴が残ってしまっている
            conversation: ConversationChain = ConversationChain(
                llm=self.llm,
                verbose=True,
                memory=ConversationBufferMemory()
            )
            conversation.predict(input=template)
            template = (
                '予想した行動に対して最も解決したほうがいい具体的な質問を生成してください。'
                '質問に対して〇〇していないのような否定系でネガティブな選択肢4つを提供してください。'
                '質問は難しくせず小学生でも分かるような言葉にしてください。'
                '質問と選択肢以外は出力しないでください。json形式で出力してください。'
                '例: {"question": "ストレスを管理するために、以下の選択肢の中から最も当てはまる行動を選んでください。", "selections": ["ストレスを全く意識していない。","ストレスが溜まったら感情を爆発させてしまう。","ストレスへの対処方法を知らない","定期的にリラクゼーション法を実践していない"]'
            )
            question_and_answer_str_raw = conversation.predict(input=template)
            question_and_answer_str = json.loads(question_and_answer_str_raw)
            template = (f'selections:['
                        + ', '.join(question_and_answer_str['selections'])
                        +']ChatGPTのタスク: (selectionsに対して改善するアドバイスを生成してください。questionとselectionsは出力せずアドバイスのみを出力してください。json形式で出力してください。例: {"answer": ["体の健康を維持するための良い習慣を持っている。しかし、心のリラックスも大切にすること。","心の健康を維持するための良い習慣を持っている。しかし、体の活動も忘れずに。","趣味の時間を大切にしているが、長時間のゲームは体や目への負担となる可能性がある。","エンジニアとしての熱心さが伺えるが、適切な休息が不足している可能性が高い。"]})')
            advise_str_raw = conversation.predict(input=template)
            conversation.memory.clear()
            # Todo: たまにjson形式で出力してくれないときがある(のでデバッグ用に出力)
            try:
                advise_str = json.loads(advise_str_raw)
            except json.JSONDecodeError as e:
                print(advise_str_raw)
                raise e
            return [question_and_answer_str, advise_str]

        count = len(st.session_state.my_state.answers)
        while True:
            try:
                result = get_from_ai(st.session_state.my_state.request_first, count)
            except json.JSONDecodeError:
                continue
            break
        qa = result[0]
        question = qa['question']
        selections = qa['selections']
        advice = result[1]['answer']
        st.text(question)
        answer = [st.button(s) for s in selections]
        # 答えなかったばあい
        if not any(answer):
            return
        # 答えた場合の処理
        st.session_state.my_state.answers.append(advice[answer.index(True)])
        if count + 1 >= max_count:
            # 答えきった場合の処理
            self.init_answer_page()
        st.rerun()

    def init_answer_page(self):
        st.session_state.my_state.page = Page.answer

    def answer_page(self):
        @st.cache_data()
        def get_from_ai():
            advices = st.session_state.my_state.answers
            req: RequestFirst = st.session_state.my_state.request_first
            template = (
                f"""
                以下の文章をすごく{req.partner_character}な{req.partner_gender}の口調で表現してください。表現したものは必ず「」で閉じてください。
                """
                + '\n'.join(advices)
                + f"また、{req.partner_character}な{req.partner_gender}の目線で解決方法を付け足してください。次のjson形式にしてください"
                """
                {"tone1": "心のリラックスも忘れずにね。ストレスをためないように、趣味やリラックスする時間を持つのも大切だよ。心も体も元気でいたいからね。","tone2": "心のリラックスも忘れずにね。ストレスをためないように、趣味やリラックスする時間を持つのも大切だよ。心も体も元気でいたいからね。","tone3": "心のリラックスも忘れずにね。ストレスをためないように、趣味やリラックスする時間を持つのも大切だよ。心も体も元気でいたいからね。","tone4": "心のリラックスも忘れずにね。ストレスをためないように、趣味やリラックスする時間を持つのも大切だよ。心も体も元気でいたいからね。",}
                
                ただし、以下の文章は生成しないでください。
                - 自分の話。
                - セリフ以外の文章
                - 口調の説明
                """
            )
            text = self.llm.predict(template)
            return json.loads(text)
        
        result: dict[str, str] = get_from_ai()
        print(result)
        for v in result.values():
            st.text(v)

    def _main(self):
        # stateの初期化
        if 'my_state' not in st.session_state:
            st.session_state.my_state = MyState(request_first=None, page=Page.top, answers=None)
        # タイトルの設定
        st.title("MIRAI NO IRAI")
        st.text("未来の二人へ、今日からの挑戦。")

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
