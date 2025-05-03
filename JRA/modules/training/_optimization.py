import optuna
import numpy as np
import pandas as pd
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from lightgbm import LGBMClassifier
import optuna.visualization as vis
from tqdm import tqdm
from sklearn.model_selection import StratifiedKFold, cross_val_score

# ログの設定
logging.basicConfig(filename="optuna_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def optimization(data, n_trials=1000):
    # 説明変数と目的変数を分離
    X = data.drop(columns=['rank', 'date'])  # 'rank' を削除
    y = data['rank']  # 目的変数

    # 訓練データとテストデータに分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # プログレスバーを設定
    pbar = tqdm(total=n_trials, desc="Optimization Progress")

    def objective(trial):
        # 特徴量の選択
        selected_features = [col for col in X_train.columns if trial.suggest_categorical(f"use_{col}", [True, False])]
        
        if len(selected_features) == 0:
            pbar.update(1)
            return 0  # 全ての特徴量が False ならスキップ

        X_train_selected = X_train[selected_features]
        X_test_selected = X_test[selected_features]

        # ハイパーパラメータの選択
        params = {
            'objective': 'binary',
            'metric': 'auc',
            'boosting_type': 'gbdt',
            'n_estimators': 500,
            'learning_rate': trial.suggest_loguniform('learning_rate', 0.005, 0.1),
            'num_leaves': trial.suggest_int('num_leaves', 20, 40),  # 上限を下げる
            'max_depth': trial.suggest_int('max_depth', 3, 6),  # 上限を下げる
            'min_child_samples': trial.suggest_int('min_child_samples', 50, 200),  # 下限を上げる
            'colsample_bytree': trial.suggest_uniform('colsample_bytree', 0.3, 0.7),
            'subsample': trial.suggest_uniform('subsample', 0.3, 0.7),
            'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-3, 100.0),
            'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-3, 100.0),
            'verbose': -1
        }

        # モデルの学習
        model = LGBMClassifier(**params)
        model.fit(X_train_selected, y_train)
        
        # # 精度を評価指標とする
        # y_pred_prob = model.predict_proba(X_test_selected)[:, 1]  # 確率スコアを取得

        # 交差検証で AUC を評価
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        auc_scores = cross_val_score(model, X_train_selected, y_train, cv=skf, scoring="roc_auc")
          # ログに記録
        logging.info(f"Trial {trial.number}: AUC={np.mean(auc_scores)}, Features={len(selected_features)}")
        
        pbar.update(1)  # プログレスバーを更新    

        # 平均 AUC を最適化対象とする
        return np.mean(auc_scores)

        

    
    # Optuna で最適化
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=n_trials)
    
    pbar.close()  # プログレスバーを閉じる
    
    print("Best AUC:", study.best_value)
    print("Best Parameters:", study.best_params)

    # 最適な特徴量の選択
    best_features = [col for col in X.columns if study.best_params.get(f"use_{col}", False)]
    print("Selected Features:", best_features)
    
    hyperparams = {k: v for k, v in study.best_params.items() if not k.startswith("use_")}
    
    return best_features, hyperparams
