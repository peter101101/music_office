def get_all_songs():
    """
    模拟歌曲数据库
    """
    return [
        {
            "title": "演员",
            "artist": "薛之谦",
            "features": {
                "pitch_range": 220,
                "tempo": 90
            }
        },
        {
            "title": "稻香",
            "artist": "周杰伦",
            "features": {
                "pitch_range": 250,
                "tempo": 100
            }
        }
    ]

def load_songs_from_csv():
    """
    从CSV加载歌曲（暂时返回模拟数据）
    """
    return get_all_songs()