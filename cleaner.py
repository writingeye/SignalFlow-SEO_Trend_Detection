import pandas as pd 
from config import KEYWORD
from fetcher import *

# cleaner
def prepare_df(df, source, keyword):
  df_copy = df.copy()
  df_copy = df_copy.drop(columns=["isPartial"])
  df_copy = df_copy.reset_index()
  # df_copy[keyword] = df_copy[keyword] * WEIGHTS[source]
  # df_copy = df_copy.rename(columns = {"date":"ds", keyword:"y"})
  df_copy["source"] = source
  return df_copy

cleaned_search = prepare_df(search_df, "search", KEYWORD)
cleaned_youtube = prepare_df(youtube_df, "youtube", KEYWORD)
cleaned_news = prepare_df(news_df, "news", KEYWORD)

# combined_df = pd.concat([cleaned_search, cleaned_youtube, cleaned_news])
# combined_df = pd.concat([cleaned_search, cleaned_youtube, cleaned_news], join="outer")

combined_df.sort_values("date", ascending=False)