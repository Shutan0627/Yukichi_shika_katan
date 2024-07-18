import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import sys

# 録音の設定
sample_rate = 44100  # サンプリングレート（標準的には44100Hz）
channels = 1  # ステレオ録音
def recording():
    print("録音を開始するにはEnterキーを押してください。終了するにはCtrl+Cを押してください。")

    try:
        while True:

            print("録音中... Enterを押して録音を停止してください。")
            recording = []
            
            # 録音を開始
            def callback(indata, frames, time, status):
                if status:
                    print(status, file=sys.stderr)
                recording.append(indata.copy())
            
            with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback):
                input()  # Enterキーが押されるのを待つ

            # 録音が停止された後
            print("録音が完了しました。")

            # 録音データを配列に変換
            recording = np.concatenate(recording, axis=0)

            # WAVファイルとして保存
            output_filename = '/Users/siga6/Desktop/WORK/Yukichi_shika_katan/voice_recognition/records/recorded.wav'
            write(output_filename, sample_rate, recording)

            print(f"音声が {output_filename} として保存されました。")
            return 'recorded.wav'

    except KeyboardInterrupt:
        print("中止。")
        raise KeyboardInterrupt
