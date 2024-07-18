import gradio as gr
from GazeTracking.example import gaze_tracking
def show_capturing(image):

    return "Capturing"

iface = gr.Interface(fn=gaze_tracking, inputs=[], outputs="image")
iface.launch()
