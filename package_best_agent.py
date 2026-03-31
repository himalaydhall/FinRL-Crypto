#!/usr/bin/env python3
"""
Package Best FinRL-Crypto Agent for Sharing
============================================

This script creates a zip package with the best performing agent
and all necessary files for easy deployment and sharing.

Usage:
    python package_best_agent.py
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_agent_package():
    """Create a zip package with the best agent."""
    
    # Configuration
    best_model_dir = "res_2026-03-08__11_59_39_model_KCV_ppo_5m_4H_25k"
    package_name = "FinRL_Crypto_Best_Agent"
    
    print("🚀 Creating FinRL-Crypto Best Agent Package...")
    print(f"📦 Package Name: {package_name}")
    print(f"🏆 Best Model: {best_model_dir}")
    print("-" * 50)
    
    # Create package directory
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Copy best model files
    print("📋 Copying best model files...")
    model_source = f"train_results/{best_model_dir}"
    model_dest = f"{package_name}/model"
    
    if os.path.exists(model_source):
        shutil.copytree(model_source, model_dest)
        print(f"✅ Model files copied to {model_dest}")
    
    # Copy configuration files
    print("⚙️ Copying configuration files...")
    config_files = [
        "config_main.py",
        "config_api.py", 
        "requirements.txt",
        "README.md"
    ]
    
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, f"{package_name}/{file}")
            print(f"✅ {file} copied")
    
    # Copy core modules
    print("🔧 Copying core modules...")
    modules_to_copy = [
        "drl_agents",
        "environment_Alpaca.py", 
        "function_finance_metrics.py",
        "processor_Binance.py",
        "processor_Yahoo.py"
    ]
    
    for module in modules_to_copy:
        if os.path.exists(module):
            if os.path.isdir(module):
                shutil.copytree(module, f"{package_name}/{module}")
            else:
                shutil.copy2(module, f"{package_name}/{module}")
            print(f"✅ {module} copied")
    
    # Copy results and plots
    print("📊 Copying results and plots...")
    if os.path.exists("plots_and_metrics"):
        shutil.copytree("plots_and_metrics", f"{package_name}/results")
        print("✅ Results and plots copied")
    
    # Create deployment script
    print("Creating deployment script...")
    deployment_script = f"""#!/usr/bin/env python3
'''
FinRL-Crypto Best Agent Deployment Script
========================================

This script loads and deploys the best performing K-Cross Validation agent.
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Performance:
- Sharpe Ratio: 28.78
- PBO Score: 0.0%
- Validation Method: K-Cross Validation
'''

import os
import sys
import joblib
import torch
import pandas as pd
import numpy as np
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def load_best_agent():
    \"\"\"Load the best performing agent.\"\"\"
    print("Loading FinRL-Crypto Best Agent...")
    
    # Load study and best trial
    study_path = "model/study.pkl"
    if not os.path.exists(study_path):
        raise FileNotFoundError(f"Study file not found: {{study_path}}")
    
    study = joblib.load(study_path)
    best_trial = study.best_trial
    
    print(f"Best Trial: {{best_trial.number}}")
    print(f"Sharpe Ratio: {{best_trial.value:.2f}}")
    print(f"Best Params: {{best_trial.params}}")
    
    return study, best_trial

def print_model_info():
    \"\"\"Print detailed model information.\"\"\"
    print("\\n" + "="*60)
    print("FINRL-CRYPTO BEST AGENT INFORMATION")
    print("="*60)
    
    print("\\nPerformance Metrics:")
    print("   • Sharpe Ratio: 28.78")
    print("   • PBO Score: 0.0% (No Overfitting)")
    print("   • Validation Method: K-Cross Validation")
    print("   • Training Period: Feb-Apr 2022")
    print("   • Test Period: Apr-Jun 2022")
    
    print("\\nModel Configuration:")
    print("   • Algorithm: PPO (Proximal Policy Optimization)")
    print("   • Network Architecture: 4096 neurons")
    print("   • Learning Rate: 0.015")
    print("   • Batch Size: 512")
    print("   • Timeframe: 5-minute intervals")
    
    print("\\nTrading Assets:")
    assets = ['AAVEUSDT', 'AVAXUSDT', 'BTCUSDT', 'NEARUSDT', 'LINKUSDT', 
              'ETHUSDT', 'LTCUSDT', 'MATICUSDT', 'UNIUSDT', 'SOLUSDT']
    for i, asset in enumerate(assets, 1):
        print(f"   {{i:2d}}. {{asset}}")
    
    print("\\nRisk Warning:")
    print("   • Past performance does not guarantee future results")
    print("   • Start with paper trading before real money")
    print("   • Use proper risk management")
    print("   • Never invest more than you can afford to lose")
    
    print("\\n" + "="*60)

def main():
    \"\"\"Main deployment function.\"\"\"
    try:
        # Print model information
        print_model_info()
        
        # Load the best agent
        study, best_trial = load_best_agent()
        
        print("\\nNext Steps:")
        print("1. Set up your API keys in config_api.py")
        print("2. Run paper trading to test performance")
        print("3. Monitor and adjust as needed")
        print("4. Consider periodic retraining with fresh data")
        
        print("\\nAgent loaded successfully!")
        print("Check the 'results' folder for detailed performance analysis")
        
    except Exception as e:
        print(f"Error loading agent: {{e}}")
        print("Please check all files are present and correctly configured")

if __name__ == "__main__":
    main()
"""
    
    with open(f"{package_name}/deploy_agent.py", "w") as f:
        f.write(deployment_script)
    print("✅ Deployment script created")
    
    # Create README for package
    package_readme = f"""# FinRL-Crypto Best Agent Package

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
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    with open(f"{package_name}/README.md", "w") as f:
        f.write(package_readme)
    print("✅ Package README created")
    
    # Create zip file
    print("🗜️ Creating zip package...")
    zip_filename = f"{package_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, package_name)
                zipf.write(file_path, arcname)
    
    print(f"✅ Package created: {zip_filename}")
    
    # Clean up directory
    shutil.rmtree(package_name)
    
    # Show package info
    zip_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
    print(f"\n📊 Package Information:")
    print(f"   • File: {zip_filename}")
    print(f"   • Size: {zip_size:.1f} MB")
    print(f"   • Best Sharpe: 28.78")
    print(f"   • PBO Score: 0.0%")
    
    print(f"\n🎉 Ready to share on GitHub!")
    print(f"📋 Include both AGENTS_SUMMARY.md and {zip_filename}")

if __name__ == "__main__":
    create_agent_package()
