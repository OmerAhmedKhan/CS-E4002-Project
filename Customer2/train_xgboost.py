#from sklearn.metrics import r2_score
import mlflow.xgboost
import xgboost as xgb
#from load_dataset import load_dataset
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

''' include user name and password to request '''
TRACKING_URI = 'http://54.154.121.22/'
''' set up tracking uri '''
mlflow.set_tracking_uri(TRACKING_URI)
client = mlflow.tracking.MlflowClient(TRACKING_URI)

def load_data(path, sep=';', test_size=0.2, random_state=123):
    data = pd.read_csv(path, sep=';')
    # Process dataset
    data = pd.get_dummies(data)
    data = data.drop(['y_no'], axis=1)
    x = data.drop(['y_yes'], axis=1)
    y = data['y_yes']
    # Log dataset parameters
    mlflow.log_param("dataset_path", path)
    mlflow.log_param("dataset_shape", data.shape)
    mlflow.log_param("test_size", test_size)
    mlflow.log_param("random_state", random_state)
    mlflow.log_param("one_hot_encoding", True)
    return train_test_split(x, y, test_size=test_size, random_state=random_state)

def run_exp(data_path, exp_name='default_name', model_name="direct-marketing-xgboost-model"):
    from sklearn.metrics import r2_score, mean_squared_error
    mlflow.set_experiment(exp_name)

    x = np.linspace(0, 2 * np.pi , num=100)
    y = np.cos(x)
    plt.plot(x, y)
    plt.savefig('./test_picture.png')
    ''' log parameters, metrics and artifacts on server '''

    with mlflow.start_run(run_name='direct-marketing-xgboost-basic') as run:
        mlflow.log_artifact('./test_picture.png')

        x_train, x_test, y_train, y_test = load_data(data_path)

        cls = xgb.XGBClassifier(objective='binary:logistic', eval_metric='auc')
        cls.fit(x_train, y_train)

        auc = cls.score(x_test, y_test)
        print("AUC ", auc)
        mlflow.log_metric("AUC", auc)

        y_pred = cls.predict(x_test)
        r2_score = r2_score(y_test, y_pred)
        print("R2 ", r2_score)
        mlflow.log_metric("R2", r2_score)

        mse = mean_squared_error(y_test, y_pred)
        mlflow.log_metric("MSE", mse)
        print("MSE ", mse)

        mlflow.xgboost.log_model(cls, model_name)
        artifact_path = mlflow.get_artifact_uri()
        model_path = '{}/{}-model/'.format(artifact_path, exp_name)
        mlflow.log_param("model_path", model_path)
        mlflow.end_run()
        return model_path



if __name__ == '__main__':
    print(run_exp('bank-additional/bank-additional-full.csv', 'oak-marketing-xgboost'))