import os
from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import librosa
import numpy as np

# 导入自定义模块
from audio_processing import AudioProcessor
from evaluation import SingingEvaluation
from recommendation import SongRecommendation
import database

app = Flask(__name__)
CORS(app)  # 解决跨域问题

# 确保上传目录存在
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    """
    渲染主页
    """
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_audio():
    """
    处理音频文件的主路由
    """
    try:
        # 检查是否有文件上传
        if 'file' not in request.files:
            return jsonify({"error": "未检测到音频文件"}), 400
        
        file = request.files['file']
        
        # 保存上传的文件
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # 加载音频数据
        audio_data, sample_rate = librosa.load(file_path)
        
        # 歌唱评估
        evaluation_report = SingingEvaluation.evaluate_singing(audio_data, sample_rate)
        
        # 特征提取
        user_features = {
            'pitch_range': evaluation_report['pitch_analysis']['mean_pitch'],
            'tempo': evaluation_report['rhythm_analysis']['tempo']
        }
        
        # 歌曲推荐
        recommended_songs = SongRecommendation.recommend_songs(user_features)
        
        # AI演唱（模拟）
        ai_singing_path = SongRecommendation.ai_sing(user_features, recommended_songs[0])
        
        # 返回结果
        return jsonify({
            'evaluation': evaluation_report,
            'recommended_songs': recommended_songs,
            'ai_singing_path': ai_singing_path
        })
    
    except Exception as e:
        # 详细的错误日志
        print(f"处理音频时发生错误: {str(e)}")
        return jsonify({
            'error': '音频处理失败',
            'details': str(e)
        }), 500

# 其他路由保持不变

if __name__ == '__main__':
    # 确保创建必要的目录
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('ai_singing', exist_ok=True)
    
    # 运行Flask应用
    app.run(
        host='0.0.0.1',  # 修改为本地回环地址
        port=5000,       
        debug=True       
    )