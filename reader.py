import webbrowser
import os
import json
import re


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


if __name__ == "__main__":
    print(read_json(os.getcwd() + "/test_input"))
