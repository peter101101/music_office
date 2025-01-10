import librosa
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import soundfile as sf
import torch
import torchaudio

class AudioProcessor:
    @staticmethod
    def record_audio(duration=5, sample_rate=44100):
        """
        高级录音功能，支持降噪和格式转换
        """
        print(f"开始录音，时长 {duration} 秒...")
        try:
            # 录制音频
            audio_data = sd.rec(int(duration * sample_rate), 
                                samplerate=sample_rate, 
                                channels=1, 
                                dtype='float32')
            sd.wait()
            
            # 简单降噪
            audio_data = AudioProcessor.denoise(audio_data)
            
            print("录音结束。")
            return audio_data.flatten()
        except Exception as e:
            print("录音过程中发生错误：", e)
            return None

    @staticmethod
    def denoise(audio_data, noise_threshold=0.1):
        """
        简单降噪处理
        """
        # 使用阈值过滤
        denoised = np.where(np.abs(audio_data) > noise_threshold, audio_data, 0)
        return denoised

    @staticmethod
    def load_audio(file, target_sr=44100):
        """
        增强音频加载功能
        """
        try:
            # 使用 librosa 读取并重采样
            audio_data, sr = librosa.load(file.stream, sr=target_sr)
            return audio_data
        except Exception as e:
            print(f"音频加载错误: {e}")
            return None

    @staticmethod
    def save_audio(file_path, audio_data, sample_rate=44100):
        """
        保存音频并支持多种格式
        """
        try:
            sf.write(file_path, audio_data, sample_rate)
            print(f"音频保存到：{file_path}")
        except Exception as e:
            print(f"音频保存错误: {e}")