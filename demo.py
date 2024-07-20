import gradio as gr
from GazeTracking.example import gaze_tracking
from voice_recognition.voice_recognition import voice_recognition, return_formatted_output
from voice_recognition.inntonation_30sec import analyze_video
import time
from gpt import create_feedback
import concurrent.futures


def make_comment_from_wpm(path):
    wpm_list = voice_recognition(path)
    threshold = 500
    comment = []

    for wpmdata in wpm_list:
        if wpmdata[2] > threshold:
            comment.append([wpmdata[0], "wpm", "fast"])
    return comment

def make_comment_from_pitch(path):
    pitch_list = analyze_video(path)
    comment = []
    for pitchdata in pitch_list:
        if pitchdata[2] == False:
            comment.append([pitchdata[0], "pitch", "抑揚：なし"])
    return comment

def make_comment_from_eye(path):    
    eye_list = gaze_tracking(path)
    comment = []
    for eyedata in eye_list:
        if eyedata[1] == False:
            comment.append([eyedata[0], "eye", f"視線：{eyedata[2]}秒間外れていた"])
    return comment

def comment_streaming(path):
    comments, feed_back = generate_comment(path)
    current_comments = []
    for comment in comments:
        current_comments.append(f"{int(comment[0])}:\n@{comment[1]}さん: {comment[2]}")
    
    return "\n".join(current_comments), feed_back

def get_formatted_output(path):
    return return_formatted_output(path)

def generate_comments(path):
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
    


def generate_comment(path):
    comment = generate_comments(path)
    comment.sort()
    formatted_output = return_formatted_output(path)
    feed_back = create_feedback(formatted_output, comment)

    return comment, feed_back




with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            movie = gr.Video(label="capturing")
            button = gr.Button("processing")
        with gr.Column():
            chat = gr.Text(label="capturing", interactive=False)
    feed_back = gr.Markdown(label="capturing")
    button.click(fn=comment_streaming, inputs=movie, outputs=[chat, feed_back])

demo.launch()
