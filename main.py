import pysrt
import glob
import re
import json
from collections import OrderedDict


SRT_DIR = "/foo/bar"


def write_jsonl(data, file_name):
    with open(file_name, "w", encoding="utf-8") as file:
        for item in data:
            json.dump(item, file)
            file.write("\n")


def unique_ordered_list(items):
    return list(OrderedDict.fromkeys(items))


def remove_junk(text):
    text = text.replace("\n", " ")
    text = text.replace("WWW.MY-SUBS.CO", "")
    text = text.replace("♪", "")
    text = text.replace("<i>", "")
    text = text.replace("</i>", "")

    text = re.sub(r"^\([^)]+\)$", "", text, flags=re.MULTILINE)

    return text.strip()


def srt_to_text(srt_file):
    subs = pysrt.open(srt_file, encoding="utf-8")

    return [remove_junk(sub.text) for sub in subs if remove_junk(sub.text).strip()]


def create_dataset(items):
    dataset = []
    for i in range(len(items) - 1):
        pair = {"prev": items[i], "next": items[i + 1]}
        dataset.append(pair)
    return dataset


srt_files = glob.glob(SRT_DIR + "*.srt")

subs = []
for srt_file in srt_files:
    subs.extend(srt_to_text(srt_file))

dataset = create_dataset(unique_ordered_list(subs))

print(len(dataset))
write_jsonl(dataset, "dataset.jsonl")
