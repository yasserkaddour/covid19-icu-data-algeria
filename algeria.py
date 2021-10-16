# A large portion of the code came from the COVID-19 Dataset project by Our World in Data 
# https://github.com/owid/covid-19-data/tree/master/scripts/scripts/vaccinations/src/vax/manual/twitter
# Mainly contributed by Lucas Rodés-Guirao https://github.com/lucasrodes
# The code is under completely open access under the Creative Commons BY license
# https://creativecommons.org/licenses/by/4.0/

import os
import pandas as pd
import re
import tweepy

try:
    from config import TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET
except ImportError:
    TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
    TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')

class TwitterAPI:

    def __init__(self, consumer_key: str, consumer_secret: str):
        self._api = self._get_api(consumer_key, consumer_secret)

    def _get_api(self, consumer_key, consumer_secret):
        auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
        return tweepy.API(auth)

    def get_tweets(self, username, num_tweets=30):
        tweets = tweepy.Cursor(self._api.user_timeline ,
                   screen_name=username, 
                               include_rts=False,
            tweet_mode='extended',
            exclude_replies=False,
        ).items(num_tweets)
        return tweets


class TwitterCollectorBase:
    
    def __init__(self, api, username: str, location: str, num_tweets=100):
        self.username = username
        self.location = location
        self.tweets = api.get_tweets(self.username, num_tweets)
        self.tweets_relevant = []
        self.output_path = "./algeria-covid19-icu-data.csv"
        self._data_old = self._get_current_data()

    def _set_output_path(self, paths, output_path):
        if output_path is None:
            if paths is not None:
                return paths.tmp_vax_out_proposal(self.location)
            else:
                raise AttributeError("Either specify attribute `paths` or method argument `output_path`")

    def _get_current_data(self):
        if os.path.isfile(self.output_path):
            return pd.read_csv(self.output_path)
        else:
            None

    @property
    def last_update(self):
        if self._data_old is not None:
            return self._data_old.date.max()
        else:
            return None

    def _propose_df(self):
        raise NotImplementedError

    def propose_df(self):
        df = (
            self._propose_df()
            .pipe(self.merge_with_current_data)
            .sort_values("date")
        )
        return df

    def build_post_url(self, tweet_id: str):
        return f"https://twitter.com/{self.username}/status/{tweet_id}"

    def merge_with_current_data(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return self._data_old
        if self._data_old is not None:
            df_current = self._data_old[~self._data_old.date.isin(df.date)]
            df = pd.concat([df, df_current]).sort_values(by="date")
        return df

    def stop_search(self, dt):
        if self._data_old is None:
            return False
        elif dt >= self.last_update:
            return False
        elif dt < self.last_update:
            return True

    def to_csv(self):
        df = self.propose_df()
        df.to_csv(self.output_path, index=False)


class Algeria(TwitterCollectorBase):
    def __init__(self, api, **kwargs):
        super().__init__(
            api=api,
            username="Sante_Gouv_dz",
            location="Algeria",
            **kwargs
        )

    def _propose_df(self):
        data = []
        for tweet in self.tweets:
            match = re.search(r"مؤشرات الترصد لوباء كوفيد-19", tweet.full_text) or re.search(r"حصيلة وباء كورونا كوفيد-19 ليوم", tweet.full_text)
            match2 = re.search(r"في العناية المركز", tweet.full_text)
            if match and match2:
                dt_match = re.search(r"(\d{1,2})\s*([ء-ي]+)\s*[ء-ي]*(202\d)", tweet.full_text)
                dt = dt_match.group(3)+"-"+arabicMonthToNum(dt_match.group(2))+"-"+dt_match.group(1).zfill(2)
                if self.stop_search(dt):
                    break
                new_cases_line =re.findall("^.*جديدة.*$",tweet.full_text,re.MULTILINE)[0]
                new_cases = int(re.search(r'\d+', new_cases_line).group(0)) 
                recoveries_line =re.findall("^.*للشفاء.*$",tweet.full_text,re.MULTILINE)[0]
                recoveries = int(re.search(r'\d+', recoveries_line).group(0)) 
                in_icu_line =re.findall("^.*في العناية المركز.*$",tweet.full_text,re.MULTILINE)[0]
                in_icu = int(re.search(r'\d+', in_icu_line).group(0)) 
                new_deaths_line =re.findall("^.*وفيات.*$",tweet.full_text,re.MULTILINE)[0]
                new_deaths = int(re.search(r'\d+', new_deaths_line).group(0)) 
                data.append({
                    "date": dt,
                    "new_cases": new_cases,
                    "recoveries": recoveries,
                    "in_icu": in_icu,
                    "death": new_deaths,
                    "text": tweet.full_text,
                    "source_url": self.build_post_url(tweet.id),
                })
        df = pd.DataFrame(data)
        return df

def arabicMonthToNum(month):
    return {
            'جانفي' : "01",
            'فيفري' : "02",
            'مارس' : "03",
            'أفريل' : "04",
            'ماي' : "05",
            'جوان' : "06",
            'جويلية' : "07",
            'اوت' : "08",
            'أوت' : "08",
            'سبتمبر' : "09", 
            'أكتوبر' : "10",
            'اكتوبر' : "10",
            'كتوبر' : "10",
            'نوفمبر' : "11",
            'ديسمبر' : "12"
    }[month]


def main():
    api = TwitterAPI(TWITTER_CONSUMER_KEY,TWITTER_CONSUMER_SECRET)
    Algeria(api).to_csv()


if __name__ == "__main__":
    main()
