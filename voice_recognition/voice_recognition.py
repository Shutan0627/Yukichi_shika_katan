import whisper
import json
# from voice_recognition.recording import recording

def voice_recognition():
    # file_name = recording()
    file_name = "3.wav"
    file_path = f"/Yukichi_shika_katan/voice_recognition/records/{file_name}" #音声ファイルのパス
    model = whisper.load_model("small") #モデル指定
    result = model.transcribe(file_path, verbose=True, fp16=False, language="ja") #ファイル指定
    print(result['text'])

    f = open('./transcription.txt', 'w', encoding='UTF-8')

    # セグメント情報を取得してフォーマットする
    formatted_output = ""
    for segment in result['segments']:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        formatted_output += f"[{start_time:05.3f} --> {end_time:05.3f}] {text}\n"


    f.write(formatted_output)
    f.close()

voice_recognition()

