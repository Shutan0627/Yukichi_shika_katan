import gradio as gr
from Gaze_tracking.eye import gaze_tracking
from voice_recognition.voice_recognition import voice_recognition, return_formatted_output
from voice_recognition.inntonation_30sec import analyze_video
from gpt import create_feedback
import concurrent.futures
import pandas as pd
import random

def make_comment_for_streaming(path):
    """
    pathからコメントのリストをcsv形式で生成し、フィードバックを生成する関数
    input: path
    output: None(.csv形式で保存)
    """
    def make_comment_from_wpm(path):
        """
        wpmのコメントを生成する関数
        input: path
        output: [
            float: 経過時間(秒), 
            str: "wpm", 
            str: 評価内容
        ]
        
        """
        wpm_list = voice_recognition(path)
        threshold = 500
        comment = []

        for wpmdata in wpm_list:
            if wpmdata[2] > threshold:
                comment.append([f"{wpmdata[0]:.2f}", "wpm", "fast"])
            else:
                comment.append([f"{wpmdata[0]:.2f}", "wpm", "appropriate"])
        return comment

    def make_comment_from_pitch(path):
        """
        pitchのコメントを生成する関数
        input: path
        output: [
            float: 経過時間(秒), 
            str: "pitch", 
            str: 評価内容
        ]
        """
        pitch_list = analyze_video(path)
        comment = []
        for pitchdata in pitch_list:
            if pitchdata[2] == False:
                comment.append([f"{pitchdata[0]:.2f}", "pitch", "false"])
            else:
                comment.append([f"{pitchdata[0]:.2f}", "pitch", "true"])
        return comment

    def make_comment_from_eye(path):
        """
        視線のコメントを生成する関数
        input: path
        output: [
            float: 経過時間(秒), 
            str: "eye", 
            str: 評価内容
        ]
        """
        eye_list = gaze_tracking(path)
        comment = []
        for eyedata in eye_list:
            if eyedata[1] == False:
                comment.append([f"{float(eyedata[0]):.2f}", "eye", f"視線：{eyedata[2]}秒間外れていた"])
        return comment


    def merge_comments(path):
        """
        3つのコメントを統合する関数
        input: path
        output: [
            float: 経過時間(秒), 
            str: "wpm" or "pitch" or "eye", 
            str: 評価内容
        ]
        """

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_wpm = executor.submit(make_comment_from_wpm, path)
            future_pitch = executor.submit(make_comment_from_pitch, path)
            future_eye = executor.submit(make_comment_from_eye, path)

            # 結果を集める
            comments = []
            comments.extend(future_wpm.result())
            comments.extend(future_pitch.result())
            comments.extend(future_eye.result())

        return comments

    def generate_comments(path):
        merged_comments = merge_comments(path)
        merged_comments.sort(key=lambda x: float(x[0]))

        return merged_comments
    import csv

    # コメントを生成
    data = generate_comments(path)
    csv_file_path = './data/output.csv'

    with open(csv_file_path, mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "time", "class", "comment"])

        for idx, (time, category, comment) in enumerate(data):
            if category == "wpm":
                if comment == "fast":
                    comment = random.choice(["もっとゆっくり話して欲しいかも(´・ω・`)", "着いていけなくなったかも（´。＿。｀）", "置いていかれた→待ってー!","私を置いていかないで(´；ω；`)"])
                else:
                    comment = random.choice(["テンション上がってきた！！", "この速さがちょうどいいかも！(・ω・)", "この速さでいいと思います-_-b", "♫", "聞きやすいなあ"])
            if category == "pitch":
                if comment == "false":
                    comment = random.choice(["もっと抑揚欲しい（´_ゝ｀）", "眠いZzz…(*´～`*)", "退屈ー(ノД`)・゜。"])
                else:
                    comment = random.choice(["抑揚があっていい感じですね(´・ω・`)", "聞いてて飽きないですね！", "抑揚があると楽しいですね(´・ω・`)", "抑揚があると聞いてて楽しいですね！"])
            if category == "eye":
                comment = random.choice(["目線が安定してない(・_・;)", "目が合わない(´・ω・`)", "こっち見て！", "目が合わないと不安ヾ(･ω･`;)ﾉ", "こっちみてーー！！"])

            writer.writerow([idx + 1, time, category, comment])

    print(f"データが {csv_file_path} に保存されました。")

    # フィードバックを生成
    formatted_output = return_formatted_output(path)
    feed_back = create_feedback(formatted_output, data)
    #フィードバックをcsvに保存
    with open(csv_file_path, mode='a',newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([0,10000,"gpt",feed_back])
    
    
    return csv_file_path




# print(make_comment_for_streaming("/Users/siga6/Downloads/ムービー（2024-07-20 16.37）.mp4"))

