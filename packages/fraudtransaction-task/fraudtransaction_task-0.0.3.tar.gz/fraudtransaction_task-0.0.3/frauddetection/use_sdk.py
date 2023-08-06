import frauddetection.use_model as fd

fd.FraudDetectionPredict.predictSingleSample([1, 1, 1, 4, 5, 6, 7, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18])
fd.FraudDetectionPredict.predictDatasetCsv('data.csv')
fd.FraudDetectionPredict.predictDatasetOds('data.ods')