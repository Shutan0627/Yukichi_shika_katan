import whisper
from pykakasi import kakasi
import numpy as np  

sample_rate = 44100
channels = 1


def voice_recognition(path):
    """
    音声認識を行う関数
    input: path
    output: {
        ["text": str,
        "start": float,
        "end": float,
        ],
        "formatted_output": str
    }
    """

    def hiragana_text(text):
        hiragana = kakasi()
        hiragana.setMode('J', 'H')
        hiragana_text = hiragana.getConverter()
        return hiragana_text.do(text)
    
    wpm_list = []

    model = whisper.load_model("small") #モデル指定
    # path = "/Users/siga6/Downloads/3-2.wav"
    result = model.transcribe(audio=path, verbose=True, fp16=False, language="ja") #ファイル指定
    print(result['text'])
    
    # セグメント情報を取得してフォーマットする
    formatted_output = ""
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        text_hiragana = hiragana_text(text)
        wpm = int(len(text_hiragana) / (end_time - start_time) * 60.0)
        formatted_output += f"[{start_time:05.3f} --> {end_time:05.3f} : {wpm}wpm]\n   {text}\n"
        wpm_list.append([start_time, end_time, wpm])
    # f.write(formatted_output)
    print(formatted_output)
    # f.close()
    return wpm_list

def return_formatted_output(path):
    """
    音声認識を行う関数
    input: path
    output: {
        ["text": str,
        "start": float,
        "end": float,
        ],
        "formatted_output": str
    }
    """

    def hiragana_text(text):
        hiragana = kakasi()
        hiragana.setMode('J', 'H')
        hiragana_text = hiragana.getConverter()
        return hiragana_text.do(text)
    
    wpm_list = []

    model = whisper.load_model("small") #モデル指定
    # path = "/Users/siga6/Downloads/3-2.wav"
    result = model.transcribe(audio=path, verbose=True, fp16=False, language="ja") #ファイル指定
    print(result['text'])
    
    # セグメント情報を取得してフォーマットする
    formatted_output = ""
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        text_hiragana = hiragana_text(text)
        wpm = int(len(text_hiragana) / (end_time - start_time) * 60.0)
        formatted_output += f"[{start_time:05.3f} --> {end_time:05.3f} : {wpm}wpm]\n   {text}\n"
    # f.write(formatted_output)
    # f.close()
    return formatted_output
