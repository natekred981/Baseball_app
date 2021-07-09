from flask import Flask, render_template, request
from fit import get_svm
from extraction import create_table
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
clf,x_test,y_test = get_svm()
@app.route('/')
def home():
    #y_pred = clf.predict(x_test)
    return render_template('home.html')
    #return str(metrics.accuracy_score(y_test, y_pred))
df,df2,y = create_table()
@app.route('/play',methods=['POST'])
def predict():
    player = request.form['player']    
    exists = player in df2['name'].values
    if (exists == True):
        df3 = df2[df2['name'] == player]
        stats = df3.to_html()
        df3 = df3.drop(columns=['playerID','name','nominated'])
        df3 = df3.to_numpy()
        prediction = clf.predict(df3)
        exists = str(prediction) == "[1]"
        print(stats)
        print(df3)
        if (str(prediction) == "[1]"):
            return render_template("predict_again.html",player=player, result = "will make the Hall of Fame", stats=[stats])
        else:
            return render_template("predict_again.html",player=player, result = "will not make the Hall of Fame",stats = [stats])
    else:
        return render_template('home.html')
if __name__ == '__main__':
   app.run(debug=False)