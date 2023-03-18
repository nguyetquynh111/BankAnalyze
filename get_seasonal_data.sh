#!/bin/sh
source /Users/quynh.nguyen111/miniconda3/etc/profile.d/conda.sh 
conda activate date_engineer
python BankAnalyze/no-nhom-theo-nam.py
python BankAnalyze/no-nhom-theo-quy.py
python BankAnalyze/shareholder.py
python thong-tin-tai-chinh-theo-nam.py
python thong-tin-tai-chinh-theo-quy.py
python update_seasonal.py