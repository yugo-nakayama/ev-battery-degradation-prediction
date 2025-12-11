# EV Battery Degradation Prediction & RUL Forecasting
### EVバッテリーの劣化特性予測および残寿命(RUL)予測モデル

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Library](https://img.shields.io/badge/Library-PyTorch%20%7C%20LightGBM-orange)
![Status](https://img.shields.io/badge/Status-Development-green)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## 📖 概要 (Overview)
電気自動車（EV）の普及において、バッテリーの劣化状態（SOH: State of Health）と残寿命（RUL: Remaining Useful Life）の正確な予測は、**車両の残価設定、リユース事業の収益性、および安全性担保**における最重要課題です。

本プロジェクトでは、NASA PCoEの公開データセットを使用し、リチウムイオン電池の充放電サイクルデータからSOHを高精度に予測する機械学習モデルを構築しました。単なる精度追求だけでなく、**製造業の現場導入を見据えた「ロバスト性」と「運用コスト」の評価**も行っています。

## 🎯 目的 (Objectives)
1.  **高精度な寿命予測**: 初期の充放電サイクルデータから、将来のSOH推移を予測する（目標RMSE < 1.5%）。
2.  **ビジネスインパクトの可視化**: 過剰な安全マージン削減による推定コストダウン効果を試算する。
3.  **実運用への適用性検証**: ノイズに対する頑健性や、計算リソース（推論コスト）の最適化を検証する。

## 📊 データセット (Dataset)
**NASA PCoE Li-ion Battery Aging Datasets**
- **Data Source**: [NASA Prognostics Center of Excellence](https://data.nasa.gov/dataset/li-ion-battery-aging-datasets)
- **Batteries**: B0005, B0006, B0007, B0018 (Operating at Room Temp)
- **Features**: Voltage, Current, Temperature, Time, Capacity
- **Scenario**: 定電流-定電圧（CC-CV）充電および定電流（CC）放電によるサイクル劣化試験

## 🛠️ 技術スタック (Tech Stack)
- **Language**: Python 3.9
- **Preprocessing**: Pandas, NumPy, Scipy (MATファイル解析)
- **Modeling**: 
  - **Baseline**: LightGBM (Gradient Boosting)
  - **Advanced**: LSTM / GRU (Recurrent Neural Networks), PyTorch
- **Evaluation**: RMSE, MAE, R² score
- **Visualization**: Matplotlib, Seaborn, Plotly

## 🏆 成功基準とKPI (KPIs & Success Criteria)

| Category | KPI | Target | Description |
| :--- | :--- | :--- | :--- |
| **Technical** | **SOH RMSE** | **< 1.5%** | 劣化率予測の平均二乗誤差平方根 |
| **Technical** | **R² Score** | **> 0.95** | モデルの当てはまりの良さ |
| **Business** | **False Positive Rate** | **< 5%** | 正常な電池を「劣化」と誤判定する率（過剰交換の防止） |
| **Business** | **Cost Impact** | **-10%** | 最適な交換サイクル予測によるダウンタイム/部品コスト削減率（試算） |

## 🏗️ モデルパイプライン (Pipeline)

1.  **Data Ingestion**: `.mat` 形式の生データをパースし、サイクル単位の構造化データへ変換。
2.  **Feature Engineering**:
    - 電圧・電流曲線からの統計特徴量（平均、歪度、尖度）抽出。
    - 容量低下トレンドの平滑化処理。
3.  **Modeling**:
    - LightGBMによる重要特徴量の選定。
    - LSTMによる時系列予測モデルの構築。
4.  **Evaluation**:
    - ホールドアウト検証（B0005, B0006, B0007で学習し、B0018でテスト）。
    - ノイズ付加データによるロバスト性テスト。

## 📈 結果 (Results)
*(※開発進行に合わせてここにグラフや数値を追記します)*

- **SOH Prediction Accuracy**:
    - LightGBM: RMSE = x.xx
    - LSTM: RMSE = x.xx
- **Robustness Test**:
    - ノイズレベル5%付加時の精度低下率: x%

## 🏭 製造業AIとしての評価 (Industrial AI Perspective)
本PoCでは、アカデミックな精度だけでなく、以下の実運用観点を評価しています。

- **ロバスト性 (Robustness)**: センサーノイズを想定した摂動データに対する推論安定性の検証。
- **ポータビリティ (Portability)**: 異なるバッテリー個体（B0018）への適用性能から、ライン横展開の可能性を評価。
- **運用コスト (Operational Cost)**: 推論レイテンシとモデルサイズのトレードオフ分析。

## 📂 ディレクトリ構成 (Directory Structure)
