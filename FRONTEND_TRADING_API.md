# FinRL-Crypto Live Trading Frontend API Specification

## 🎯 **Frontend Integration Prompt**

### **API Endpoint Specification for Live Trading Dashboard**

---

## 📡 **Core API Endpoints**

### **1. Model Loading & Status**
```javascript
// GET /api/model/status
// Response: Current model status and configuration
{
  "status": "loaded",
  "model_name": "K-Cross Validation Trial 2",
  "sharpe_ratio": 28.78,
  "pbo_score": 0.0,
  "last_training": "2026-03-08T11:59:39Z",
  "assets": ["BTCUSDT", "ETHUSDT", "SOLUSDT", ...],
  "timeframe": "5m",
  "is_paper_trading": true
}

// POST /api/model/load
// Load specific model for trading
{
  "model_id": "res_2026-03-08__11_59_39_model_KCV_ppo_5m_4H_25k",
  "mode": "paper" // or "live"
}
```

### **2. Real-Time Predictions**
```javascript
// GET /api/predictions/current
// Get current trading predictions
{
  "timestamp": "2026-03-26T02:15:00Z",
  "predictions": {
    "BTCUSDT": {
      "action": "BUY",
      "confidence": 0.85,
      "position_size": 0.15,
      "expected_return": 0.023,
      "risk_score": 0.3
    },
    "ETHUSDT": {
      "action": "HOLD", 
      "confidence": 0.45,
      "position_size": 0.0,
      "expected_return": 0.002,
      "risk_score": 0.6
    },
    "SOLUSDT": {
      "action": "SELL",
      "confidence": 0.72,
      "position_size": -0.08,
      "expected_return": -0.015,
      "risk_score": 0.4
    }
  },
  "portfolio_allocation": {
    "total_value": 100000.0,
    "cash": 25000.0,
    "positions": {
      "BTCUSDT": 15000.0,
      "ETHUSDT": 30000.0,
      "SOLUSDT": 8000.0,
      "AVAXUSDT": 12000.0,
      "others": 10000.0
    }
  }
}

// WebSocket: /ws/predictions
// Real-time prediction stream
{
  "type": "prediction_update",
  "timestamp": "2026-03-26T02:15:30Z",
  "asset": "BTCUSDT",
  "action": "BUY",
  "confidence": 0.87,
  "price": 45000.0,
  "change": "+0.5%"
}
```

### **3. Portfolio Management**
```javascript
// GET /api/portfolio/status
// Current portfolio status
{
  "total_value": 100000.0,
  "initial_value": 100000.0,
  "pnl": 0.0,
  "pnl_percentage": 0.0,
  "daily_return": 0.015,
  "sharpe_ratio": 2.34,
  "max_drawdown": -0.05,
  "positions": [
    {
      "asset": "BTCUSDT",
      "quantity": 0.33,
      "avg_price": 44500.0,
      "current_price": 45000.0,
      "pnl": 165.0,
      "pnl_percentage": 0.011
    }
  ],
  "cash": 25000.0,
  "margin_used": 0.0,
  "risk_metrics": {
    "var_95": -2500.0,
    "beta": 1.2,
    "correlation_btc": 0.85
  }
}

// POST /api/portfolio/rebalance
// Execute portfolio rebalancing
{
  "target_allocation": {
    "BTCUSDT": 0.25,
    "ETHUSDT": 0.30,
    "SOLUSDT": 0.15,
    "AVAXUSDT": 0.12,
    "others": 0.18
  },
  "rebalance_threshold": 0.05
}
```

### **4. Risk Management**
```javascript
// GET /api/risk/current
// Current risk metrics
{
  "portfolio_risk": {
    "var_95": -2500.0,
    "var_99": -4500.0,
    "max_drawdown": -0.05,
    "volatility": 0.15,
    "beta": 1.2
  },
  "position_risks": {
    "BTCUSDT": {
      "position_size": 0.15,
      "risk_contribution": 0.25,
      "correlation_portfolio": 0.85
    }
  },
  "alerts": [
    {
      "level": "warning",
      "message": "BTCUSDT position approaching limit",
      "current": 0.15,
      "limit": 0.20
    }
  ]
}

// POST /api/risk/limits
// Update risk limits
{
  "max_position_size": 0.20,
  "max_portfolio_risk": 0.25,
  "var_limit": -5000.0,
  "stop_loss_threshold": -0.10
}
```

### **5. Historical Performance**
```javascript
// GET /api/performance/history?period=1d
// Historical performance data
{
  "period": "1d",
  "data": [
    {
      "timestamp": "2026-03-26T00:00:00Z",
      "portfolio_value": 100000.0,
      "pnl": 0.0,
      "return": 0.0,
      "sharpe": 2.34,
      "drawdown": 0.0
    }
  ],
  "summary": {
    "total_return": 0.015,
    "annualized_return": 0.054,
    "volatility": 0.12,
    "sharpe_ratio": 2.34,
    "max_drawdown": -0.05,
    "win_rate": 0.65,
    "profit_factor": 1.8
  }
}

// GET /api/performance/trades
// Recent trade history
{
  "trades": [
    {
      "timestamp": "2026-03-26T01:30:00Z",
      "asset": "BTCUSDT",
      "action": "BUY",
      "quantity": 0.1,
      "price": 44500.0,
      "fees": 44.5,
      "pnl": 0.0,
      "status": "filled"
    }
  ],
  "summary": {
    "total_trades": 150,
    "winning_trades": 98,
    "losing_trades": 52,
    "win_rate": 0.653,
    "avg_win": 250.0,
    "avg_loss": -120.0,
    "profit_factor": 1.8
  }
}
```

---

## 🎨 **Frontend Component Specifications**

### **Dashboard Layout**
```jsx
// Main Dashboard Component
<Dashboard>
  <Header>
    <ModelStatus />
    <TradingModeToggle />
    <AccountInfo />
  </Header>
  
  <MainContent>
    <PortfolioOverview />
    <PredictionPanel />
    <RiskMetrics />
  </MainContent>
  
  <Sidebar>
    <AssetAllocation />
    <RecentTrades />
    <PerformanceChart />
  </Sidebar>
</Dashboard>
```

### **Real-Time Components**
```jsx
// Live Prediction Display
<PredictionPanel>
  <AssetPredictions>
    {predictions.map(asset => (
      <AssetCard 
        symbol={asset.symbol}
        action={asset.action}
        confidence={asset.confidence}
        positionSize={asset.position_size}
        expectedReturn={asset.expected_return}
        riskScore={asset.risk_score}
      />
    ))}
  </AssetPredictions>
  
  <ExecuteButton 
    onClick={executePredictions}
    disabled={!modelLoaded || isLiveTrading}
  />
</PredictionPanel>

// Portfolio Status Display
<PortfolioOverview>
  <TotalValue value={portfolio.total_value} change={daily_return} />
  <PnLChart data={historical_pnl} />
  <PositionList positions={portfolio.positions} />
  <RiskAlerts alerts={risk.alerts} />
</PortfolioOverview>
```

---

## 🔄 **WebSocket Integration**

### **Real-Time Data Streams**
```javascript
// WebSocket connections for live updates
const wsConnections = {
  predictions: 'ws://localhost:8000/ws/predictions',
  portfolio: 'ws://localhost:8000/ws/portfolio',
  prices: 'ws://localhost:8000/ws/prices',
  trades: 'ws://localhost:8000/ws/trades'
};

// Message handlers
wsConnections.predictions.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updatePredictions(data);
  showNotification(`New prediction for ${data.asset}: ${data.action}`);
};

wsConnections.portfolio.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updatePortfolio(data);
  updateCharts(data);
};
```

---

## 🛡️ **Security & Authentication**

### **API Security**
```javascript
// Authentication headers
const headers = {
  'Authorization': `Bearer ${api_token}`,
  'X-API-Key': api_key,
  'Content-Type': 'application/json'
};

// Rate limiting
const rateLimits = {
  predictions: '10/minute',
  trades: '100/minute',
  portfolio: '60/minute'
};

// Permission levels
const permissions = {
  read_only: ['GET'],
  trader: ['GET', 'POST:/api/portfolio/rebalance'],
  admin: ['GET', 'POST', 'PUT', 'DELETE']
};
```

---

## 📱 **Responsive Design**

### **Mobile Optimization**
```css
/* Mobile-first responsive design */
.dashboard {
  display: grid;
  grid-template-areas: 
    "header header"
    "main sidebar"
    "footer footer";
}

@media (max-width: 768px) {
  .dashboard {
    grid-template-areas: 
      "header"
      "main"
      "sidebar"
      "footer";
  }
  
  .prediction-panel {
    flex-direction: column;
  }
  
  .asset-cards {
    display: block;
    overflow-x: auto;
  }
}
```

---

## 🎯 **User Experience Features**

### **Interactive Elements**
```jsx
// Interactive prediction controls
<PredictionControls>
  <ModelSelector 
    models={available_models}
    selected={current_model}
    onChange={switchModel}
  />
  
  <TimeframeSelector 
    options={['1m', '5m', '15m', '1h']}
    selected={current_timeframe}
    onChange={changeTimeframe}
  />
  
  <RiskSlider 
    min={0}
    max={1}
    step={0.1}
    value={risk_tolerance}
    onChange={updateRiskTolerance}
  />
</PredictionControls>

// Real-time notifications
<NotificationCenter>
  {notifications.map(notification => (
    <Notification 
      type={notification.type}
      message={notification.message}
      timestamp={notification.timestamp}
      actions={notification.actions}
    />
  ))}
</NotificationCenter>
```

---

## 🚀 **Implementation Guide**

### **Frontend Stack Recommendation**
```json
{
  "framework": "React.js with TypeScript",
  "state_management": "Redux Toolkit + RTK Query",
  "charts": "Chart.js / D3.js",
  "websocket": "Socket.io-client",
  "styling": "Tailwind CSS + Material-UI",
  "testing": "Jest + React Testing Library",
  "build": "Vite"
}
```

### **Backend Integration**
```javascript
// API client setup
import { createApi } from '@reduxjs/toolkit/query/react';

export const tradingApi = createApi({
  reducerPath: 'tradingApi',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/',
    prepareHeaders: (headers, { getState }) => {
      headers.set('authorization', `Bearer ${getState().auth.token}`);
      return headers;
    },
  }),
  tagTypes: ['Portfolio', 'Predictions', 'Risk'],
  endpoints: (builder) => ({
    getPredictions: builder.query<Predictions, void>({
      query: () => 'predictions/current',
      providesTags: ['Predictions'],
    }),
    getPortfolio: builder.query<Portfolio, void>({
      query: () => 'portfolio/status',
      providesTags: ['Portfolio'],
    }),
    executeTrades: builder.mutation<TradeResponse, TradeRequest>({
      query: (tradeRequest) => ({
        url: 'trades/execute',
        method: 'POST',
        body: tradeRequest,
      }),
      invalidatesTags: ['Portfolio'],
    }),
  }),
});
```

---

## 📊 **Performance Metrics Display**

### **Key Performance Indicators**
```jsx
<PerformanceMetrics>
  <KPI title="Sharpe Ratio" value={2.34} change="+0.15" />
  <KPI title="Win Rate" value="65.3%" change="+2.1%" />
  <KPI title="Max Drawdown" value="-5.2%" change="-0.8%" />
  <KPI title="Daily Return" value="+1.5%" change="+0.3%" />
  
  <PerformanceChart 
    data={historical_performance}
    type="line"
    metrics={['return', 'sharpe', 'drawdown']}
  />
  
  <RiskGauge 
    value={current_risk}
    max={max_risk_limit}
    thresholds={[0.5, 0.7, 0.9]}
  />
</PerformanceMetrics>
```

---

## ⚠️ **Error Handling & User Feedback**

### **Error States**
```jsx
<ErrorBoundary>
  {error && (
    <ErrorMessage>
      <Icon name="warning" />
      <Text>Trading system temporarily unavailable</Text>
      <Button onClick={retry}>Retry</Button>
    </ErrorMessage>
  )}
  
  {loading && <LoadingSpinner />}
  
  {data && <TradingDashboard data={data} />}
</ErrorBoundary>

// User feedback system
<ToastContainer>
  {toasts.map(toast => (
    <Toast 
      type={toast.type}
      message={toast.message}
      duration={toast.duration}
      action={toast.action}
    />
  ))}
</ToastContainer>
```

---

## 🎯 **Complete Frontend Integration Prompt**

**Use this specification to build a comprehensive live trading dashboard that integrates seamlessly with your FinRL-Crypto backend system. The frontend should provide:**

1. **Real-time predictions** from your trained K-Cross Validation model
2. **Portfolio management** with live updates
3. **Risk monitoring** with alert systems
4. **Performance analytics** with interactive charts
5. **Trade execution** with safety controls
6. **Mobile-responsive** design for trading on any device

**The system should handle paper trading and live trading modes with proper authentication and security measures.**
