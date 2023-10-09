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

## 動作環境
- 今回はcolab上でアプリケーションを起動し、ngrokで外部公開した
- sukikirai.ipynb
## googl colab 上での秘匿情報の扱い方
- 秘匿情報を書いた txt を googl drive の任意の場所に保存(今回はmydrive)
- 以下で drive と colab をつなげる
  - window が開くので承認する
```
from google.colab import drive
drive.mount('/content/drive')
```
- ファイルを指定して変数名に保存する
```
with open('/content/drive/My Drive/unkstone/api_key.txt', 'r') as file:
    api_key = file.readline().strip()
```

## ngrok で　colab 上から外部公開する
- ngrok の会員登録をして左タブの Your Authtoken からアクセスキーを取得
- pyngrok をインストール
```
!pip install pyngrok --quiet
```
- アプリケーションコードの一番上に以下のコードを追加
```
%%writefile app.py
```
- アプリケーションを起動
  - portはngrokと合わせておく必要がある
```
!streamlit run app.py --server.port 8051 &>/dev/null&
```
- 以下で外部公開をする
```
# アクセスキーを適用
!ngrok authtoken ngrok_key
ngrok.kill()
# pygronkにアクセスキーを登録
ngrok.set_auth_token(ngrok_key)
# 公開
public_url = ngrok.connect(8051).public_url
```