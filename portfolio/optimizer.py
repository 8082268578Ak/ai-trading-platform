import pandas as pd
import json
import os
from config.settings import Config
from utils.logger import get_logger

logger = get_logger("portfolio.optimizer")

class PortfolioOptimizer:
    @staticmethod
    def allocate_capital(df_summary: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
        """
        Implements Heuristic Weighted Allocation (Option A).
        Returns the updated dataframe with 'Allocation_%' and a metadata dictionary.
        """
        if df_summary.empty:
            return df_summary, {}
            
        allocations = []
        raw_weights = []
        
        for _, row in df_summary.iterrows():
            signal = row.get("Signal", "HOLD")
            expected_return = row.get("Expected_Return_%", 0) / 100.0  # convert % back to decimal
            confidence = row.get("Confidence", 0.0)
            risk = row.get("Annualized_Risk", 0.1) # Avoid division by zero
            
            if risk <= 0.0:
                risk = 0.1
                
            # Only allocate if BUY or HOLD. SELL gets 0 allocation.
            if signal == "SELL":
                raw_weight = 0.0
            else:
                # Option A Formula: (expected_return * confidence) / risk
                raw_weight = max(0.0, (expected_return * confidence) / risk)
                
                # Boost BUY signals
                if signal == "BUY":
                    raw_weight *= 2.0
                    
            raw_weights.append(raw_weight)
            
        # Normalize weights
        total_weight = sum(raw_weights)
        
        if total_weight > 0:
            allocations = [(w / total_weight) * 100.0 for w in raw_weights]
        else:
            # If all weights are 0, allocate 0
            allocations = [0.0] * len(raw_weights)
            
        df_summary['Allocation_%'] = [round(a, 2) for a in allocations]
        
        # Calculate Portfolio Metrics
        total_expected_return = sum((df_summary['Expected_Return_%'] / 100.0) * (df_summary['Allocation_%'] / 100.0)) * 100
        total_risk = sum(df_summary['Annualized_Risk'] * (df_summary['Allocation_%'] / 100.0))
        
        # Diversification score (1 = perfectly even, approaches 0 if concentrated)
        num_allocated = sum(1 for a in allocations if a > 0)
        div_score = num_allocated / len(allocations) if len(allocations) > 0 else 0
        
        # Generate AI Recommendation
        sorted_df = df_summary.sort_values(by="Allocation_%", ascending=False)
        best_asset = sorted_df.iloc[0] if not sorted_df.empty and sorted_df.iloc[0]['Allocation_%'] > 0 else None
        worst_asset = df_summary.sort_values(by="Confidence", ascending=True).iloc[0] if not df_summary.empty else None
        
        recommendation = ""
        if best_asset is not None:
            recommendation += f"Allocate {best_asset['Allocation_%']:.1f}% heavily to {best_asset['Symbol']} due to high expected return and strong confidence. "
        else:
            recommendation += "No assets currently meet the criteria for capital allocation. Stay in cash. "
            
        if worst_asset is not None and worst_asset['Signal'] == 'SELL':
            recommendation += f"Avoid {worst_asset['Symbol']} entirely due to {worst_asset.get('Risk_Category', 'High')} downside risk and a SELL signal."
        
        metadata = {
            "Total_Expected_Return_%": round(total_expected_return, 2),
            "Total_Risk": round(total_risk, 4),
            "Diversification_Score": round(div_score, 2),
            "Recommendation": recommendation.strip()
        }
        
        # Save metadata to JSON
        metadata_path = os.path.join(Config.DATA_DIR, "portfolio_metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=4)
            
        logger.info("Portfolio optimization completed and metadata saved.")
        return df_summary, metadata
