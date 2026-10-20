import requests
import time
import random
import pandas as pd
from pytrends.request import TrendReq
from pytrends import exceptions # Import exceptions module to catch TooManyRequestsError

def fetch_trends(KEYWORD, gprop="", hl="fr", time_frame ="today 12-m", tz=360):
  """
    Fetches Google Trends data for a list of keywords.
    gprop: "" (web), "youtube", or "news"
    Returns a raw wide dataframe.
  """
  pytrends = TrendReq( timeout = (10,20),
                      # requests_args = {"verify": False }, # Corrected typo: Flase to False
                       )
  max_tries = 10
  wait_seconds = 2
  retries = 0

  while retries < max_tries:
    try :
      print(f"\nSending request for : {KEYWORD}")
      # Pass KEYWORD as a list to pytrends.build_payload
      pytrends.build_payload([KEYWORD] ,
                            gprop= gprop,
                            timeframe = time_frame
                            )
      iot = pytrends.interest_over_time()
      if iot.empty:
        # If empty, raise ValueError to trigger retry logic or final return
        raise ValueError("Empty Dataframe received from pytrends.")
      else:
        print("✅ Success")
        time.sleep(3)
        return iot
    except exceptions.TooManyRequestsError as e:
        # This specifically handles the 429 error raised by pytrends when rate-limited
        retries += 1
        wait = min(wait_seconds * (2 ** retries) + random.uniform(0, 5), 120)
        print(f"⚠️ 429 Rate limit (PytrendsError). Retrying in {wait:.0f}s. Attempt {retries}/{max_tries}")
        time.sleep(wait)
    except requests.exceptions.HTTPError as e:
        # This handles general HTTP errors not specifically caught by pytrends.exceptions
        status = e.response.status_code if e.response is not None else None
        retries += 1

        if status == 429:
            wait = min(wait_seconds * (2 ** retries) + random.uniform(0, 5), 120)
            print(f"⚠️ 429 Rate limit (HTTPError). Retrying in {wait:.0f}s. Attempt {retries}/{max_tries}")
            time.sleep(wait)
        elif status == 500:
            wait = min(wait_seconds * (2 ** retries) + random.uniform(0, 5), 120)
            print(f"⚠️ 500 Google error. Retrying in {wait:.0f}s. Attempt {retries}/{max_tries}")
            time.sleep(wait)
        elif status == 400:
            print("⚠️ 400 Bad request. Skipping.")
            print("❌ Unknown HTTP error:", e)
            raise ValueError("Wrong Keyword or bad request from HTTPError.") # Re-raise for immediate stop
        else:
            wait = min(wait_seconds * (2 ** retries) + random.uniform(0, 5), 120)
            print(f"❌ Unknown HTTP error: {e}. Retrying in {wait:.0f}s. Attempt {retries}/{max_tries}")
            time.sleep(wait)
    except ValueError as e: # Catch the ValueError for "Empty Dataframe"
        retries += 1
        wait = min(wait_seconds * (2 ** retries) + random.uniform(0, 5), 120)
        print(f"⚠️ {e}. Retrying in {wait:.0f}s. Attempt {retries}/{max_tries}")
        time.sleep(wait)
    except Exception as e:
        # Catch any other unexpected errors
        retries += 1
        wait = min(wait_seconds * (2 ** retries) + random.uniform(0, 5), 120)
        print(f"❌ An unexpected error occurred: {e}. Retrying in {wait:.0f}s. Attempt {retries}/{max_tries}")
        time.sleep(wait)

  print(f"❌ Max retries ({max_tries}) reached for KEYWORD: {KEYWORD}. Returning empty DataFrame.")
  # If all retries fail, return an empty DataFrame with the expected columns
  # so subsequent operations like prepare_df don't fail immediately due to missing columns.
  # `isPartial` is expected by `prepare_df` to be dropped.
  return pd.DataFrame(columns=['date', KEYWORD, 'isPartial'])

# Calling fetch_treds function
search_df = fetch_trends(KEYWORD, gprop="")
youtube_df = fetch_trends(KEYWORD, gprop="youtube")
news_df = fetch_trends(KEYWORD, gprop="news")