import webbrowser
import os
import json
import re
import time
import datetime
import sys


def read_json(directory: str):
    json_files = [file for file in os.listdir(directory) if file.endswith(".json")]
    if len(json_files) == 0:
        raise FileNotFoundError("没有找到json文件！")

    valid_files = {}
    for file in json_files:
        if matsuri_pattern.match(file) is not None:
            liver = re.findall(r".+(?=_.+_\d{13}\.json)", file)[0]
            valid_files[re.findall(r"\d{13}(?=\.json)", file)[0]] = [
                file,
                "matsuri",
                liver,
            ]
        elif danmakus_pattern.match(file) is not None:
            liver = re.findall(r"(?<=\d_).+(?=\.json)", file)[0]
            valid_files[re.findall(r"\d{13}", file)[1]] = [file, "danmakus", liver]
    if len(valid_files) == 0:
        raise FileNotFoundError("没有找到合法的弹幕文件！从网站上下载后请不要改名")

    recent = "0"
    for key in valid_files.keys():
        if int(key) > int(recent):
            recent = key

    with open(valid_files[recent][0], encoding="utf8") as file:
        return {
            "data": json.load(file),
            "type": valid_files[recent][1],
            "start_time": recent,
            "liver": valid_files[recent][2],
        }


def parse_matsuri(data: object):
    danmu_rows = ""
    for i in data["full_comments"]:
        dm_time = i["time"] - data["info"]["start_time"]
        text = ""
        if "superchat_price" in i.keys():
            text = f"￥{i['superchat_price']} <b>{i['text']}</b>"
        elif "text" in i.keys():
            if "点点红包抽礼物" in i["text"]:
                continue
            text = i["text"]
        elif "gift_name" in i.keys():
            if no_gift:
                continue
            text = f"￥{i['gift_price']} <b>{i['gift_name']} * {i['gift_num']}</b>"

        danmu_rows += f'<tr><td>{datetime.datetime.fromtimestamp(dm_time // 1000, datetime.timezone.utc).strftime("%H:%M:%S")}.{dm_time % 1000}</td><td><a target="_blank" href="https://space.bilibili.com/{i["user_id"]}">{i["username"]}</a></td><td>{text}</td></tr>'

    return f"""<!DOCTYPE html>
<html>

<head>
    <title>{time.strftime("%Y%m%d", time.localtime(data['info']['start_time'] // 1000))}_直播弹幕文件</title>
    <link rel="stylesheet" href="../table_style.css">
</head>

<body>

    <p>开始时间：{time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(data['info']['start_time'] // 1000))}</p>
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

</html>"""


def parse_danmakus(data: object):
    danmu_rows = ""
    for i in data["danmakus"]:
        dm_time = i["sendDate"] - data["live"]["startDate"]
        text = ""
        if i["type"] == 0:
            if re.match(r"\[http", i["message"]) is not None:
                text = f'<img src="{i["message"][1:-1]}" alt="图片表情" height="50">'
            else:
                text = i["message"]
        elif i["type"] == 1 or i["type"] == 2 or i["type"] == 3:
            if no_gift:
                continue
            if i["price"] == 0:
                continue
            text = f"￥{i['price']} <b>{i['message']}</b>"

        danmu_rows += f'<tr><td>{datetime.datetime.fromtimestamp(dm_time // 1000, datetime.timezone.utc).strftime("%H:%M:%S")}.{dm_time % 1000}</td><td><a target="_blank" href="https://space.bilibili.com/{i["uId"]}">{i["uName"]}</a></td><td>{text}</td></tr>'

    return f"""<!DOCTYPE html>
<html>

<head>
    <title>{time.strftime("%Y%m%d", time.localtime(data['live']["startDate"] // 1000))}_直播弹幕文件</title>
    <link rel="stylesheet" href="../table_style.css">
</head>

<body>

    <p>开始时间：{time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(data['live']["startDate"] // 1000))}</p>
    <p>结束时间：{time.strftime("%Y.%m.%d %H:%M:%S", time.localtime(data['live']["stopDate"] // 1000))}</p>
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

</html>"""


def handle_default():
    result = read_json(os.getcwd())
    start_time = time.strftime(
        "%Y%m%d-%H%M%S", time.localtime(int(result["start_time"]) // 1000)
    )
    output_html = ""
    if result["type"] == "matsuri":
        output_html = parse_matsuri(result["data"])
    else:
        output_html = parse_danmakus(result["data"])

    if not os.path.exists("output"):
        os.makedirs("output")
    filename = f'output/{start_time}-{result["liver"]}.html'
    with open(filename, "w", encoding="utf8") as file:
        file.write(output_html)
    print("文件已生成:", os.path.join(os.getcwd(), filename))
    if open_browser:
        webbrowser.open(f"file:///{os.path.join(os.getcwd(), filename)}")


def handle_matsuri(filename: str):
    with open(filename, encoding="utf8") as file:
        data = json.load(file)
    output_html = parse_matsuri(data)
    start_time = time.strftime(
        "%Y%m%d-%H%M%S", time.localtime(data["info"]["start_time"] // 1000)
    )
    liver = re.findall(r".+(?=_.+_\d{13}\.json)", filename)[0]
    new_filename = f"output/{start_time}-{liver}.html"
    with open(new_filename, "w", encoding="utf8") as file:
        file.write(output_html)
    print("文件已生成:", os.path.join(os.getcwd(), new_filename))
    if open_browser:
        webbrowser.open(f"file:///{os.path.join(os.getcwd(), new_filename)}")


def handle_danmakus(filename: str):
    with open(filename, encoding="utf8") as file:
        data = json.load(file)
    output_html = parse_danmakus(data)
    start_time = time.strftime(
        "%Y%m%d-%H%M%S", time.localtime(data["live"]["startDate"] // 1000)
    )
    liver = re.findall(r"(?<=\d_).+(?=\.json)", file)[0]
    new_filename = f"output/{start_time}-{liver}.html"
    with open(new_filename, "w", encoding="utf8") as file:
        file.write(output_html)
    print("文件已生成:", os.path.join(os.getcwd(), new_filename))
    if open_browser:
        webbrowser.open(f"file:///{os.path.join(os.getcwd(), new_filename)}")


if __name__ == "__main__":
    open_browser = "-b" not in sys.argv
    no_gift = "-g" in sys.argv or "--gift" in sys.argv
    matsuri_pattern = re.compile(r".*_.*_\d{13}\.json$")
    danmakus_pattern = re.compile(r"\d{13}_\d{13}_.*_\d{1,16}_.+\.json$")

    if len(sys.argv) > 1 and sys.argv[1] == "-m":
        if len(sys.argv) == 2:
            print("错误：请提供文件名！")
        elif matsuri_pattern.match(sys.argv[2]) is None:
            print("错误：没有找到合法的弹幕文件！从网站上下载后请不要改名")
        else:
            handle_matsuri(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "-d":
        if len(sys.argv) == 2:
            print("错误：请提供文件名！")
        elif danmakus_pattern.match(sys.argv[2]) is None:
            print("错误：没有找到合法的弹幕文件！从网站上下载后请不要改名")
        else:
            handle_danmakus(sys.argv[2])
    else:
        try:
            handle_default()
        except Exception as e:
            print("错误:", e.args[0])
            input("按Enter键退出")
