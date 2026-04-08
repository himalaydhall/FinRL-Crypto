# FinRL-Crypto Best Agent Package

## Champion Model: K-Cross Validation (Sharpe: 28.78)

This package contains the best performing cryptocurrency trading agent from the FinRL-Crypto project.

## Package Contents

- `model/` - Trained agent and study results
- `config_main.py` - Configuration settings  
- `deploy_agent.py` - Deployment script
- `results/` - Performance charts and metrics
- `drl_agents/` - Deep RL agent implementations
- `requirements.txt` - Python dependencies

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Keys:**
   Edit `config_api.py` with your exchange API keys

3. **Deploy Agent:**
   ```bash
   python deploy_agent.py
   ```

## Performance Highlights

- **Sharpe Ratio**: 28.78 (Exceptional)
- **PBO Score**: 0.0% (No overfitting)
- **Validation**: K-Cross Validation (5 folds)
- **Assets**: 10 major cryptocurrencies
- **Timeframe**: 5-minute intervals

## Important Notes

- Start with **paper trading** before real money
- Monitor performance continuously
- Retrain periodically with fresh data
- Never invest more than you can afford to lose

## Documentation

See `AGENTS_SUMMARY.md` for detailed analysis of all trained agents.

---
*Generated: 2026-03-18 02:55:51*
