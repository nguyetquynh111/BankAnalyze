#!/bin/sh
source /Users/quynh.nguyen111/miniconda3/etc/profile.d/conda.sh 
conda activate date_engineer
python BankAnalyze/stockhistory.py
python BankAnalyze/update_daily.py