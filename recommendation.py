import os
import numpy as np
import soundfile as sf
import database  # Ensure this import is present

class SongRecommendation:
    @staticmethod
    def recommend_songs(user_features, top_n=5):
        """
        基于用户特征推荐歌曲
        """
        all_songs = database.load_songs_from_csv()
        
        # 特征向量化
        song_features = [
            [
                float(song['features'].get('pitch_range', 0)),
                float(song['features'].get('tempo', 0))
            ] for song in all_songs
        ]
        
        user_vector = [
            user_features.get('pitch_range', 0),
            user_features.get('tempo', 0)
        ]
        
        # 简单的相似度计算
        similarities = [
            np.linalg.norm(np.array(user_vector) - np.array(features)) 
            for features in song_features
        ]
        
        # 根据相似度排序并推荐
        recommended_indices = np.argsort(similarities)[:top_n]
        recommended_songs = [all_songs[i] for i in recommended_indices]
        
        return recommended_songs

    @staticmethod
    def ai_sing(user_features, song):
        """
        模拟AI生成音频
        """
        # 确保 AI 生成目录存在
        ai_singing_dir = 'ai_singing'
        os.makedirs(ai_singing_dir, exist_ok=True)
        
        # 生成文件名
        output_filename = f"ai_singing_{song['title']}.wav"
        output_path = os.path.join(ai_singing_dir, output_filename)
        
        try:
            # 生成简单的模拟音频
            duration = 10  # 10秒音频
            sample_rate = 44100
            
            # 生成正弦波模拟音频
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            
            # 根据用户特征调整音频
            pitch = user_features.get('pitch_range', 220)  # 默认音高
            audio_data = 0.5 * np.sin(2 * np.pi * pitch * t)
            
            # 添加一些随机性
            audio_data += 0.1 * np.random.normal(size=audio_data.shape)
            
            # 保存音频文件
            sf.write(output_path, audio_data, sample_rate)
            
            return output_filename
        
        except Exception as e:
            print(f"AI演唱生成错误: {e}")
            return "ai_singing_error.wav"