import pandas as pd
import time
from flask import Flask, jsonify, render_template, request

filepath = './data/output.csv'

app = Flask(__name__)

def format_time(seconds):
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}分{remaining_seconds}秒"


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def data():
    df = pd.read_csv(filepath)
    pd.set_option('display.max_colwidth', None)
    tm = request.json

    response_data = {}
    print('dtype: ', df.dtypes)
    gpt_review = df.loc[df['class']=='gpt', 'comment']
    print('gpt_review: ', gpt_review)
    response_data['gpt_review'] = str(gpt_review)
    print('gpt_review: ', str(gpt_review))
    
    filtered_df = df[df['time'] <= int(tm)].sort_values(by='time', ascending=False).head(7)
    type_data = filtered_df['class'].tolist()
    comment_data = filtered_df['comment'].tolist()
    filtered_df['time'] = filtered_df['time'].astype(int)
    filtered_df['time'] = filtered_df['time'] + 3
    time_data = filtered_df['time'].tolist()
    print('time: ', tm)

    for i in range(7):
        response_data[f'type{i+1}'] = type_data[i] if i < len(type_data) else ""
        print('type: ', type_data[i]) if i < len(type_data) else ""
        response_data[f'comment{i+1}'] = comment_data[i] if i < len(comment_data) else ""
        print('comment: ', comment_data[i]) if i < len(type_data) else ""
        response_data[f'time{i+1}'] = format_time(time_data[i]) + ' : ' if i < len(time_data) else ""
        
    
    return jsonify(response_data)

# @app.route('/data')
# def data():
#     df = pd.read_csv(filepath)
#     tm = input("秒数を入力してください: ")
#     filtered_df = df[df['time'] <= int(tm)].sort_values(by='time', ascending=False).head(5)
#     # type = df.loc[df['time']==int(tm), 'class'].values[0]
#     # comment = df.loc[df['time']==int(tm), 'comment'].values[0]
#     type_data = filtered_df['class'].tolist()
#     comment_data = filtered_df['comment'].tolist()
#     time_data = filtered_df['time'].tolist()

#     response_data = {}
#     for i in range(4):
#         response_data[f'type{i+1}'] = type_data[i] if i < len(type_data) else ""
#         response_data[f'comment{i+1}'] = comment_data[i] if i < len(comment_data) else ""
#         response_data[f'time{i+1}'] = format_time(time_data[i]) + ' : ' if i < len(time_data) else ""

#     return jsonify(response_data)
#     # return jsonify({'type': type, 'comment': comment})

if __name__ == '__main__':
    app.run(debug=True)
        
