import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from config.settings import Config
from utils.logger import get_logger

# Import Sentiment Analyzers
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

# Optional import for FinBERT to avoid slow startup if not used
try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

logger = get_logger("sentiment.analyzer")

class SentimentAnalyzer:
    """Class to handle financial news fetching and sentiment analysis."""
    
    def __init__(self, model_type: str = Config.SENTIMENT_MODEL):
        self.model_type = model_type.lower()
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        if self.model_type == "finbert":
            if not HAS_TRANSFORMERS:
                logger.error("transformers library not found. Falling back to vader.")
                self.model_type = "vader"
            else:
                logger.info("Loading FinBERT pipeline (this may take a moment)...")
                # Using ProsusAI/finbert for financial sentiment
                self.finbert = pipeline("sentiment-analysis", model="ProsusAI/finbert")
                logger.info("FinBERT loaded.")
                
    def fetch_news(self, ticker: str, days_back: int = 30) -> list:
        """
        Fetch news for a ticker. Uses NewsAPI if key is available, else mock data.
        """
        api_key = Config.NEWS_API_KEY
        if not api_key:
            logger.warning("No NEWS_API_KEY found. Using mock news data for demonstration.")
            return self._generate_mock_news(ticker, days_back)
            
        logger.info(f"Fetching actual news for {ticker} using NewsAPI.")
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        url = f"https://newsapi.org/v2/everything?q={ticker}&from={from_date}&sortBy=publishedAt&apiKey={api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('status') == 'ok':
                articles = data.get('articles', [])
                return [{'date': a['publishedAt'][:10], 'title': a['title']} for a in articles if a['title']]
            else:
                logger.error(f"NewsAPI error: {data.get('message')}")
                return self._generate_mock_news(ticker, days_back)
        except Exception as e:
            logger.error(f"Failed to fetch news: {str(e)}")
            return self._generate_mock_news(ticker, days_back)
            
    def _generate_mock_news(self, ticker: str, days_back: int) -> list:
        """Generate synthetic news data when API is unavailable."""
        import random
        mock_headlines = [
            f"{ticker} announces record quarterly earnings.",
            f"{ticker} faces new regulatory challenges.",
            f"Analysts upgrade {ticker} to Strong Buy.",
            f"Supply chain issues hit {ticker} production.",
            f"{ticker} launches innovative new product line.",
            f"Market volatility causes {ticker} stock to dip.",
            f"{ticker} CEO steps down amid controversy."
        ]
        
        articles = []
        for i in range(days_back):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            # 1 to 3 articles per day
            num_articles = random.randint(1, 3)
            for _ in range(num_articles):
                articles.append({
                    'date': date,
                    'title': random.choice(mock_headlines)
                })
        return articles
        
    def analyze_sentiment(self, text: str) -> float:
        """
        Return a sentiment score between -1.0 and 1.0
        """
        if self.model_type == "finbert":
            # FinBERT returns [{'label': 'positive', 'score': 0.8}]
            result = self.finbert(text)[0]
            label = result['label'].lower()
            score = result['score']
            if label == 'positive': return score
            elif label == 'negative': return -score
            else: return 0.0  # neutral
            
        elif self.model_type == "textblob":
            return TextBlob(text).sentiment.polarity
            
        else: # vader
            return self.vader_analyzer.polarity_scores(text)['compound']
            
    def get_daily_sentiment(self, ticker: str, days_back: int = 30) -> pd.DataFrame:
        """
        Fetch news, compute sentiment, and aggregate daily.
        """
        articles = self.fetch_news(ticker, days_back)
        if not articles:
            return pd.DataFrame(columns=['Sentiment_Score'])
            
        # Score each article
        for article in articles:
            article['score'] = self.analyze_sentiment(article['title'])
            
        df = pd.DataFrame(articles)
        # Aggregate by date (average score)
        daily_sentiment = df.groupby('date')['score'].mean().reset_index()
        daily_sentiment.rename(columns={'score': 'Sentiment_Score', 'date': 'Date'}, inplace=True)
        daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'])
        daily_sentiment.set_index('Date', inplace=True)
        
        logger.info(f"Computed daily sentiment for {len(daily_sentiment)} days.")
        return daily_sentiment

    def save_sentiment(self, df: pd.DataFrame, ticker: str):
        filepath = os.path.join(Config.DATA_DIR, f"{ticker}_sentiment.csv")
        df.to_csv(filepath)
        logger.info(f"Saved sentiment data to {filepath}")
        
    def load_sentiment(self, ticker: str) -> pd.DataFrame:
        filepath = os.path.join(Config.DATA_DIR, f"{ticker}_sentiment.csv")
        if os.path.exists(filepath):
            logger.info(f"Loading sentiment data from {filepath}")
            return pd.read_csv(filepath, index_col=0, parse_dates=True)
        else:
            return pd.DataFrame()
