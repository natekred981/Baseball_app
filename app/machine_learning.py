from extraction import data
import tensorflow
from tensorflow.keras.layers import Dense,Flatten
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split as tts
import mysql.connector

df,players = data()
df = df.drop(columns=['Unnamed: 0'])
x = df.drop(columns=['nominated']).to_numpy()
y = df['nominated'].to_numpy().astype('int')
x_train,x_test,y_train,y_test = tts(x,y,test_size=0.25)
y_train = tensorflow.keras.utils.to_categorical(y_train, num_classes=2)
y_test = tensorflow.keras.utils.to_categorical(y_test, num_classes=2)
mlp = Sequential()
mlp.add(Dense(20,activation='sigmoid',name='input'))
mlp.add(Dense(2, activation='softmax'))
mlp.compile(loss='categorical_crossentropy', optimizer='adam', metrics = ['accuracy'])
mlp.fit(x_train,y_train, epochs = 5, verbose = 1)
print('Test accuracy: %.2f %%'%(100*mlp.evaluate(x_test,y_test, verbose=1)[1]))
""" data.to_csv("./Baseball_HOF/here.csv")
config = {
        'user': 'root',
        'password': ',s;s_ghi&9=A',
        'host': 'db',
        'port': '3306',
        'database': 'lahaman2016'
    }
connection = mysql.connector.connect(**config) """
