from pydub import AudioSegment
import os

def convert_audio(input_file, output_file, output_format):
    """
    将音频文件从一种格式转换为另一种格式。

    Args:
        input_file (str): 输入音频文件的路径。
        output_file (str): 输出音频文件的路径。
        output_format (str): 输出音频的格式 (例如: 'wav', 'mp3', 'flac')。
    """
    try:
        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format=output_format)
        print(f"成功将 {input_file} 转换为 {output_file}")
    except FileNotFoundError:
        print(f"错误：找不到输入文件 {input_file}")
    except Exception as e:
        print(f"转换过程中发生错误：{e}")

def main():
    # 设置输入和输出文件夹路径
    input_dir = r"D:\SingingApp\data"
    output_dir = r"D:\SingingApp\output_wav"

    # 确保输出文件夹存在，如果不存在则创建
    os.makedirs(output_dir, exist_ok=True)

    # 设置要转换的文件名和输出格式
    input_filename = "录音_20250108215542.m4a"  # 替换为你的 M4A 文件名
    output_filename = "test2.wav" # 替换为你想要的输出文件名
    output_format_type = "wav"      # 设置为 "wav"

    # 构建完整的输入和输出文件路径
    input_file_path = os.path.join(input_dir, input_filename)
    output_file_path = os.path.join(output_dir, output_filename)

    convert_audio(input_file_path, output_file_path, output_format_type)

if __name__ == "__main__":
    main()