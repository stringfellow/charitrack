import tweepy

from django.db import models

# Create your models here.

class TweetTrack(models.Model):
    query = models.CharField(max_length=200)
    last_checked = models.DateTimeField(auto_now=True)
    tweets = models.ManyToManyField('Tweet', null=True, blank=True)
    rate = models.PositiveIntegerField(default=3)

    def __unicode__(self):
        return self.query

    @property
    def updatable(self):
        if self.last_checked < (datetime.now() - timedelta(minutes=self.rate)) or not self.last_checked:
            return True
        return False

    def update(self):
        if not self.updatable:
            return
        
        try:
            pass
        except Exception, e:
            print "Twitter get error:",e.code
            self.last_checked = datetime.now()
            self.rate = self.rate+1
            self.save()
            return

        self.rate = 3
        for tweet in tweets:
            (tw, created) = Tweet.objects.get_or_create(twit_id=tweet['id'],
                json_dump=simplejson.dumps(tweet))
            self.tweets.add(tw)
        self.save()
        return tweets

    def cleanup(self):
        today = datetime.now()
        yesterday = today - timedelta(1)
        old_tweets = self.tweets.filter(retrieved_lte=yesterday)
        for tweet in old_tweets:
            tweet.delete()


class Tweet(models.Model):
    twit_id = models.CharField(max_length=200)
    retrieved = models.DateTimeField(auto_now_add=True)
    json_dump = models.TextField()

    @property
    def obj(self):
        result = simplejson.loads(self.json_dump)
        return result

    def __unicode__(self):

        return self.obj['text'][:20]
