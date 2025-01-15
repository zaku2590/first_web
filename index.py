import streamlit as st
from streamlit_chat import message

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.schema import AIMessage
from dotenv import load_dotenv
# 環境変数の読み込み
load_dotenv()

# ChatGPT-3.5のモデルのインスタンスの作成
chat = ChatOpenAI(model_name="gpt-3.5-turbo",temperature=0.2)

# セッション内に保存されたチャット履歴のメモリの取得
try:
    memory = st.session_state["memory"]
except:
    memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("""
    あなたは、百戦錬磨のプレイボーイです。とても優しく相手の女性を気遣いながら素敵なメールの返事を書いて女性を喜ばせます。ほんの少しセクシーな大人の男性の雰囲気を醸し出した文章によりお相手の女性はうっとりしていまいます。これからあなたは私になりきり女性へのメッセージの返信を代筆します。メッセージはしつこくならない程度の200文字程度の文章でやりとりをします。なおかつ相手のプロフィールに準拠した内容です。

    #メッセージの制約事項
    - メッセージの最初はマッチングしたことに対するお礼を入れること
    - 相手の呼び方を聞くこと
    - 一人称は僕、相手のことはさん付けで呼ぶこと。
    - 僕のプロフィールに準拠した返信を書くこと
    - お互いの共通項でのお話を優先すること。
    - 丁寧語ではなすけど丁寧になりすぎないこと。
    - メッセージには適度に相手の興味関心を惹きつけるような質問を加えることそして会話のキャッチボールを促すこと。
    - 基本的に聞き上手であること、
    - 自分のことを話しすぎないこと
    - ほんのちょっぴり女性から見てセクシーであること
    - 適切なメッセージ交換数(4回以上）でデートにお誘いすること。お食事が望ましい

    ここから下は私が登録している婚活アプリのプロフィール情報です。プロフィール情報をうまく活用してメッセージを作成してください。
    """),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
prompt_reply = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("あなたは、百戦錬磨のプレイボーイです。とても優しく相手の女性を気遣いながら素敵なメールの返事を書いて女性を喜ばせます。ほんの少しセクシーな大人の男性の雰囲気を醸し出した文章によりお相手の女性はうっとりしていまいます。これからあなたは私になりきり女性へのメッセージの返信を代筆します。メッセージはしつこくならない程度の200文字程度の文章でやりとりをします。相手からの返信を基に自分の返答を作成してください。その際に、3ラリー程度で実際に会ってデートするような会話に持っていってください。そのため、具体的な日時や場所、デート内容などを会話から引き出し決定するような返信を考えてください"),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# チャット用のチェーンのインスタンスの作成
chain = ConversationChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
)
# リプライ用チャット用のチェーンのインスタンスの作成
chain_reply = ConversationChain(
    llm=chat,
    prompt=prompt_reply,
    memory=memory,
)

button_click_num = 0

# Streamlitによって、タイトル部分のUIをの作成
st.title("婚活GPT")
st.caption("返信作成")

# チャット履歴（HumanMessageやAIMessageなど）を格納する配列の初期化
history = []

humanHistory = []
aiHistory = []

if "isDisplayReply" not in st.session_state:
    st.session_state["isDisplayReply"] = 0

# 入力フォームと送信ボタンのUIの作成
if st.session_state.isDisplayReply == 0:
    text_my_profile_input = st.text_area("自分のプロフィール", height=150, max_chars=600)
    text_your_profile_input = st.text_area("相手のプロフィール", height=150, max_chars=600)
    send_button = st.button("送信")
else:
    send_button = None

# text_my_profile_input = "はじめまして。都内の企業で管理職をしているナオキです。年齢は40代の前半です。仕事はある程度部下に任せる立場になり、すこし気持ちや時間に余裕がもてたのと、自分とは違う世代の方と交流することで、若い世代との接し方が学べたり自分磨きになるのでは？と思いサイトに登録しました。一緒に美味しい食事やお酒を楽しんだり、ゆっくりとお話する素敵な時間を過ごせる女性を探しています。20代前半～30代ぐらいで、のんびり時間をすごせる、ちょっとおっとりした女性を希望しています。複数の方と同時に関係をもつことは考えていないので、長期的、定期的な関係を築ける方が見つかればと思っています。はじめは、ランチやカフェでお茶などでお話をしながら、お互いの印象を確認したいなと思います。オシャレなカフェやスイーツに詳しい方は是非教えてください。休日はゴルフやドライブ、旅行先などで散歩をしてのんびり過ごすのが好きです。親しくなれたらご一緒できると嬉しいです。長文になりましたが、最後までご覧いただきありがとうございました。よい出会いになりますように。"

# text_your_profile_input = "はじめまして、えみりです。プロフィールを見てくださってありがとうございます。経済学部を卒業後、商社で事務系の仕事をしています。家では資格取得の勉強とお料理していることが多く、あまり外出する機会がありません。自分の知らない世界を勉強したいと思い、思い切って登録してみました。お酒はたしなむ程度ですが、好き嫌いなく何でも食べます。特にカレーが好きです。同僚からは、幸せそうに食べるって言われます.見た目は童顔で、普通くらいの体型です。経験豊富な年上の男性から、お話を聞かせてもらえたらいいなと思っています。一人の方に、長期的に会っていただけるのが理想です。都内に住んでいるので、お会いする時間と場所は合わせられると思います。少しでも興味を持っていただけたら、連絡をいただけると嬉しいですわからないことが多いので、失礼や不手際があったらすみません。素敵な方とお会いできることを楽しみにしています"

# ボタンが押された時、OpenAIのAPIを実行
if send_button:
    send_button = False
    st.session_state["isDisplayReply"] = 1

    chat_prompt = AIMessage
    with st.spinner("ChatGPT is typing ..."):
        chain.predict(input="自分のプロフィール:\n```\n"+text_my_profile_input+"\n```\n相手のプロフィール:\n```\n"+text_your_profile_input+"\n```")

    # セッションへのチャット履歴の保存
    st.session_state["memory"] = memory

    # チャット履歴（HumanMessageやAIMessageなど）の読み込み
    try:
        history = memory.load_memory_variables({})["history"]
    except Exception as e:
        st.error(e)

    # チャット履歴の表示
    for index, chat_message in enumerate(history):
        if type(chat_message) == HumanMessage:
            message(chat_message.content, is_user=True, key=2 * index)
        elif type(chat_message) == AIMessage:
            message(chat_message.content, is_user=False, key=2 * index + 1)

def clear_reply():
    st.session_state["reply"] = ""

if st.session_state.isDisplayReply == 1:
    reply = st.text_area("相手の返信",height=100, max_chars=400, key="reply")
    send_reply_button = st.button("返信を送信")
else:
    send_reply_button = None
# ボタンが押された時、返信用のOpenAIのAPIを実行
# if len(history) > 0:
if send_reply_button:
    send_button = False

    chat_prompt = AIMessage

    # チャット履歴（HumanMessageやAIMessageなど）の読み込み
    try:
        history = memory.load_memory_variables({})["history"]
    except Exception as e:
        st.error(e)

    # チャット履歴の取得
    for index, chat_message in enumerate(reversed(history)):
      if type(chat_message) == HumanMessage:
          humanHistory.append(chat_message.content)
      elif type(chat_message) == AIMessage:
          aiHistory.append(chat_message.content)

    with st.spinner("ChatGPT is typing ..."):
        chain.predict(input="自分のメッセージ:\n```\n"+aiHistory[button_click_num]+"\n```\n相手からの返信:\n```\n"+reply+"\n```")

    #　todo メッセージ履歴にしたい
    # chain.predict(input="メッセージの履歴:\n```\n"+text_my_profile_input+"\n```\n相手からの返信:\n```\n"+reply+"\n```")
    
    # セッションへのチャット履歴の保存
    st.session_state["memory"] = memory

    button_click_num += 1

    # チャット履歴の表示
    for index, chat_message in enumerate(history):
        if type(chat_message) == HumanMessage:
            message(chat_message.content, is_user=True, key=2 * index)
        elif type(chat_message) == AIMessage:
            message(chat_message.content, is_user=False, key=2 * index + 1)