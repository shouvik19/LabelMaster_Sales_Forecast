import pandas as pd
import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt

df = pd.read_csv('/content/drive/My Drive/Practicum/df_503_imputed_feat_lag_1.csv')



df = df.loc[:, df.columns != 'Date']

df = df.round(2)

test_ind = 6

train = df.iloc[:-test_ind]
test = df.iloc[-test_ind:]

# scale
mean = train.mean(axis=0)
scaled_train = train - mean
std = train.std(axis=0)
scaled_train /= std


x_scaled_train=scaled_train.iloc[:,:-1]
y_scaled_train = scaled_train.iloc[:,-1]



'''
# scale
x_mean = x_train.mean(axis=0)
x_scaled_train = x_train - x_mean
x_std = x_train.std(axis=0)
x_scaled_train /= x_std

y_mean = y_train.mean(axis=0)
y_scaled_train = y_train - y_mean
y_std = y_train.std(axis=0)
y_scaled_train /= y_std
'''

scaled_test = test - mean
scaled_test /=std

x_scaled_test=scaled_test.iloc[:,:-1]
y_scaled_test = scaled_test.iloc[:,-1]

'''
y_scaled_test = y_test - y_mean
y_scaled_test /=y_std
'''

# converting into numpy array
scaled_train_array = np.array(scaled_train)
x_scaled_train_array = np.array(x_scaled_train)
y_scaled_train_array = np.array(y_scaled_train)

scaled_test_array = np.array(scaled_test)
x_scaled_test_array = np.array(x_scaled_test)
y_scaled_test_array = np.array(y_scaled_test)

# transformation operations for y, both produce same results
#(y_scaled_test * std[100]) +mean[100]
#(y_scaled_test_array * std[100]) +mean[100]

from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

# define generator
#length = 3 # Length of the output sequences (in number of timesteps)
#batch_size = 1 #Number of timeseries samples in each batch
#generator = TimeseriesGenerator(scaled_train_array, y_scaled_train_array, length=length, batch_size=batch_size)

#len(x_scaled_train)
#len(generator) 

#X,y = generator[0]

#print(f'Given the Array: \n{X.flatten()}')
#print(f'Predict this y: \n {y}')

#print(X.shape)
#print(y.shape)


# new and correct model
#--------------------------------
from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import Dense,LSTM,Conv1D
from keras import layers
import tensorflow as tf
tf.keras.backend.clear_session()
tf.random.set_seed(51)
np.random.seed(51)


# define model
def nn_model(scaled_train_array,y_scaled_train_array,length,epochs):
    
    length = 12 # Length of the output sequences (in number of timesteps)
    batch_size = 1 #Number of timeseries samples in each batch
    generator = TimeseriesGenerator(scaled_train_array, y_scaled_train_array, length=length, batch_size=batch_size)
    
    model = Sequential()
    
    model.add(tf.keras.layers.Conv1D(filters=32, kernel_size=5,
                          strides=1, padding="causal",
                          activation="tanh",
                          input_shape=(None,(scaled_train_array.shape[1]))))
 
    model.add(tf.keras.layers.LSTM(512, activation = 'tanh', dropout=0.25, recurrent_dropout= 0.25, return_sequences=True))

    model.add(tf.keras.layers.LSTM(512, dropout=0.25, recurrent_dropout= 0.25, activation = 'tanh', return_sequences=True))
    model.add(tf.keras.layers.LSTM(512,  activation = 'tanh'))
    
    model.add(tf.keras.layers.Dense(100))
    model.add(tf.keras.layers.Dense(1))
    
    optimizer = tf.keras.optimizers.Adam(lr=0.0001)
    model.compile(optimizer=optimizer, loss='mse')
    
    model.summary()
    #---------------------------------
    
    
    #from tensorflow.keras.callbacks import EarlyStopping
    
    #early_stop = EarlyStopping(monitor='val_loss',patience=1)
    
    #validation_generator = TimeseriesGenerator(scaled_test_array,y_scaled_test_array, 
     #                                          length=length, batch_size=batch_size)
    
    model.fit_generator(generator,epochs=epochs)
    #                    validation_data=validation_generator)
                  #     callbacks=[early_stop])
    
    
    model.history.history.keys()
    
    losses = pd.DataFrame(model.history.history)
    losses.plot()
    return model


'''
model = nn_model(scaled_train_array,y_scaled_train_array,length = 13,epochs =1)

length = 13
first_eval_batch = scaled_train_array[-length:]

first_eval_batch = first_eval_batch.reshape((1, length, scaled_train_array.shape[1]))

model.predict(first_eval_batch)
'''


# updated 
#---------------------------------------
length = 9
epochs =8
n_features = scaled_train.shape[1]
test_predictions = []

first_eval_batch = scaled_train_array[-length:]
current_batch = first_eval_batch.reshape((1, length, n_features))


scaled_train_array_iter = scaled_train_array
y_scaled_train_array_iter = y_scaled_train_array

for i in range(len(test)):

    print('Iteration {ii} out of {l}'.format(ii=i+1, l=len(test)))
    print('scaled_train_array_iter.shape = ' + str(scaled_train_array_iter.shape))
    print('y_scaled_train_array_iter.shape = ' + str(y_scaled_train_array_iter.shape))

    model = nn_model(scaled_train_array_iter,y_scaled_train_array_iter,length,epochs=epochs)
    
    # get prediction 1 time stamp ahead ([0] is for grabbing just the number instead of [array])
    current_pred = model.predict(current_batch)[0]
    
    # store prediction
    test_predictions.append(current_pred)
    
    test_batch_2 = np.append(x_scaled_test_array[i,:], current_pred)
    test_batch_2 = test_batch_2.reshape(1,x_scaled_test_array.shape[1]+1)

    test_batch_3 = test_batch_2.reshape((1,1,n_features))

    
    # update batch to now include prediction and drop first value
    current_batch = np.append(current_batch[:,1:,:], test_batch_3[:,:1,:] ,axis=1)
    
    scaled_train_array_iter = np.append(scaled_train_array[:,:], test_batch_2[:(i+1),:],axis=0)
    y_scaled_train_array_iter = scaled_train_array_iter[:,-1]
    
    
    
#-----------------------
#scaled_train_array_iter = np.append(scaled_train_array[:,:], scaled_test_array[:(0+1),:],axis=0)
#y_scaled_train_array_iter = scaled_train_array_iter[:,-1]


#-----------------------



# check results
a=0
b=0
for i in range(len(test_predictions)):
  a = (test_predictions[i] * std[100]) +mean[100]
  b= np.array(y_scaled_test)
  b=(b[i] * std[100]) +mean[100]
  print(a)
  print(b)
  print('% error = ' + str((a-b)/b*100))

