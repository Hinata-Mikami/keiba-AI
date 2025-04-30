import pandas as pd
import lightgbm as lgb
from sklearn.metrics import roc_auc_score
import optuna.integration.lightgbm as lgb_o

from ._data_splitter import DataSplitter


class ModelWrapper:
    """
    モデルのハイパーパラメータチューニング・学習の処理が記述されたクラス。
    """
    def __init__(self):
        self.__lgb_model = lgb.LGBMClassifier(objective='binary')
        # self.__lgb_model = lgb.LGBMClassifier(objective='multiclass')
        # self.__lgb_model = lgb.LGBMRegressor(objective='regression')
        
        self.__feature_importance = None

    def tune_hyper_params(self, datasets: DataSplitter):
        """
        optunaによるチューニングを実行。
        """

        params = {'importance' : 'gain', 'objective': 'binary', 'extra_trees' : False}
        # params = {
        #     'importance' : 'gain',
        #     'extra_trees' : True,
        #     'objective':'multiclass', # 目的 : 多クラス分類
        #     'metric':{'multi_error'}, # 評価指標 : 正答率
        #     'num_class': 4             # クラス数 : 4
        #     }
        # 回帰に修正
        # params = {
        #     'importance': 'gain',
        #     'objective': 'regression',  # or 'regression_l2'
        #     'metric': 'rmse',
        #     'extra_trees': True
        # }
        

        # チューニング実行
        lgb_clf_o = lgb_o.train(
            params,
            datasets.lgb_train_optuna,
            valid_sets=(datasets.lgb_train_optuna, datasets.lgb_valid_optuna),
            callbacks=[
                lgb.callback.log_evaluation(period=100),  # 100イテレーションごとに評価結果を出力
                lgb.callback.early_stopping(stopping_rounds=10)  # 早期停止パラメータ、verboseはデフォルトtrueのため指定不要
                ],
            optuna_seed=42 # optunaのseed固定
            )

        # num_iterationsとearly_stopping_roundは今は使わないので削除
        tunedParams = {
            k: v for k, v in lgb_clf_o.params.items() if k not in ['num_iterations', 'early_stopping_round']
            }

        self.__lgb_model.set_params(**tunedParams)

    @property
    def params(self):
        return self.__lgb_model.get_params()

    def set_params(self, ex_params):
        """
        外部からハイパーパラメータを設定する場合。
        """
        self.__lgb_model.set_params(**ex_params)

    def train(self, datasets: DataSplitter):
        # 学習
        self.__lgb_model.fit(datasets.X_train.values, datasets.y_train.values)
        # AUCを計算して出力
        auc_train = roc_auc_score(
            datasets.y_train, 
            self.__lgb_model.predict_proba(datasets.X_train)[:, 1],
            # self.__lgb_model.predict_proba(datasets.X_train),
            # multi_class='ovr'
            )
        auc_test = roc_auc_score(
            datasets.y_test,
            self.__lgb_model.predict_proba(datasets.X_test)[:, 1],
            # self.__lgb_model.predict_proba(datasets.X_test),
            # multi_class='ovr'
            )
        # 回帰なのでRMSE（平均二乗誤差の平方根）に変更
        # from sklearn.metrics import mean_squared_error

        # # 予測
        # y_pred_train = self.__lgb_model.predict(datasets.X_train)
        # y_pred_test = self.__lgb_model.predict(datasets.X_test)

        # # 評価
        # rmse_train = mean_squared_error(datasets.y_train, y_pred_train, squared=False)
        # rmse_test = mean_squared_error(datasets.y_test, y_pred_test, squared=False) 
        
        # 特徴量の重要度を記憶しておく
        self.__feature_importance = pd.DataFrame({
            "features": datasets.X_train.columns,
            "importance": self.__lgb_model.feature_importances_
            }).sort_values("importance", ascending=False)
        
        print('AUC: {:.3f}(train), {:.3f}(test)'.format(auc_train, auc_test))
        # print('RMSE: {:.3f}(train), {:.3f}(test)'.format(rmse_train, rmse_test))
        
        # policies._score_policy.py L16 も修正

    @property
    def feature_importance(self):
        return self.__feature_importance

    @property
    def lgb_model(self):
        return self.__lgb_model

    @lgb_model.setter
    def lgb_model(self, loaded):
        self.__lgb_model = loaded
