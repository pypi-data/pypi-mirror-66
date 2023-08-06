import frauddetection.use_model as fd

fd.FraudDetectionPredict.predictSingleSample([ 0, 1, 1, 1, 1, 0, 188, 174, 0, 1, 3, 3, 8, 52, 1, 1, 1, 1])
fd.FraudDetectionPredict.predictDatasetCsv('data.csv')
fd.FraudDetectionPredict.predictDatasetOds('data.ods')