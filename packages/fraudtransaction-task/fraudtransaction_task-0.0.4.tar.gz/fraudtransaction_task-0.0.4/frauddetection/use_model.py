
import pandas as pd
import joblib
import numpy as np
from pandas_ods_reader import read_ods

class FraudDetectionPredict:

    def predictDatasetCsv(filename):
        original_df = pd.read_csv(filename)
        df = original_df.drop('gender', 1)
        df = df.drop('consumer_id', 1)
        df = df.fillna(0)

        # standardize the data to normal distribution
        from sklearn import preprocessing
        dataset_standardized = preprocessing.scale(df)
        dataset_standardized = pd.DataFrame(dataset_standardized)

        # Load the model from the file
        model_from_joblib = joblib.load('model_logistic.pkl')

        # Use the loaded model to make predictions
        prediction = model_from_joblib.predict(dataset_standardized)
        print(prediction)

    def predictDatasetOds(filename):
        original_df = read_ods(filename, 1)
        df = original_df.drop('gender', 1)
        df = df.drop('consumer_id', 1)
        df = df.fillna(0)

        # standardize the data to normal distribution
        from sklearn import preprocessing
        dataset_standardized = preprocessing.scale(df)
        dataset_standardized = pd.DataFrame(dataset_standardized)

        # Load the model from the file
        model_from_joblib = joblib.load('model_logistic.pkl')

        # Use the loaded model to make predictions
        prediction = model_from_joblib.predict(dataset_standardized)
        print(prediction)


    def predictSingleSample(arrayValue):
        # Load the model from the file
        model_from_joblib = joblib.load('model_logistic.pkl')
        # Use the loaded model to make predictions
        arr = np.array(arrayValue)
        arr = arr.reshape(1, -1)
        prediction = model_from_joblib.predict(arr)
        print(prediction)


#fd = FraudDetectionPredict()
#fd.predictDatasetCsv('data.csv')
#fd.predictDatasetOds('data.ods')
#fd.predictSingleSample([ 0, 1, 1, 1, 1, 0, 188, 174, 0, 1, 3, 3, 8, 52, 1, 1, 1, 1])