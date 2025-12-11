import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
import zipfile
import os
import scipy.io

# 1. データのダウンロードと解凍
data_url = "https://ti.arc.nasa.gov/c/5/"  # NASA PCoE dataset link (direct download often changes, using manual download instruction context if needed, but let's try a direct approach or Kaggle instruction usually)
# 補足: NASAの元リンクが不安定な場合があるため、Kaggleなどで整理されたcsvを使うのが実務的ですが、
# 今回は「元データから加工できる力」を示すため、MATLAB形式(.mat)をパースする工程を経験することをお勧めします。

# まずは作業ディレクトリを作成
base_dir = "data/nasa_battery"
os.makedirs(base_dir, exist_ok=True)

print("指示: 以下のURLから 'BatteryAgingARC-FY08Q4.zip' をダウンロードし、")
print("data/nasa_battery フォルダに解凍してください。")
print("URL: https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/")
print("※ '5. Battery Data Set' という項目です。")

# ここでは、データが既に 'data/nasa_battery/B0005.mat' にあると仮定して
# MATLABファイルを読み込む関数を定義します。これはデータエンジニアリング力の重要なアピールになります。

def load_mat_data(file_path):
    mat = scipy.io.loadmat(file_path)
    data = mat['data']
    
    # 複雑なネスト構造になっているため、必要な部分（cycle, type, ambient_temperature, time, data）を抽出
    # 構造解析のロジックは少し複雑ですが、まずは読み込めるか確認します
    print(f"Loaded: {file_path}")
    print(f"Data shape: {data.shape}")
    return data

# テストコード（ファイル配置後に実行）
# file_path = os.path.join(base_dir, 'B0005.mat')
# if os.path.exists(file_path):
#     data_b0005 = load_mat_data(file_path)
# else:
#     print("ファイルが見つかりません。配置を完了してください。")
