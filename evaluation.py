import librosa
import numpy as np
import scipy.stats

class SingingEvaluation:
    @staticmethod
    def evaluate_singing(audio_data, sample_rate=44100):
        """
        专业的歌唱能力多维度评估
        """
        try:
            pitch_analysis = SingingEvaluation.analyze_pitch(audio_data, sample_rate)
            rhythm_analysis = SingingEvaluation.analyze_rhythm(audio_data, sample_rate)
            timbre_analysis = SingingEvaluation.analyze_timbre(audio_data, sample_rate)
            breath_analysis = SingingEvaluation.analyze_breath(audio_data, sample_rate)

            # 构建评估报告
            evaluation_report = {
                'pitch_analysis': pitch_analysis,
                'rhythm_analysis': rhythm_analysis,
                'timbre_analysis': timbre_analysis,
                'breath_analysis': breath_analysis
            }

            # 计算综合评分
            evaluation_report['overall_score'] = SingingEvaluation.calculate_overall_score(evaluation_report)
            
            # 生成改进建议
            evaluation_report['improvement_suggestions'] = SingingEvaluation.generate_suggestions(evaluation_report)

            return evaluation_report
        except Exception as e:
            print(f"歌唱评估错误: {e}")
            return {
                'error': str(e),
                'overall_score': 0,
                'pitch_analysis': {},
                'rhythm_analysis': {},
                'timbre_analysis': {},
                'breath_analysis': {},
                'improvement_suggestions': []
            }

    @staticmethod
    def analyze_pitch(audio_data, sample_rate):
        """
        音高分析
        """
        try:
            # 使用 librosa 的音高跟踪
            pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sample_rate)
            
            # 过滤有效的音高值
            valid_pitches = pitches[pitches > 0]
            
            if len(valid_pitches) == 0:
                return {
                    'mean_pitch': 0,
                    'pitch_stability': 0,
                    'pitch_range': 0,
                    'pitch_quality': "无法分析"
                }
            
            pitch_analysis = {
                'mean_pitch': float(np.mean(valid_pitches)),
                'pitch_stability': float(np.std(valid_pitches)),
                'pitch_range': float(np.max(valid_pitches) - np.min(valid_pitches)),
            }
            
            # 音高质量评估
            pitch_analysis['pitch_quality'] = (
                "优秀" if pitch_analysis['pitch_stability'] < 10 else 
                "良好" if pitch_analysis['pitch_stability'] < 20 else 
                "需要改进"
            )
            
            return pitch_analysis
        except Exception as e:
            print(f"音高分析错误: {e}")
            return {
                'mean_pitch': 0,
                'pitch_stability': 0,
                'pitch_range': 0,
                'pitch_quality': "分析失败"
            }

    @staticmethod
    def analyze_rhythm(audio_data, sample_rate):
        """
        节奏分析
        """
        try:
            # 使用 librosa 的节奏跟踪
            tempo, beat_frames = librosa.beat.beat_track(y=audio_data, sr=sample_rate)
            
            # 计算节奏稳定性
            onset_env = librosa.onset.onset_strength(y=audio_data, sr=sample_rate)
            tempo_variation = float(np.std(np.diff(beat_frames)))
            
            rhythm_analysis = {
                'tempo': float(tempo),
                'beat_count': int(len(beat_frames)),
                'tempo_consistency': tempo_variation,
                'rhythm_quality': (
                    "非常稳定" if tempo_variation < 5 else 
                    "基本稳定" if tempo_variation < 10 else 
                    "节奏不稳"
                )
            }
            
            return rhythm_analysis
        except Exception as e:
            print(f"节奏分析错误: {e}")
            return {
                'tempo': 0,
                'beat_count': 0,
                'tempo_consistency': 0,
                'rhythm_quality': "分析失败"
            }

    @staticmethod
    def analyze_timbre(audio_data, sample_rate):
        """
        音色分析
        """
        try:
            # 频谱质心
            spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sample_rate)[0]
            
            # 频谱带宽
            spectral_bandwidths = librosa.feature.spectral_bandwidth(y=audio_data, sr=sample_rate)[0]
            
            timbre_analysis = {
                'spectral_centroid': float(np.mean(spectral_centroids)),
                'spectral_bandwidth': float(np.mean(spectral_bandwidths)),
                'timbre_richness': float(np.std(spectral_centroids)),
                'timbre_quality': (
                    "音色丰富" if np.std(spectral_centroids) > 500 else 
                    "音色一般" if np.std(spectral_centroids) > 200 else 
                    "音色单一"
                )
            }
            
            return timbre_analysis
        except Exception as e:
            print(f"音色分析错误: {e}")
            return {
                'spectral_centroid': 0,
                'spectral_bandwidth': 0,
                'timbre_richness': 0,
                'timbre_quality': "分析失败"
            }

    @staticmethod
    def analyze_breath(audio_data, sample_rate):
        """
        气息分析
        """
        try:
            # 使用 librosa 的静音检测
            intervals = librosa.effects.split(audio_data)
            
            breath_analysis = {
                'breath_intervals': int(len(intervals)),
                'silence_ratio': float(len(intervals) / len(audio_data)),
                'breath_quality': (
                    "气息充沛" if len(intervals) > 10 else 
                    "气息一般" if len(intervals) > 5 else 
                    "气息不足"
                )
            }
            
            return breath_analysis
        except Exception as e:
            print(f"气息分析错误: {e}")
            return {
                'breath_intervals': 0,
                'silence_ratio': 0,
                'breath_quality': "分析失败"
            }

    @staticmethod
    def calculate_overall_score(analysis_report):
        """
        综合评分计算
        """
        try:
            # 安全地获取分数
            pitch_score = 100 - min(analysis_report['pitch_analysis'].get('pitch_stability', 0) * 5, 30)
            rhythm_score = 100 - min(analysis_report['rhythm_analysis'].get('tempo_consistency', 0) * 5, 20)
            timbre_score = 80 + min(np.log(analysis_report['timbre_analysis'].get('spectral_centroid', 1) + 1) * 5, 20)
            breath_score = 90 - min(analysis_report['breath_analysis'].get('silence_ratio', 0) * 50, 30)
            
            overall_score = (pitch_score + rhythm_score + timbre_score + breath_score) / 4
            return round(max(min(overall_score, 100), 0), 2)
        except Exception as e:
            print(f"综合评分计算错误: {e}")
            return 0

    @staticmethod
    def generate_suggestions(analysis_report):
        """
        生成个性化改进建议
        """
        suggestions = []
        
        try:
            pitch_analysis = analysis_report.get('pitch_analysis', {})
            if pitch_analysis.get('pitch_quality') == "需要改进":
                suggestions.append("音高不稳定，建议进行音准训练和声音控制练习")
            
            rhythm_analysis = analysis_report.get('rhythm_analysis', {})
            if rhythm_analysis.get('rhythm_quality') == "节奏不稳":
                suggestions.append("节奏控制需要改进，建议使用节拍器进行规律性训练")
            
            timbre_analysis = analysis_report.get('timbre_analysis', {})
            if timbre_analysis.get('timbre_quality') == "音色单一":
                suggestions.append("音色表现单一，建议扩展声音表现力，尝试不同的发声技巧")
            
            breath_analysis = analysis_report.get('breath_analysis', {})
            if breath_analysis.get('breath_quality') == "气息不足":
                suggestions.append("气息控制薄弱，建议进行腹式呼吸和肺活量训练")
        except Exception as e:
            print(f"建议生成错误: {e}")
            suggestions = ["无法生成具体建议，请重新上传音频"]
        
        return suggestions if suggestions else ["无法生成具体建议，请重新上传音频"]