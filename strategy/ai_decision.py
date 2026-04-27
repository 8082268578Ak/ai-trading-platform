import pandas as pd

def analyze_trend(row: pd.Series) -> tuple[int, str]:
    """
    Analyzes the trend using basic technical indicators.
    Returns: (trend_score, trend_reason_string)
    """
    # Use standard ta library features if available
    rsi = row.get('momentum_rsi', 50)
    macd_diff = row.get('trend_macd_diff', 0)
    
    trend_score = 0
    reasons = []
    
    # RSI Logic
    if rsi > 60:
        trend_score += 0.5
        reasons.append(f"bullish RSI ({rsi:.1f})")
    elif rsi < 40:
        trend_score -= 0.5
        reasons.append(f"bearish RSI ({rsi:.1f})")
    
    # MACD Logic
    if macd_diff > 0:
        trend_score += 0.5
        reasons.append("positive MACD momentum")
    elif macd_diff < 0:
        trend_score -= 0.5
        reasons.append("negative MACD momentum")
        
    # Compile Final Trend Score
    final_score = 1 if trend_score > 0 else (-1 if trend_score < 0 else 0)
    
    if final_score == 1:
        trend_str = "Strong uptrend detected with " + " and ".join(reasons) + "."
    elif final_score == -1:
        trend_str = "Downtrend confirmed with " + " and ".join(reasons) + "."
    else:
        trend_str = "Sideways trend with mixed indicators."
        
    return final_score, trend_str

def generate_ai_decision(row: pd.Series, predicted_col: str, sentiment_col: str) -> dict:
    """
    Combines trend analysis, price prediction, and news sentiment into a final weighted signal.
    """
    current_price = row.get('Close', 0.0)
    predicted_price = row.get(predicted_col, current_price)
    sentiment = row.get(sentiment_col, 0.0)
    
    # 1. Trend Analysis
    trend_score, trend_explanation = analyze_trend(row)
    
    # 2. Prediction Score
    pct_diff = 0.0
    if current_price > 0:
        pct_diff = ((predicted_price - current_price) / current_price) * 100
        
    if predicted_price > current_price:
        pred_score = 1
        pred_explanation = f"Model predicts price increase of {pct_diff:.2f}%."
    elif predicted_price < current_price:
        pred_score = -1
        pred_explanation = f"Model predicts price drop of {abs(pct_diff):.2f}%."
    else:
        pred_score = 0
        pred_explanation = "Model predicts no significant price change."
        
    # 3. Sentiment Score
    if sentiment > 0.2:
        sent_score = 1
        sent_explanation = "positive news sentiment"
    elif sentiment < -0.2:
        sent_score = -1
        sent_explanation = "negative news sentiment"
    else:
        sent_score = 0
        sent_explanation = "neutral sentiment"
        
    # 4. Final Weighted Decision
    # Weighting: Trend (40%), Prediction (40%), Sentiment (20%)
    total_score = (trend_score * 0.4) + (pred_score * 0.4) + (sent_score * 0.2)
    
    if total_score >= 0.4:
        signal_text = "BUY"
        int_signal = 1
    elif total_score <= -0.4:
        signal_text = "SELL"
        int_signal = -1
    else:
        signal_text = "HOLD"
        int_signal = 0
        
    # 5. Confidence Score
    confidence = abs(total_score)
    
    # Risk Level Based on Signal Conviction
    if confidence >= 0.8:
        risk_level = "Low"
    elif confidence >= 0.5:
        risk_level = "Medium"
    else:
        risk_level = "High"
        
    # 6. Explanation Generator
    if signal_text == "BUY":
        explanation = f"📈 BUY Signal: {trend_explanation} {pred_explanation} Supported by {sent_explanation}."
    elif signal_text == "SELL":
        explanation = f"📉 SELL Signal: {trend_explanation} {pred_explanation} Supported by {sent_explanation}."
    else:
        explanation = f"⚠️ HOLD Signal: {trend_explanation} {pred_explanation} Combined with {sent_explanation}."
        
    return {
        "signal_text": signal_text,
        "int_signal": int_signal,
        "confidence": confidence,
        "reason": explanation,
        "risk_level": risk_level,
        "total_score": total_score
    }
