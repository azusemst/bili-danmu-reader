import webbrowser
import os
import json
import re
import time


def read_json(directory: str):
    json_files = [file for file in os.listdir(directory) if file.endswith(".json")]
    if len(json_files) == 0:
        raise OSError("没有找到json文件")

    matsuri_pattern = re.compile(r".*_.*_\d{13}\.json$")
    danmakus_pattern = re.compile(r"\d{13}_\d{13}_.*_\d{1,16}_.+\.json$")
    valid_files = {}
    for file in json_files:
        if matsuri_pattern.match(file) is not None:
            valid_files[re.findall(r"\d{13}(?=\.json)", file)[0]] = [file, "matsuri"]
        elif danmakus_pattern.match(file) is not None:
            valid_files[re.findall(r"\d{13}", file)[1]] = [file, "danmakus"]
    if len(valid_files) == 0:
        raise OSError("没有找到合法的弹幕文件")

    recent = "0"
    for key in valid_files.keys():
        if int(key) > int(recent):
            recent = key

    with open(os.path.join(directory, valid_files[recent][0]), encoding="utf8") as file:
        try:
            return {"data": json.load(file), "type": valid_files[recent][1]}
        except json.JSONDecodeError:
            raise OSError("不合法的json文件")

def parse_matsuri(data: object):
    danmu_rows = ''
    for i in data['full_comments']:
        dm_time = i['time'] - data['info']['start_time']
        text = ''
        if 'superchat_price' in i.keys():
            text = f"￥{i['superchat_price']} <b>{i['text']}</b>"
        elif 'text' in i.keys():
            if '点点红包抽礼物' in i['text']:
                continue
            text = i['text']
        elif 'gift_name' in i.keys():
            text = f"￥{i['gift_price']} <b>{i['gift_name']} * {i['gift_num']}</b>"
        
        danmu_rows += f'<tr><td>{time.strftime("%H:%M:%S", time.localtime(dm_time // 1000))}.{dm_time % 1000}</td><td><a target="_blank" href="https://space.bilibili.com/{i["user_id"]}">${i["username"]}</a></td><td>${text}</td></tr>'
    
    return f'''<!DOCTYPE html>
<html>

<head>
    <title>{time.strftime("%Y.%m.%d", time.localtime(data['info']['start_time']))}_直播弹幕文件</title>
    <link rel="stylesheet" href="../table_style.css">
</head>

<body>

    <p>开始时间：{time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(data['info']['start_time']))}</p>
    <br><br>
    <table>
        <tr>
            <th>时间</th>
            <th>用户</th>
            <th>内容</th>
        </tr>
        {danmu_rows}
    </table>

</body>

</html>'''


if __name__ == "__main__":
    result = read_json(os.getcwd() + "/test_input")
    if result['type'] == 'matsuri':
        parse_matsuri(result['data'])
