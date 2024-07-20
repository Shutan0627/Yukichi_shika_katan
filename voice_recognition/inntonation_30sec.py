import numpy as np
import librosa
import moviepy.editor as mp

#parameters
threshold_pitch = 0.1
threshold_volume = 0.1

def detect_intonation(y, sr, threshold_pitch = threshold_pitch ,threshold_volume =threshold_volume):
    # Extract pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitches = pitches[magnitudes > np.median(magnitudes)]
    pitches = pitches[pitches > 0]

    # Extract volume (RMS energy)
    hop_length = 512
    volume = librosa.feature.rms(y=y, frame_length=hop_length, hop_length=hop_length)[0]

    # Calculate pitch and volume variations
    pitch_variation = np.std(pitches)
    volume_variation = np.std(volume)

    # Determine if there's intonation
    has_pitch_variation = pitch_variation > threshold_pitch
    has_volume_variation = volume_variation > threshold_volume
    has_intonation = has_pitch_variation or has_volume_variation

    return has_intonation, has_pitch_variation, has_volume_variation, pitch_variation, volume_variation

def analyze_video(video_file, segment_duration=30):
    # Extract audio from video
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")

    # Load the audio file
    y, sr = librosa.load("temp_audio.wav")

    # Calculate the number of samples for each 30-second segment
    samples_per_segment = sr * segment_duration

    pitch_list = []

    # Analyze each 30-second segment
    for i in range(0, len(y), samples_per_segment):
        segment = y[i:i+samples_per_segment]
        
        if len(segment) < sr:  # Skip segments shorter than 1 second
            continue

        start_time = i / sr
        end_time = (i + len(segment)) / sr

        has_intonation, has_pitch_var, has_volume_var, pitch_var, volume_var = detect_intonation(segment, sr)

        print(f"Time: {start_time:.2f}s - {end_time:.2f}s")
        print(f"Has intonation: {has_intonation}")
        print(f"Has significant pitch variation: {has_pitch_var}")
        print(f"Has significant volume variation: {has_volume_var}")
        print(f"Pitch variation: {pitch_var:.2f}")
        print(f"Volume variation: {volume_var:.2f}")
        print("--------------------")
        pitch_list.append([start_time, end_time, has_intonation])
    return pitch_list