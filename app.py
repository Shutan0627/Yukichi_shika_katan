import threading
from voice_recognition.voice_recognition import voice_recognition
from GazeTracking.example import gaze_tracking
# 結果を格納する変数を定義
# 画像認識関数
def image_recognition():
    global image_result
    image_result = gaze_tracking()


# スレッドを使用して音声認識を実行
def audio_thread():
    global audio_result
    audio_result = voice_recognition()

# 結果を格納する変数を定義
audio_result = None
image_result = None

# スレッドの定義
t1 = threading.Thread(target=audio_thread)

# スレッドの開始
t1.start()

# メインスレッドで画像認識を実行
image_result = image_recognition()

# 音声認識スレッドが終了するのを待つ
t1.join()

# 結果の統合
combined_result = {
    'audio': audio_result,
    'image': image_result
}

# 結果の表示
print(combined_result)
