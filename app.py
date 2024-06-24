# 必要なライブラリをインポート
from flask import Flask
import tweepy
from openai import ChatCompletion
import openai
import os
from dotenv import load_dotenv

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# .envファイルをロード
load_dotenv()

# Twitter APIキーの設定
twitter_keys = {
    "consumer_key": os.getenv("CONSUMER_KEY"),
    "consumer_secret": os.getenv("CONSUMER_SECRET"),
    "access_token": os.getenv("ACCESS_TOKEN"),
    "access_token_secret": os.getenv("ACCESS_TOKEN_SECRET")
}

# OpenAI APIキーの設定
openai.api_key = os.getenv("OPENAI_KEY")

# Twitter APIの認証を設定
auth = tweepy.OAuthHandler(twitter_keys["consumer_key"], twitter_keys["consumer_secret"])
auth.set_access_token(twitter_keys["access_token"], twitter_keys["access_token_secret"])

# Twitter APIのインスタンスを作成
api = tweepy.API(auth)

def generate_today_info():

    import random

    prompts = [
            f"よくあるニーズを一言で一つ教えてください。シチュレーションもあると分かりやすいです。「～と」「～が」「～を」「～に」「～で」で始まり「～と」「～が」「～を」「～に」「～で」を挟み「したい」「してほしい」「たい」「ほしい」で終わるようにしてください",
            f"恋愛でよくある具体的なニーズを一言で一つ教えてください。シチュレーションもあると分かりやすいです。「～と」「～が」「～を」「～に」「～で」で始まり「～と」「～が」「～を」「～に」「～で」を挟み「したい」「してほしい」「たい」「ほしい」で終わるようにしてください",
            f"仕事でよくある具体的なニーズを一言で一つ教えてください。シチュレーションもあると分かりやすいです。「～と」「～が」「～を」「～に」「～で」で始まり「～と」「～が」「～を」「～に」「～で」を挟み「したい」「してほしい」「たい」「ほしい」で終わるようにしてください",
            f"通勤でよくある具体的なニーズを一言で一つ教えてください。シチュレーションもあると分かりやすいです。「～と」「～が」「～を」「～に」「～で」で始まり「～と」「～が」「～を」「～に」「～で」を挟み「したい」「してほしい」「たい」「ほしい」で終わるようにしてください",
            f"学校でよくある具体的なニーズを一言で一つ教えてください。シチュレーションもあると分かりやすいです。「～と」「～が」「～を」「～に」「～で」で始まり「～と」「～が」「～を」「～に」「～で」を挟み「したい」「してほしい」「たい」「ほしい」で終わるようにしてください"
        ]
    
    prompt = random.choice(prompts)
    prompt = prompt + "　文法や助詞が不自然にならないように注意すること（不自然になっていたら地球が滅びます）　分の最後に「。」を付けないで出力すること"

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたは世間の具体的なニーズを知り尽くしたプロです。ニーズのみを出力してください。"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=280
    )
    # GPT-4oからのレスポンスは複数の選択肢（'choices'）の形で返ってきます。
    # ここでは最初の選択肢（'choices'[0]）のテキストを取得し、前後の空白を削除（.strip()）して返します。
    return response['choices'][0]['message']['content'].strip() 
    

# GPT-4oを使用してツイートを生成する関数を定義します。
def generate_tweet_with_gpt4o():
    # プロンプト（GPT-3に与える初期の入力）を設定します。

    shimo_success = False
    shimo_mes = ""
    while not shimo_success:
        user_message = generate_today_info()
        print(user_message)

        prompt = f"""
        次の指示に従って、さとり構文でぶっとんだ面白い下品な下ネタ文章を書いてください：

1. **特定の目的やニーズ**を持つ人を明示してください（ここはユーザにニーズを聞いてください）。
2. その人たちが取るべき**ぶっ飛んだ下品な具体的な行動**を提案してください。（具体的に詳細にすること。絶対にありえないだろう思うぶっ飛んだ下品な下ネタを提案すること。下品にすることにフォーカスすること。）
3. **ぶっ飛んだ下品な具体的な行動**で得られる**ポジティブな結果**を提案してください。(爆笑、笑い系は除いて具体的に何が得れるのかを提示)
4. **似ている特定の目的やニーズを持つ人**を提案（ユーザに聞いたニーズに関連するものにすること）（文脈が不自然にならないようにすること）
5. **似ている特定の目的やニーズを持つ人が得られる**ポジティブな結果**を説明してください。
6. **ポジティブな結果や利益**がどのくらい増加するか具体的な数字を挙げてください。（～％）

「{user_message}なら～[ぶっ飛んだ下品な具体的な行動]+[自然な文末]！！ + [ポジティブな結果] + [自然な文末]！！+ [似ている特定の目的やニーズを持つ人] + には + [似ている特定の目的やニーズを持つ人が得られるポジティブな結果] +[自然な文末]！！

上記の形で出力してください。

[]内は変数です。実際の回答に[]は出力しなくていいです。

必ず140字以内にまとめてください（守らないと地球が滅びます）
文法や接続詞が不自然にならないように注意すること（不自然になっていたら地球が滅びます）
本文のみ出力してください。



---

それでは、「特定の目的やニーズ」のみユーザに聞いてください。聞いた「特定の目的やニーズ」に沿った文章を書いてください。
            """
        
        
        # GPT-4oにプロンプトを与えて、最大280トークンのレスポンスを生成させます。
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=280
        )
        print("-----------------------------------------")
        shimo_mes = response['choices'][0]['message']['content']
        print(f"判定前:{shimo_mes}")
        if("申し" not in shimo_mes and len(shimo_mes) <= 140 and "以下に" not in shimo_mes and "目的ニーズ" not in shimo_mes and "ニーズ" not in shimo_mes and "ごめん" not in shimo_mes
           and "自然な" not in shimo_mes and "+" not in shimo_mes and user_message in shimo_mes):
            break
           
    return shimo_mes
        

def tweet():
    print("tweet()が呼び出されました")
    client = tweepy.Client(
        consumer_key        = twitter_keys["consumer_key"],
        consumer_secret     = twitter_keys["consumer_secret"],
        access_token        = twitter_keys["access_token"],
        access_token_secret = twitter_keys["access_token_secret"],
    )
    text = generate_tweet_with_gpt4o()
    client.create_tweet(text = text)
    print(f"ツイート内容：{text}")
    print("tweet()の処理が完了しました")
    return text

if __name__ == "__main__":
    # Flaskアプリケーションを実行
    app.run()