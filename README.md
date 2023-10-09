# sukikirai
石巻ハッカソン2023 スキキライ

## Install
お使いのパッケージマネージャで以下を導入する
- Python3.11
- Poetry

このリポジトリにcdしてから以下実行
```
poetry install
```

local.pyを作成して、以下のような内容を書く
```python
# api_keyはopenAI API用のキーに変える
api_key = "sk-xxxx"
```

環境変数を使う場合は以下のようにする
```python
import os
api_key = os.environ["OPENAI_API_KEY"] 
```

## 実行
以下のコマンドで仮想環境に入ってから
```
poetry shell
```

以下のコマンドでstreamlitを起動する
```
streamlit run main.py
```