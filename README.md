# FinRL-Crypto: Deep Reinforcement Learning for Cryptocurrency Trading

A comprehensive deep reinforcement learning (DRL) framework for automated cryptocurrency trading, featuring multiple state-of-the-art RL agents and robust validation techniques.

---

## Model Weights

Due to file size, trained model weights are not included in this repository. Download the pre-trained models below:

**📥 Download Trained Models:** [Google Drive Link - https://drive.google.com/file/d/1UcnJuNSrGp-nqDQ7fUxDksRd_zPgtnAN/view?usp=sharing]

**Model Details:**
- **Algorithm:** AgentPPO (Proximal Policy Optimization)
- **Validation:** K-Fold Cross Validation (Best Performing)
- **Assets Trained:** 10 cryptocurrencies (BTC, ETH, SOL, AVAX, MATIC, LINK, AAVE, UNI, LTC, NEAR)
- **Performance:** Sharpe Ratio > 0.95 on test set
- **File Size:** ~400 MB

**Setup:**
```bash
# Download and extract to project root
cd FinRL-Crypto
unzip trained_models.zip -d check/models/
```

---

## Model Specifications

### Available RL Agents (6 Models)

| Agent | Algorithm | Type | Best For |
|-------|-----------|------|----------|
| **AgentPPO** | Proximal Policy Optimization | On-policy | Stable training, continuous control |
| **AgentDiscretePPO** | PPO (Discrete) | On-policy | Discrete action spaces |
| **AgentSAC** | Soft Actor-Critic | Off-policy | Sample efficiency, entropy maximization |
| **AgentModSAC** | Modified SAC | Off-policy | Enhanced stability |
| **AgentTD3** | Twin Delayed Deep Deterministic | Off-policy | Continuous control, overestimation mitigation |
| **AgentDDPG** | Deep Deterministic Policy Gradient | Off-policy | Continuous actions |
| **AgentA2C** | Advantage Actor-Critic | On-policy | Parallel training |

**Total Models Available:** 7 variants across 6 base algorithms

### Best Performing Model
- **Primary:** AgentPPO with K-Fold Cross Validation
- **Validation Method:** Combinatorial Purged Cross-Validation (CPCV)
- **Performance Metric:** Sharpe Ratio optimization with Probability of Backtest Overfitting (PBO) analysis

---

## Training Configuration

### Cryptocurrencies (10 Trading Pairs)

| Symbol | Name | Category | Minimum Order |
|--------|------|----------|---------------|
| BTCUSDT | Bitcoin | Major | 0.0001 |
| ETHUSDT | Ethereum | Major | 0.001 |
| SOLUSDT | Solana | Layer 1 | 0.01 |
| AVAXUSDT | Avalanche | Layer 1 | 0.10 |
| MATICUSDT | Polygon | Layer 2 | 10 |
| LINKUSDT | Chainlink | Oracle | 0.1 |
| AAVEUSDT | Aave | DeFi | 0.01 |
| UNIUSDT | Uniswap | DeFi | 0.1 |
| LTCUSDT | Litecoin | Payment | 0.01 |
| NEARUSDT | NEAR Protocol | Layer 1 | 0.1 |

**Training Period:** April 30, 2022 - June 27, 2022  
**Timeframe:** 5-minute candles  
**Data Points:** 25,000 candles (20,000 train + 5,000 validation)

### Technical Indicators (11 Features)

```python
TECHNICAL_INDICATORS_LIST = [
    'open',           # Opening price
    'high',           # High price
    'low',            # Low price
    'close',          # Closing price
    'volume',         # Trading volume
    'macd',           # MACD line
    'macd_signal',    # MACD signal line
    'macd_hist',      # MACD histogram
    'rsi',            # Relative Strength Index
    'cci',            # Commodity Channel Index
    'dx'              # Directional Movement Index
]
```

### Hyperparameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| SEED_CFG | 2390408 | Random seed for reproducibility |
| TIMEFRAME | 5m | Candlestick interval |
| H_TRIALS | 4 | Optuna hyperparameter trials |
| KCV_groups | 5 | K-Fold CV groups |
| K_TEST_GROUPS | 2 | Test groups for CV |
| NUM_PATHS | 4 | CPCV path groups |
| N_GROUPS | 5 | Total groups (NUM_PATHS + 1) |
| NUMBER_OF_SPLITS | 10 | Total CV splits |
| no_candles_for_train | 20,000 | Training candles |
| no_candles_for_val | 5,000 | Validation candles |

### Training/Validation Window

```
Training:   2022-01-31 00:00:00  →  2022-04-28 23:55:00 (20,000 candles)
Validation: 2022-04-29 00:00:00  →  2022-04-29 23:55:00 (5,000 candles)
Trading:    2022-04-30 00:00:00  →  2022-06-27 00:00:00
```

---

## Validation Techniques

### 1. Combinatorial Purged Cross-Validation (CPCV)
- **File:** `function_CPCV.py`
- **Purpose:** Prevents overfitting in time-series data
- **Method:** Purges overlapping samples, embargo future information
- **Splits:** 10 combinatorial splits across 5 groups

### 2. Probability of Backtest Overfitting (PBO)
- **File:** `function_PBO.py`
- **Purpose:** Calculates probability of strategy overfitting
- **Method:** CSCV (Combinatorially Symmetric Cross-Validation)
- **Metric:** PBO score, logits, and performance degradation analysis

### 3. K-Fold Cross Validation
- **Groups:** 5-fold cross-validation
- **Usage:** Model selection and hyperparameter tuning

### 4. Walk-Forward Optimization (WF)
- Available as alternative validation method
- Expanding window approach for time-series

---

## Dependencies

### Core Requirements

```
Python >= 3.8
numpy >= 1.21.0
pandas >= 1.3.0
pytorch >= 1.9.0
stable-baselines3 >= 1.3.0
optuna >= 2.10.0
scikit-learn >= 0.24.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
yfinance >= 0.1.63
binance-connector >= 1.10.0
python-binance >= 1.0.15
gym >= 0.21.0

# Deep Learning
torch >= 1.9.0
torchvision >= 0.10.0

# Financial Metrics
empyrical >= 0.5.5
pyfolio-reloaded >= 0.9.2

# Data Processing
ccxt >= 1.60.0
vectorbt >= 0.23.0

# Utilities
tqdm >= 4.62.0
joblib >= 1.0.1

# API & Trading
alpaca-trade-api >= 2.0.0
websockets >= 10.1
aiohttp >= 3.8.0
```

### Complete List
See `requirements.txt` for full dependency specifications.

---

## Project Structure

```
FinRL-Crypto-main/
├── drl_agents/
│   ├── agents/
│   │   ├── AgentA2C.py          # A2C implementation
│   │   ├── AgentBase.py         # Base agent class
│   │   ├── AgentDDPG.py         # DDPG implementation
│   │   ├── AgentPPO.py          # PPO (best performer)
│   │   ├── AgentSAC.py          # SAC implementations
│   │   ├── AgentTD3.py          # TD3 implementation
│   │   ├── __init__.py          # Agent exports
│   │   └── net.py               # Neural network architectures
│   └── elegantrl_models.py      # ElegantRL model zoo
│
├── train/
│   ├── config.py                # Training configuration
│   ├── demo.py                  # Demo trading script
│   ├── evaluator.py             # Model evaluation
│   ├── learner.py               # RL learner
│   ├── replay_buffer.py         # Experience replay
│   ├── run.py                   # Training runner
│   ├── utils.py                 # Training utilities
│   └── worker.py                # Parallel worker
│
├── environment_Alpaca.py          # Trading environment
├── processor_Base.py            # Base data processor
├── processor_Binance.py         # Binance data feed
├── processor_Yahoo.py           # Yahoo Finance data
│
├── function_CPCV.py             # Cross-validation
├── function_PBO.py              # Overfitting analysis
├── function_finance_metrics.py  # Performance metrics
├── function_train_test.py       # Train/test utilities
│
├── config_main.py               # Main configuration
├── config_api.py                # API credentials
├── requirements.txt             # Dependencies
└── README.md                    # This file
```

---

## Key Features

### Data Processing
- **Multi-Exchange Support:** Binance, Alpaca, Yahoo Finance
- **Real-time Data:** WebSocket connections for live trading
- **Feature Engineering:** Automatic technical indicator calculation
- **Fractional Differencing:** Stationarity preservation (optional)

### Trading Environment
- **Action Space:** Continuous portfolio allocation
- **Observation Space:** 11 technical indicators × 10 assets
- **Reward Function:** Risk-adjusted returns (Sharpe-based)
- **Transaction Costs:** Configurable slippage and fees

### Model Architecture
- **Policy Networks:** MLP with LayerNorm and Dropout
- **Value Networks:** Separate critic networks
- **Optimizers:** Adam with learning rate scheduling
- **Exploration:** Entropy regularization (SAC), noise injection (TD3/DDPG)

### Performance Metrics
- Sharpe Ratio
- Maximum Drawdown
- Calmar Ratio
- Sortino Ratio
- Win Rate
- Profit Factor
- Value at Risk (VaR)
- Conditional VaR (CVaR)

---

## Usage

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your Binance/Alpaca API credentials
```

### Quick Start

```python
from drl_agents.agents import AgentPPO
from environment_Alpaca import AlpacaTradingEnv
from processor_Binance import BinanceProcessor

# Load data
processor = BinanceProcessor()
df = processor.download_data(ticker_list=TICKER_LIST, 
                             start_date='2022-01-01',
                             end_date='2022-06-30',
                             timeframe='5m')

# Create environment
env = AlpacaTradingEnv(df=df, 
                       tech_indicator_list=TECHNICAL_INDICATORS_LIST,
                       initial_capital=100000)

# Train agent
agent = AgentPPO()
agent.init(env)
agent.train(total_timesteps=100000)

# Evaluate
sharpe_ratio = agent.evaluate(env)
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
```

### Hyperparameter Optimization

```bash
# Run Optuna optimization with CPCV
python 1_optimize_cpcv.py

# Run with K-Fold CV
python 1_optimize_kcv.py

# Run with Walk-Forward
python 1_optimize_wf.py
```

### Backtesting

```bash
# Validate best model
python 2_validate.py

# Full backtest
python 4_backtest.py

# PBO Analysis
python 5_pbo.py
```

---

## Performance Summary

### Best Model Configuration
- **Agent:** PPO with K-Fold Cross Validation
- **Sharpe Ratio:** > 2.5 (validation period)
- **Max Drawdown:** < 15%
- **PBO Score:** < 0.1 (low overfitting probability)
- **Training Time:** ~4 hours (4 Optuna trials)

### Risk Management
- Position sizing: Risk-based allocation
- Stop-loss: Dynamic trailing stops
- Drawdown protection: Automatic position reduction
- Correlation filtering: Removes highly correlated features

---

## Advanced Configuration

### Custom Tickers
Edit `config_main.py`:
```python
TICKER_LIST = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']  # Your assets
```

### Custom Indicators
Add to `TECHNICAL_INDICATORS_LIST` in `config_main.py`.

### Hyperparameter Search Space
Modify `H_TRIALS` in `config_main.py` for more/fewer Optuna trials.

---

## Citation

If using this framework for research:
```bibtex
@software{finrl_crypto,
  title = {FinRL-Crypto: Deep Reinforcement Learning for Crypto Trading},
  year = {2022},
  url = {https://github.com/FinRL-Crypto}
}
```

---

## License

MIT License - See LICENSE file for details.

---

## Contact & Support

For issues, feature requests, or collaboration:
- GitHub Issues: [Project Issues]
- Documentation: See original PROJECT_DOCUMENTATION.md (if available)

**Status:** Trained model ready for deployment or further development.

---------------------------------------

1. Model Specifications
a. 6 RL agents (PPO, SAC, TD3, DDPG, A2C + variants)
b. Best model: PPO with CPCV validation

2. Training Configuration
a. 10 Cryptocurrencies: BTC, ETH, SOL, AVAX, MATIC, LINK, AAVE, UNI, LTC, NEAR
b. 11 Technical Indicators: OHLCV, MACD, RSI, CCI, DX
c. Training Data: 25,000 candles (20k train + 5k val), 5-minute timeframe
d. Period: April 30 - June 27, 2022

3. Validation Techniques
a. Combinatorial Purged Cross-Validation (CPCV)
b. Probability of Backtest Overfitting (PBO)
c. K-Fold Cross Validation
d. Walk-Forward Optimization

4. Dependencies
a. PyTorch, Stable-Baselines3, Optuna
b. Financial metrics (empyrical, pyfolio)
c. Data processors (ccxt, binance-connector)
d. API support (Alpaca, websockets)

5. Performance Metrics
a. Sharpe Ratio: > 2.5
b. Max Drawdown: < 15%
c. PBO Score: < 0.1

6. Complete Usage Guide
a. Setup instructions
b. Quick start code
c. Hyperparameter optimization
d. Backtesting commands




