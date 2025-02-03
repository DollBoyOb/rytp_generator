from moviepy.editor import *
from pathlib import Path
import random
import os
import moviepy
import inspect

module_path = inspect.getfile(moviepy)
path_file_needed = os.path.dirname(module_path)+r"\video\fx\resize.py"

with open(path_file_needed, 'r') as f:
    file_to_update = f.read()
    if file_to_update.find("ANTIALIAS")!=-1:
        with open(path_file_needed, 'w') as f:
            f.write(file_to_update.replace('ANTIALIAS', 'LANCZOS'))
    f.close()

intro = VideoFileClip("intro.mp4")
print("""
             _                                           _
            | |                                         | |
  _ __ _   _| |_ _ __     __ _  ___ _ __   ___ _ __ __ _| |_ ___  _ __
 | '__| | | | __| '_ \   / _` |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 | |  | |_| | |_| |_) | | (_| |  __/ | | |  __/ | | (_| | || (_) | |
 |_|   \__, |\__| .__/   \__, |\___|_| |_|\___|_|  \__,_|\__\___/|_|
        __/ |   | |       __/ |
       |___/    |_|      |___/
""")
clips_range = int(input("Количество вставок в пупе (25 вставок = +-одна минута): "))
minimum = float(input("Минимальная продолжительность одной вставки в пупе: "))
maximum = float(input("Максимальная продолжительность одной вставки в пупе: "))
random_shit = [i/10 for i in range(5, 25, 1)]
effects = ['.fx(vfx.speedx, random.choice(random_shit))', '.fx(vfx.mirror_x)', '.fx(vfx.time_mirror)', '.set_audio(second_clip.audio)', '.fx(vfx.invert_colors)']
percentage_array = ["САС"] * 35 + ["РАНДОМ"] * 35 + ["ПИТЧ"] * 20 + ["НИЧЕГО"] * 10

# САС эффект
def sas(clip):
    reverse = clip.fx(vfx.time_mirror)
    saas_clip = concatenate_videoclips([clip, reverse])
    return saas_clip

# Питч эффект - с каждой итерацией (5 раз) клип становится всё быстрей и быстрей
def pitchclip(clip):
    random_timestamp = random.uniform(0, clip.duration-(clip.duration/5))
    clip_n = clip.subclip(random_timestamp, random_timestamp+(clip.duration/5))

    return concatenate_videoclips([clip_n.fx(vfx.speedx, 1+i/2) for i in range(5)])

# Суп рандом - случайная скорость с каждой итерацией (10 раз)
def soup_random(clip):
    random_timestamp = random.uniform(0, clip.duration-(clip.duration/5))
    clip_n = clip.subclip(random_timestamp, random_timestamp+(clip.duration/5))

    return concatenate_videoclips([clip_n.fx(vfx.speedx, random.uniform(1, 10)) for i in range(10)])


support_suffixes = [".mp4",".avi",".3gp",".mov"]
sources = list(filter(lambda x: Path(f"/media/{x}").suffix in support_suffixes, os.listdir(path="media")))

print("\nСурсы, использующий генератор:",sources,"\n")

print("Идёт генерирование пупа... Это может занять более 10 минут")
all_clips = [intro]
for x in range(clips_range):
    random_effects = [random.choice(effects) for i in range(random.randint(1,3))]

    if '.set_audio(second_clip.audio)' in random_effects:
        second_clip = VideoFileClip(f"media/{random.choice(sources)}")
        crop = random.uniform(0, second_clip.duration-maximum)
        second_clip = second_clip.subclip(crop, crop + random.uniform(minimum, maximum))

    first_clip = VideoFileClip(f"media/{random.choice(sources)}")
    crop = random.uniform(0, first_clip.duration-maximum)
    clip_rytp = eval(f"first_clip.subclip(crop, crop + random.uniform(minimum, maximum)){''.join(random_effects)}")
    print(clip_rytp.duration)
    c = random.choice(percentage_array)
    try:
        if c == "РАНДОМ": clip_rytp = soup_random(clip_rytp)
        if c == "ПИТЧ":   clip_rytp = pitchclip(clip_rytp)
        if c == "САС":    clip_rytp = sas(clip_rytp)
    except:
        pass

    all_clips.append(clip_rytp)
    clip_rytp.close()

    percentage_rytp = int((len(all_clips)/(clips_range+1))*100)
    print(f"Выполнено {len(all_clips)}/{clips_range+1} - {percentage_rytp}%")

print("Видео готово, остался рендер")
rytp_final = concatenate_videoclips(all_clips)
resolutions = [(320, 240), (640, 360), (1280, 720), (1024, 768)]
resolutions_img = ["320x240 - 240p", "640x360 - 360p", "1280x720 - 720p", "1024x768 - 4:3 разрешение"]

print("Выберите разрешение, в котором вы будете рендерить видео")
print('\n'.join([f'{i}. {resolutions_img[i]}' for i in range(len(resolutions_img))]))

res = int(input("-> "))
rytp = rytp_final.resize(resolutions[res])
input_fps = int(input("Введите кол-во фпс, в котором вы будете рендерить видео: "))
print("Идёт рендер пупа...")
rytp.write_videofile('new_rytp.mp4', fps=input_fps)
rytp.close()
