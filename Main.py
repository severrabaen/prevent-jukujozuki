import tweepy
import twitter
import datetime
from datetime import datetime
from janome.tokenizer import Tokenizer
from requests_oauthlib import OAuth1Session

#認証情報の設定
CK = os.environ["CONSUMER_KEY"]
CS = os.environ["CONSUMER_SECRET"]
AT = os.environ["ACCESS_TOKEN_KEY"]
AS = os.environ["ACCESS_TOKEN_SECRET"]

#認証
twitter = OAuth1Session(CK, CS, AT, AS)
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

#削除後の報告
def report(liked, RTed):
  print("先程こちらが削除したあなたのツイートは削除までの%d秒間で%d件のいいねと%d件のリツイートを獲得していました!"% % liked, % RTed)
  api.PostUpdate("1件のツイートがprevent jukujozukiによって削除されました。ツイートした方、残念でしたね。")

#該当ツイートを削除する
def dele(tweetID, liked, RTed):
  api = 'https://api.twitter.com/1.1/statuses/destroy/' + tweetID + '.json'
  req = twitter.post(api)
  #for debug
  if req.status_code == 200:
    print("Deleted!")
    report(liked,RTed)
  else:
    print("Error has occured! ErrorCode: %d" % req.status_code)
  

#5分ごとに実行
@sched.scheduled_job('cron', minute = '0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55', hour = '*/1')
def check():
  #for debug
  print("Start checking...")
  target = api.me()
  #対象の最新100件のツイートを取得(さすがに5分で100ツイートはできないと思うのでこの数)
  tweets = tweepy.Cursor(api.user_timeline, id = target.id).items(100)
  for tweet in tweets:
    sentence = tweet.text#これはツイート本文
    t = Tokenizer()
    watasiha=False
    jukujo=False
    rorikon=False
    #分類した単語を入れていく
    sec=[]
    words=0
    for token in t.tokenize(sentance):
      sec.append((str)token.surface)
      words=words+1
    for i in words:
      if sec[i]=="は" and (sec[i-1]=="私" or sec[i-1]=="わたし"):
        watashiha=True
      if sec[i]=="熟女":
        jukujo=True
      #このワードは解析でどのように分けられるのか未調査
      if sec[i]=="":
        rorikon=True
      
      #条件を満たしていれば削除行程へ
    if watashiha and (jukujo or rorikon):
      dele(tweet.id,tweet.favorite_count,tweet.retweet_count)
    else:
      print("It seems that there is no tweet to delete...")
    #for debug
    print("Done!")
      
 sched.start()

check()
