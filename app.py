from flask import Flask, render_template, request
from network import clean, build_vector, get_model
import numpy as np


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def blendie_home():
    return render_template('blendie_home.html')

@app.route('/start', methods=['POST'])
def blendie_start():
    return render_template('blendie_start.html')

@app.route('/respond', methods=['POST', 'GET'])
def blendie_respond():
    with open('mydict.txt', 'r') as f:
        mydict = set(f.read().split(',')[1:])
    size = len(mydict)
    user_feeling = request.form['user_feeling']
    user_feeling = clean(user_feeling)
    user_feeling = np.array([build_vector(user_feeling, mydict)])
    model = get_model(size)
    print(model.predict(user_feeling)[0])
    score = np.argmax(model.predict(user_feeling)[0])
    if score == 2:
        response = "I am glad to hear that everything is going well.\nPlease come again if you are feeling down!"
    elif score == 0:
        response = "I am sorry to hear that you are feeling that way."
        return render_template('blendie_negative.html', response=response)
    else:
        response = "I can't quite seem to understand. Please press 'Home' and try again. I am sorry for this defficiency! Try being more verbose."
    return render_template('blendie_respond.html', response=response)

@app.route('/techniques', methods=['POST', 'GET'])
def blendie_techniques():
    flag = request.form['technique']
    if flag.lower() == 'ppt':
        response = '''
            If you are ever in serious trouble, please call 911. These feelings are not easy to navigate 
            I am so sorry that you are feeling these negative thoughts. I suggest you do your bestt to 
            explore why you are feeling they way that you are, and ask yourself thought provoking questions. 
            Perhaps reach out to a family member or a close friend, with their consent, to discuss how the 
            relationships in your life may be impacting your feelings. Lastly, if you are feeling up to it, 
            consider seeing an actual therapist to further help with these challenging thoughts. 
            Remember, there are always people who care about you. :)
            '''
        return render_template('blendie_techniques.html', response=response)
    elif flag.lower() == 'cbt':
        response = '''
        If you are ever in serious trouble, please call 911. These feelings are not easy to navigate 
        I am so sorry that you are experiencing these negative thoughts, but it is important to remember
        that they are distorted and not worth entertaining. At this link, <https://tinyurl.com/64c8eycs>, 
        you will find a sheet to help work through these thoughts and make them more closely align with reality.
        Lastly, if you are feeling up to it, consider seeing an actual therapist to further help with these 
        challenging times. Remember, there are always people who care about you.
        '''
        return render_template('blendie_techniques.html', response=response)
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)