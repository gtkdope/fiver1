import tweepy
import logging
import time
import random
from secrets import *
from datetime import datetime, timedelta
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token,token_secret)
api = tweepy.API(auth)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

"""

This function will search for tweets that mention your Twitter 
handle and will like and retweet each tweet it finds

"""

def fav_retweet(api):
    logger.info('Retrieving tweets...')
    mentions = api.mentions_timeline(tweet_mode = 'extended')
    for mention in reversed(mentions):
        if mention.in_reply_to_status_id is not None or mention.user.id == api.me().id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        
        if not mention.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                mention.favorite()
                logger.info(f"Liked tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
                
        if not mention.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                mention.retweet()
                logger.info(f"Retweeted tweet by {mention.user.name}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)


""" 

This function will search for tweets that mention any given Twitter 
handle and will like and retweet each tweet it finds

"""

def fav_retweet_user(api, user_handle):
    search_query = f"{user_handle} -filter:retweets"
    logger.info(f'Retrieving tweets mentioning {user_handle}...')
    tweets = api.search(q=search_query, lang ="en")
    for tweet in tweets:
        #if tweet.in_reply_to_status_id is not None or tweet.user.id == api.me().id:
        #    print ("one")
            # This tweet is a reply or I'm its author so, ignore it
        #    return
        if not tweet.favorited:
            print ("two")
            # Mark it as Liked, since we have not done it yet
            try:
                print("two ty")
                tweet.favorite()
                logger.info(f"Liked a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
                logger.info(f"Retweeted a tweet mentioning {user_handle}")
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

"""
Follow All Your Followers

"""

def follow_followers(api):
    logger.info("Retrieving and following followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            try:
                follower.follow()
                logger.info(f"Following {follower.name}")
            except tweepy.error.TweepError:
                pass

"""

Unfollow a given Id or everyone you follow

"""

def unfollow(api, follower_id = None):
    if not follower_id:
        logger.info("Retrieving current users being followed...")
        for following_id in tweepy.Cursor(api.friends).items():
            try:
                api.destroy_friendship(following_id.id)
                logger.info(f"Unfollowed {following_id.name}")
            except tweepy.error.TweepError:
                pass
    else:
        try:
            api.destroy_friendship(follower_id)
            logger.info(f"Unfollowed {follower_id}...")
        except tweepy.error.TweepError:
            pass  


"""
Retweet the tweets that have given  hashtags
Hastags needs to be supplid in a python list

"""

def retweet_tweets_with_hashtag(api, need_hashtags):
    if type(need_hashtags) is list:
        search_query = f"{need_hashtags} -filter:retweets"
        tweets = api.search(q=search_query, lang ="en", tweet_mode='extended')
        if len(tweets) > 3:
            tweets= tweets[:3]
        for tweet in tweets:
            hashtags = [i['text'].lower() for i in tweet.__dict__['entities']['hashtags']]
            try:
                need_hashtags = [hashtag.strip('#').lower() for hashtag in need_hashtags]
                need_hashtags = list(need_hashtags)
                if set(hashtags) & set(need_hashtags):
                    if tweet.user.id != api.me().id:
                        api.retweet(tweet.id)
                        logger.info(f"Retweeted tweet from {tweet.user.name}")
                        time.sleep(5)
            except tweepy.TweepError:
                logger.error("Error on retweet", exc_info=True)
    else:
        print("else")
        logger.error("Hashtag search terms needs to be of type list", exc_info=True) 
        return
            

"""
Tweet Daily the date and time
not need for this project

"""

def tweet_daily(api, last_tweeted, text):
    if last_tweeted < datetime.now()-timedelta(hours=24):
        api.update_status(text)
        logger.info(f"Tweeted {text} at {datetime.now().strftime('%m/%d/%Y at %H:%M:%S')}")
        return datetime.now()
    else:
        return last_tweeted



"""def main():
    tweets = ["I am happy", "I am sad", "I am hungry", "I am tired"]
    api = create_api()
    last_tweeted = datetime.now()-timedelta(hours=24)
    while True:
        fav_retweet_user(api,"@asvn90")
        last_tweeted = tweet_daily(api, last_tweeted, random.choice(tweets))
        logger.info("Waiting...")
        time.sleep(60)"""



"""
Follow people who use a certain hashtag

"""
def follow_hashtag(api,need_hashtag):
    count = 0
    for follower in tweepy.Cursor(api.search, q=need_hashtag).items():
        if count < 3:
            person = follower.author.screen_name
            try:
                api.create_friendship(screen_name = person)
                logger.info(f"Followed  {person}")
                count  += 1
            except:
                continue
        else:
            break


def DM(api,screen_name,text):
    user=api.get_user(screen_name)
    recipient_id=user.id_str
    try:
        api.send_direct_message(recipient_id, text)
        logger.info("Sent {m} to \n{person}".format(m=text,person=screen_name))
    
    except tweepy.TweepError:

        logger.error("Cannot send dms to this person", exc_info=True)
        return


def get_tweets (api,screen_name):
    
    logger.info(f"geting tweets of: {screen_name}")
    tweets= api.user_timeline(screen_name=screen_name, count=2,include_rts = True,tweet_mode = 'extended')
    for tweet in tweets:
        try:
            api.retweet(tweet.id)
            logger.info(f"Retweeted tweet from {screen_name}")
        except:
            continue



        


# Running fav_retweet()
"""while True:
    fav_retweet(api)
    logger.info("Waiting...")
    time.sleep(30)"""

#Running fav_retweet_user()
"""f=open('people.txt','r')
for User in f.readlines():
    
    get_tweets(api,User)
    logger.info("Waiting...")
    time.sleep(5)
f.close()
"""

#Following all those who follow you

"""follow_followers(api)"""


#Unfollowing everyone
"""
unfollow(api)
"""



#Retwetting given hastags and following 5 people who use the hashtag
"""f = open ('hashtags.txt','r')
for Tag in f.readlines():
    
    Tag=Tag.rstrip()
    retweet_tweets_with_hashtag(api,[Tag])
    follow_hashtag(api,Tag)
    logger.info("Waiting...")
    time.sleep(30)
f.close()"""

#Tweet someting from database



#Following people who follow a certain hashtag
"""
follow_hashtag(api,"#Shorts")"""


#Dm a given recipient
"""
DM(api,"@ChrissyCostanza","text123")

"""


if __name__=='__main__':
    while True:
        #Retwetting given hastags and following 5 people who use the hashtag
        f = open ('hashtags.txt','r')
        for Tag in f.readlines():
            
            Tag=Tag.rstrip()
            retweet_tweets_with_hashtag(api,[Tag])
            follow_hashtag(api,Tag)
            logger.info("Waiting...")
            time.sleep(3)
        f.close()

        logger.info("Retwetting hashtag finished now waiting for starting retwetting important people")
        time.sleep(5)

        #Running Retweeting important people
        f=open('people.txt','r')
        for User in f.readlines():
            
            get_tweets(api,User)
            logger.info("Waiting...")
            time.sleep(5)
        f.close()

        logger.info("Done retweeting tweets from important people")
        time.sleep(5)





