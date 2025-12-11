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

import scipy.io
import pandas as pd
import numpy as np
import os

def load_data(file_path):
    """
    NASAバッテリーデータ(.mat)を読み込み、Pandas DataFrameに変換する関数
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None

    mat = scipy.io.loadmat(file_path)
    
    # ファイル名から変数を特定 (例: 'B0005.mat' -> 'B0005')
    filename = os.path.basename(file_path).split('.')[0]
    
    if filename not in mat:
        print(f"Key '{filename}' not found in mat file. Available keys: {mat.keys()}")
        return None

    data = mat[filename]
    
    # データの階層構造: data[0][0]['cycle'][0] -> 各サイクルの配列
    cycles = data[0][0]['cycle'][0]
    
    parsed_data = []

    for i, cycle in enumerate(cycles):
        # 各サイクルの情報を抽出
        cycle_type = str(cycle['type'][0]) # 'charge', 'discharge', 'impedance'
        ambient_temp = float(cycle['ambient_temperature'][0])
        time_stamp = str(cycle['time'][0])
        
        # 'data'フィールド（実際の計測値）の中身を抽出
        # 構造: cycle['data'] -> (1,1) struct -> 各フィールド
        measurements = cycle['data']
        
        if measurements.size == 0:
            continue
            
        # 放電(discharge)データのみ、容量(Capacity)が含まれているので抽出対象とする
        # 劣化予測では主に放電サイクルが重要
        if cycle_type == 'discharge':
            try:
                # データの取り出し（MATLAB構造体の入れ子が深いため注意）
                capacity = float(measurements[0][0]['Capacity'][0])
                voltage_battery = measurements[0][0]['Voltage_measured'][0]
                current_battery = measurements[0][0]['Current_measured'][0]
                temp_battery = measurements[0][0]['Temperature_measured'][0]
                time_sec = measurements[0][0]['Time'][0]
                
                # 1サイクル内の平均値や最大値などを特徴量として簡易抽出する例
                # (時系列全体を持ちたい場合は設計を変えるが、まずは要約統計量でSOHを見る)
                row = {
                    'cycle_id': i + 1,
                    'type': cycle_type,
                    'ambient_temperature': ambient_temp,
                    'capacity': capacity, # これがSOHの正解ラベルになる
                    'avg_voltage': np.mean(voltage_battery),
                    'min_voltage': np.min(voltage_battery),
                    'avg_temp': np.mean(temp_battery),
                    'max_temp': np.max(temp_battery),
                    'discharge_time': time_sec[-1] - time_sec[0]
                }
                parsed_data.append(row)
            except Exception as e:
                # データ形式が一部異なる場合のエラーハンドリング
                pass

    df = pd.DataFrame(parsed_data)
    return df

# --- メイン実行部 ---
if __name__ == "__main__":
    base_dir = "data/nasa_battery"
    target_file = "B0005.mat"
    file_path = os.path.join(base_dir, target_file)

    print(f"Loading {file_path} ...")
    df = load_data(file_path)

    if df is not None:
        print("読み込み成功！")
        print(f"データサイズ: {df.shape}")
        print(df.head())
        
        # 保存しておく（次回からcsvで読めるように）
        output_csv = os.path.join(base_dir, "B0005_summary.csv")
        df.to_csv(output_csv, index=False)
        print(f"CSVに保存しました: {output_csv}")
    else:
        print("データの読み込みに失敗しました。")


# テストコード（ファイル配置後に実行）
file_path = os.path.join(base_dir, 'B0005.mat')
if os.path.exists(file_path):
    data_b0005 = load_mat_data(file_path)
else:
    print("ファイルが見つかりません。配置を完了してください。")
