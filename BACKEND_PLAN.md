# FinRL-Crypto Backend Development Plan

## Overview
Convert the trained RL models into a production backend API that provides trading signals, tracks performance, and continuously learns from new market data.

---

## Phase 1: Backend Foundation (Week 1)

### 1.1 API Framework Setup
**What to build:**
- FastAPI application structure
- Health check endpoint (`GET /health`)
- Configuration management (Pydantic settings)
- Logging and error handling

**Files to create:**
```
backend/
├── main.py              # FastAPI entry point
├── config.py            # Settings management
├── logger.py            # Structured logging
└── dependencies.py      # Shared dependencies (DB, Redis)
```

### 1.2 Data Layer
**What to build:**
- SQLite/PostgreSQL for signal history
- Redis for caching recent predictions
- Data models: Signal, Trade, Performance

**Database Schema:**
```sql
signals:
  - id, timestamp, symbol, action, confidence, price, model_version

trades:
  - id, signal_id, executed_price, pnl, status

performance:
  - date, total_pnl, win_rate, sharpe_ratio
```

---

## Phase 2: Model Inference Engine (Week 1-2)

### 2.1 Model Loader
**What to build:**
- Load trained `.pth` / `.pkl` model files
- Model versioning system
- Switch between PPO/SAC/TD3 at runtime
- Fallback mechanism if model fails

**Key Functions:**
```python
class ModelManager:
    def load_model(agent_type: str, version: str) -> Agent
    def predict(observation: np.array) -> Action
    def get_confidence(action: Action) -> float
```

### 2.2 Feature Engineering Pipeline
**What to build:**
- Real-time indicator calculation (MACD, RSI, CCI)
- Data normalization (match training distribution)
- Feature cache for efficiency
- Validation that input data is complete

**Files:**
```
backend/
├── inference/
│   ├── __init__.py
│   ├── model_manager.py      # Load & serve models
│   ├── feature_engineering.py # Real-time indicators
│   └── predictor.py           # Prediction pipeline
```

---

## Phase 3: Prediction API (Week 2)

### 3.1 Signal Generation Endpoint
**Endpoint:** `POST /api/v1/predict`

**Request:**
```json
{
  "symbols": ["BTCUSDT", "ETHUSDT"],
  "timeframe": "5m",
  "model": "ppo-v1"
}
```

**Response:**
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "signals": [
    {
      "symbol": "BTCUSDT",
      "action": "BUY",
      "confidence": 0.78,
      "allocation": 0.35,
      "current_price": 43250.50,
      "indicators": {
        "rsi": 45.2,
        "macd": 125.3,
        "trend": "bullish"
      }
    }
  ],
  "model_version": "ppo-kcv-v1",
  "inference_time_ms": 45
}
```

### 3.2 Signal Interpretation
**Convert continuous allocation to discrete signals:**
```python
def allocation_to_signal(allocation: float, threshold: float = 0.1) -> str:
    """
    allocation > 0.1 → BUY (increase position)
    allocation < -0.1 → SELL (decrease position)
    -0.1 <= allocation <= 0.1 → HOLD
    """
```

### 3.3 Confidence Score Calculation
**Methods:**
1. **Policy Entropy**: Lower entropy = higher confidence
2. **Value Estimation**: Critic network estimates return
3. **Historical Accuracy**: Backtest performance on recent data

---

## Phase 4: Live Data Pipeline (Week 2-3)

### 4.1 Market Data Ingestion
**What to build:**
- Binance WebSocket connection for real-time prices
- Historical data fetcher for backfilling
- Data validation and cleaning
- Automatic reconnection on disconnect

**Files:**
```
backend/
├── data/
│   ├── __init__.py
│   ├── binance_client.py    # WebSocket + REST API
│   ├── data_buffer.py       # Ring buffer for recent data
│   └── data_validator.py    # Data quality checks
```

### 4.2 Scheduled Data Updates
**What to build:**
- APScheduler for periodic tasks
- Fetch latest candles every 5 minutes
- Update feature cache
- Trigger predictions on new data

---

## Phase 5: Online Learning (Week 3-4)

### 5.1 Experience Collection
**What to build:**
- Store (state, action, reward, next_state) tuples
- Calculate reward from actual trade performance
- Replay buffer with priority sampling

### 5.2 Model Updates
**What to build:**
- Background training job (daily/weekly)
- Fine-tune on recent market data
- A/B testing: old vs new model
- Rollback if performance degrades

**Training Trigger:**
```python
async def online_learning_job():
    # Runs every Sunday at 2 AM
    new_data = fetch_last_week_data()
    replay_buffer.add(new_data)
    
    # Fine-tune for 1000 steps
    agent.train(replay_buffer, steps=1000)
    
    # Evaluate vs production model
    if new_model_sharpe > current_sharpe * 1.05:
        deploy_new_model()
```

---

## Phase 6: Portfolio & Risk Management (Week 4)

### 6.1 Portfolio Tracker
**What to track:**
- Current positions per asset
- Cash balance
- Total portfolio value
- Unrealized P&L

**Endpoints:**
- `GET /api/v1/portfolio` - Current holdings
- `GET /api/v1/performance` - Returns metrics
- `GET /api/v1/trades` - Trade history

### 6.2 Risk Controls
**What to implement:**
- Max position size per asset (e.g., 20%)
- Stop-loss triggers
- Drawdown protection (reduce size in drawdown)
- Correlation checks (avoid correlated bets)

---

## Phase 7: Monitoring & Operations (Week 4-5)

### 7.1 Monitoring
**What to track:**
- Prediction latency (should be < 100ms)
- Model prediction distribution
- Data freshness (last update timestamp)
- API error rates

**Tools:**
- Prometheus metrics
- Grafana dashboards
- Alerting on critical failures

### 7.2 Logging
**Log events:**
- Every prediction (symbol, signal, confidence)
- Every trade execution
- Model updates
- Data quality issues

---

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/predict` | Get trading signals |
| GET | `/api/v1/signals` | Signal history |
| GET | `/api/v1/portfolio` | Current portfolio |
| GET | `/api/v1/performance` | Performance metrics |
| POST | `/api/v1/trade` | Record trade execution |
| GET | `/api/v1/models` | Available models |
| POST | `/api/v1/models/switch` | Switch active model |

---

## What You Need to Provide

### 1. API Keys (Required)
**Binance (Primary):**
- Sign up at: https://www.binance.com/en/register
- Create API Key: https://www.binance.com/en/my/settings/api-management
- Permissions needed: "Enable Reading" + "Enable Spot & Margin Trading" (for live trading later)
- IP whitelist: Your server IP (or 0.0.0.0/0 for testing)

**Alpaca (Optional - alternative data source):**
- Sign up at: https://app.alpaca.markets/signup
- Paper trading keys: https://app.alpaca.markets/paper/dashboard
- Use paper keys for testing (free, no real money)

### 2. Infrastructure (Required)
**Minimum:**
- Python 3.8+ environment
- 4GB RAM (8GB recommended for training)
- 50GB storage (for data + models)

**Optional but recommended:**
- Redis (for caching predictions)
- PostgreSQL (for production data storage)
- Docker (for deployment)

### 3. Trained Model Files (Critical)
**You need:**
- Best performing model weights (`.pth` or `.pkl` files)
- Model configuration (hyperparameters used)
- If you don't have these, we need to retrain

**Check:**
```bash
# Look for model files in your project
find . -name "*.pth" -o -name "*.pkl" -o -name "*agent*"
```

### 4. Trading Configuration (Your Input)
**Tell me:**
- Initial capital amount (e.g., $10,000)
- Risk tolerance (conservative/moderate/aggressive)
- Trading frequency (5min/15min/1h)
- Which assets to trade (stick to the 10 trained ones?)
- Paper trading first? (recommended)

---

## Estimated Timeline

| Phase | Duration | Key Deliverable |
|-------|----------|-----------------|
| 1 | 3-4 days | Running FastAPI server |
| 2 | 4-5 days | Model inference working |
| 3 | 3-4 days | Prediction API live |
| 4 | 4-5 days | Real-time data flowing |
| 5 | 5-7 days | Online learning active |
| 6 | 3-4 days | Portfolio tracking |
| 7 | 3-4 days | Monitoring & alerts |

**Total: 4-5 weeks** for production-ready backend

---

## First Step Decision

**Do you have trained model files?** (`.pth`, `.pkl`, or similar)
- **YES** → Start building backend immediately
- **NO** → We need to retrain first (adds 1-2 weeks)

Let me know and I'll start implementation!
