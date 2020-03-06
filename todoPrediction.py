import numpy as np 
from sklearn.preprocessing import MinMaxScaler 
import tensorflow as tf
from keras.models import load_model
# from tensorflow.keras.models import load_model
from flask import Flask,redirect,render_template,request
graph = tf.get_default_graph()


app = Flask(__name__)

# model = tf.keras.models.load_model('todomodel.h5')
## model will load below



@app.route('/')
def login():
     return render_template('login1.html')


@app.route('/model',methods=["POST"])
def r():
     data = dict(request.form)
     date = data['name']
     # 2020-10-06
     day = date[-2:]
     month = date[-5:-3]
     year = date [-8:-6]
     last_date = [int(str(int(day))+str(int(month))+str(int(year)))]



     Sum = []
     year = 18
     for years in range(2):
          for month in range(1,13):
               if month<=7 and month!=2:
                    if (month%2)==0 :
                         days = 30
                    else:
                         days = 31
               elif month>=8 and month!=2:
                    if (month%2)==0 :
                         days = 31
                    else:
                         days = 30
               
               elif month==2:
                    days = 28
               for day in range (1,days+1):
                    Sum.append([int(str(day)+str(month)+str(year))])
          year += 1

     scaler = MinMaxScaler()
     scaler.fit(Sum)

     rand_Sum = []
     for i in range(2):
          f_1st = np.random.randint(20,30,size=(1))
          s_2nd = np.random.randint(12,13,size=(1))
          t_3rd = np.random.randint(19,20,size=(1))
          rand_Sum.append([int(str(f_1st[0])+str(s_2nd[0])+str(t_3rd[0]))])
     
     buyed_or_not = []
     for _ in range(3):  
          buyed_or_not.append(list(np.random.randint(2,size=(29))))

     rand_Sum.append(last_date)
     scale_Sum = scaler.transform(rand_Sum)
     scale_buyed_or_not = scaler.fit_transform(buyed_or_not)

     past_data = []
     for j in range(len(scale_Sum)):
          past_data.append([scale_Sum[j][0]])
          for k in range(len(scale_buyed_or_not[0])):
               past_data[j].append(scale_buyed_or_not[j][k])

          
          
     past_data = np.array(past_data)
     past_data = past_data.reshape(1,3,30)

     with graph.as_default():
         try:
              regressor = tf.keras.models.load_model('todomodel.h5')
              prediction = regressor.predict(past_data)
         except Exception as e:
              return str(e)

     num_of_prediction =1                     # num of prediction
     all_predictions = []
     for after_day in range(num_of_prediction):
          all_predictions.append(regressor.predict(past_data)[0])
               
     prediction_result = []  
     for value in all_predictions:
          loop_list = []
          for ans in range(len(value)):
               if value[ans] >= 0.5:
                    loop_list.append(int(np.ceil(value)[ans]))
               else:
                    loop_list.append(int(np.floor(value[ans])))
          prediction_result.append(loop_list)

     prediction_result = np.array(prediction_result[0])
     items = [ 'bread', 'egg', 'waffles', 'butter','milk', 'yogurt', 'burrito', 'cereal', 
          'cheese', 'beef', 'mutton','fish', 'mango', 'oranges', 'banana', 'apple', 'grapes', 'guava',
          'cherry', 'strawberry', 'peach', 'coriander', 'mint', 'tomato', 'onion','potatoes', 'garlic', 'ginger', 'pepper']

     
     result_dict = {}
     for j in range(len(prediction_result)):
          one_or_zero = prediction_result[j]
          Items = items[j]
          result_dict[Items] = one_or_zero 
     result = []
     for k,v in result_dict.items():
          if v==1:
               result.append(k)
     
     return (str(result))     






if __name__=="__main__":
    app.run(debug=True,port=5001)