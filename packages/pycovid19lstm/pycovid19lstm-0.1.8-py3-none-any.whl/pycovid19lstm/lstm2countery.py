import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

def holt_winter(url,country,neurons,epochs):

	df_confirmed = pd.read_csv(url)

	df_confirmed1 = df_confirmed[df_confirmed["Country/Region"] == country]
	#df_confirmed1
	## structuring times eries data
	df_confirmed2 = pd.DataFrame(df_confirmed1[df_confirmed1.columns[4:]].sum(),columns=["confirmed"])
	df_confirmed2.index = pd.to_datetime(df_confirmed2.index,format='%m/%d/%y')
	df_confirmed2.tail()
	df_confirmed2.plot(title="Iraq-Confirmed cases")
	df_new = df_confirmed2[["confirmed"]]
	#df_new.tail(10)
	#daily data and i want to predict 5 days afterwards
	#len(df_new)
	x = len(df_new)-5
	#x
	train=df_new.iloc[:x]
	test = df_new.iloc[x:]
	#train
	##scale or normalize data as the data is too skewed
	from sklearn.preprocessing import MinMaxScaler
	scaler = MinMaxScaler()
	scaler.fit(train) #find max value 
	scaled_train = scaler.transform(train)#and divide every point by max value
	scaled_test = scaler.transform(test)
	#print(scaled_train[-5:])
	## feed in batches [t1,t2,t3] --> t4
	from keras.preprocessing.sequence import TimeseriesGenerator
	scaled_train.shape
	## how to decide num of inputs , 
	n_input = 5  ## number of steps
	n_features = 1 ## number of features you want to predict (for univariate time series n_features=1)
	generator = TimeseriesGenerator(scaled_train,scaled_train,length = n_input,batch_size=1)
	len(scaled_train)
	len(generator)
	x,y = generator[50]
	#(x.shape,y.shape)
	#(x,y)
	#y
	## above takes 5 inputs and predicts next point in scaled_train
	## smaller batch size leads to better trainig for time series
	from keras.models import Sequential
	from keras.layers import Dense, LSTM, Dropout, Activation
	model = Sequential()
	model.add(LSTM(neurons,activation="relu",input_shape=(n_input,n_features)))
	#model.add(Dropout(0.2))
	model.add(Dense(int(neurons/2), activation='relu'))
	model.add(Dense(units=1))
	#model.add(Activation('softmax'))
	#model.add(Dense(1))
	model.compile(optimizer="adam",loss="mse")
	#model.summary()
	validation_set = np.append(scaled_train[55],scaled_test)
	validation_set=validation_set.reshape(6,1)
	#validation_set
	## how to decide num of inputs , 
	n_input = 5
	n_features = 1
	validation_gen = TimeseriesGenerator(validation_set,validation_set,length=5,batch_size=1)
	validation_gen[0][0].shape,validation_gen[0][1].shape
	from tensorflow.keras.callbacks import EarlyStopping
	early_stop = EarlyStopping(monitor='val_loss',patience=20,restore_best_weights=True)
	model.fit_generator(generator,validation_data=validation_gen,epochs=epochs,callbacks=[early_stop],steps_per_epoch=10)
	pd.DataFrame(model.history.history).plot(title="loss vs epochs curve")
	model.history.history.keys()
	myloss = model.history.history["val_loss"]
	plt.title("validation loss vs epochs")
	plt.plot(range(len(myloss)),myloss)
	### evaluation batch
	## 5 history steps ---> step 6
	## last 5 point train predicts point 1 of test data
	## holding predictions
	test_prediction = []

	##last n points from training set
	first_eval_batch = scaled_train[-n_input:]
	current_batch = first_eval_batch.reshape(1,n_input,n_features)
	current_batch.shape
	## how far in future we can predict
	for i in range(len(test)+7):
		current_pred = model.predict(current_batch)[0]
		test_prediction.append(current_pred)
		current_batch = np.append(current_batch[:,1:,:],[[current_pred]],axis=1)
	#test_prediction
	### inverse scaled data
	true_prediction = scaler.inverse_transform(test_prediction)
	true_prediction[:,0]
	time_series_array = test.index
	for k in range(0,7):
		time_series_array = time_series_array.append(time_series_array[-1:] + pd.DateOffset(1))
	#time_series_array
	df_forecast = pd.DataFrame(columns=["confirmed","confirmed_predicted"],index=time_series_array)
	#df_forecast
	df_forecast.loc[:,"confirmed_predicted"] = true_prediction[:,0]
	df_forecast.loc[:,"confirmed"] = test["confirmed"]
	#df_forecast
	#plt.ylim([80000,85000])
	df_forecast.plot(title="{}-Predictions for next 7 days".format(country))
	#df_forecast.savefig('prediction_7_day.pdf')
	MAPE = np.mean(np.abs(np.array(df_forecast["confirmed"][:5]) - np.array(df_forecast["confirmed_predicted"][:5]))/np.array(df_forecast["confirmed"][:5]))
	print("MAPE is " + str(MAPE*100) + " %")
	sum_errs = np.sum((np.array(df_forecast["confirmed"][:5]) - np.array(df_forecast["confirmed_predicted"][:5]))**2)
	print('sum_errs:',sum_errs)
	stdev = np.sqrt(1/(5-2) * sum_errs)
	print('stdev:',stdev)
	# calculate prediction interval
	interval = 1.96 * stdev
	#interval
	df_forecast["confirm_min"] = df_forecast["confirmed_predicted"] - interval
	df_forecast["confirm_max"] = df_forecast["confirmed_predicted"] + interval
	#df_forecast
	df_forecast["Model Accuracy"] = round((1-MAPE),2)
	#df_forecast
	from datetime import datetime
	df_forecast["Country"] = country
	df_forecast["Execution date"] = str(datetime.now()).split()[0]
	#df_forecast
	df_forecast.to_excel(country+'_confirmed_prediction.xlsx')
	df_forecast.to_csv(country+'_confirmed_prediction.csv')
	### save model
	model.save("confirmed_{0}_{1}.h5".format(country,str(datetime.now()).split()[0]))
	df_forecast.iloc[:,:4].plot()
	fig= plt.figure(figsize=(10,5))
	plt.title("{} - Results".format(country))
	plt.plot(df_forecast.index,df_forecast["confirmed"],label="confirmed")
	plt.plot(df_forecast.index,df_forecast["confirmed_predicted"],label="confirmed_predicted")
	#ax.fill_between(x, (y-ci), (y+ci), color='b', alpha=.1)
	plt.fill_between(df_forecast.index,df_forecast["confirm_min"],df_forecast["confirm_max"],color="indigo",alpha=0.09,label="Confidence Interval")
	plt.legend()
	plt.savefig(country+'_result.png')
	plt.show()
	
		

