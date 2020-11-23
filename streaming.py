import sys
import time
import tweepy 
import pandas as pd
sys.version_info
com_key = ''
com_secret = ''
acc_key = ''
acc_secret = ''
auth = tweepy.OAuthHandler(com_key,com_secret )
auth.set_access_token(acc_key, acc_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

ini_csv = pd.DataFrame(columns=['date','user','is_retweet','is_quote','tid'])
ini_csv.to_csv('new_out.csv',index=False)
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        streaming_screen_name = pd.read_csv('streaming_target.csv',dtype=str)
        if status.user.screen_name in list(streaming_screen_name['screen_name'].values) and hasattr(status, "retweeted_status") == False:
            print(status.id_str)
            print(status.user.screen_name)
            print(status.created_at)
            # if "retweeted_status" attribute exists, flag this tweet as a retweet.
            is_retweet = hasattr(status, "retweeted_status")
            
            # check if text has been truncated
            if hasattr(status,"extended_tweet"):
                text = status.extended_tweet["full_text"]
            else:
                text = status.text

            # check if this is a quote tweet.
            is_quote = hasattr(status, "quoted_status")
            quoted_text = ""
            if is_quote:
                # check if quoted tweet's text has been truncated before recording it
                if hasattr(status.quoted_status,"extended_tweet"):
                    quoted_text = status.quoted_status.extended_tweet["full_text"]
                else:
                    quoted_text = status.quoted_status.text

            # remove characters that might cause problems with csv encoding
            remove_characters = [",","\n"]
            for c in remove_characters:
                text.replace(c," ")
                quoted_text.replace(c, " ")

            with open("new_out.csv", "a", encoding='utf-8') as f:
                f.write("%s,%s,%s,%s,%s\n" % (status.created_at,status.user.screen_name,is_retweet,is_quote,status.id_str))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

if __name__ == "__main__":
#     # complete authorization and initialize API endpoint
#     auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#     auth.set_access_token(access_key, access_secret)
#     api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
#    with open("out.csv", "w", encoding='utf-8') as f:
#        f.write("date,user,is_retweet,is_quote,tid\n")
#     tags = ["hate speech"]
    streaming_screen_name = pd.read_csv('streaming_target.csv',dtype=str)
    while True:
        time.sleep(1)
        try:
            stream.filter(follow=list(streaming_screen_name['id'].values))
        except:
            continue
