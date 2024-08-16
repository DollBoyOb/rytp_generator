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
def pitchclip(clip, duration):
  random_timestamp = random.uniform(0, duration/2)
  clip = clip.subclip(random_timestamp, random_timestamp+(duration/6))
  array_pitch = []
  for i in range(5):
    clip_part = clip.fx(vfx.speedx, 1+i/2)
    array_pitch.append(clip_part)
  pitch_final = concatenate_videoclips(array_pitch)
  return pitch_final

# Суп рандом - случайная скорость с каждой итерацией (10 раз)
def soup_random(clip, duration):
    array_pitch = []
    for x in range(10):
        random_timestamp = random.uniform(duration/15, duration)
        if duration<0.5: part_duration = duration/10
        else: part_duration = 0.5
        clip_p = clip.subclip(random_timestamp-part_duration-0.02, random_timestamp)
        clip_part = clip_p.fx(vfx.speedx, 3.5+random.uniform(0.2, 2))
        array_pitch.append(clip_part)
    pitch_final = concatenate_videoclips(array_pitch)
    return pitch_final

support_suffixes = [".mp4",".avi",".3gp",".mov"]
sources_dirty = os.listdir(path="media")
sources = []
for i in range(len(sources_dirty)):
    if Path(f"/media/{sources_dirty[i]}").suffix in support_suffixes:
        sources.append(sources_dirty[i])
print("\nСурсы, использующий генератор:",sources,"\n")
if len(sources)<=1:
    print("\nВнимание! В вашей папке сурсов меньше нормы (2 сурса)\n")
print("Идёт генерирование пупа... Это может занять более 10 минут")
all_clips = [intro]
for x in range(clips_range):
    try:
        rand_clip = random.choice(sources)
        clip_for_rytp = VideoFileClip(f"media/{rand_clip}")
        random_clip_of_clip = random.randint(0, abs(int((clip_for_rytp.duration)-maximum)))
        clip_for_rytp = clip_for_rytp.subclip(random_clip_of_clip, random_clip_of_clip+random.uniform(minimum, maximum))
    except OSError:
        print("Найден нечитаемый сурс:", rand_clip)
        sources.remove(rand_clip)
    # тут добавляются эффекты
    for i in range(random.randint(1,3)):
      try:
          effect = random.choice(effects)
          if effect=='.set_audio(second_clip.audio)':
              rand_second_clip = random.choice(sources)
              second_clip = VideoFileClip(f"media/{rand_second_clip}")
              random_clip_of_second_clip = random.randint(0, abs(int((second_clip.duration)-maximum))) # эта хуёвина выдавала постоянно empty randrange, поэтому я прибавил 3 к этой хуйне (я сам не понимаю, что тут происходит)
              second_clip = second_clip.subclip(random_clip_of_second_clip, random_clip_of_second_clip+random.uniform(minimum,maximum))
        
          clip_rytp = eval(f'clip_for_rytp{effect}')
          choice = random.choice(percentage_array)
          try:
            if choice == "РАНДОМ": clip_rytp = soup_random(clip_rytp, clip_rytp.duration)
            if choice == "ПИТЧ": clip_rytp = pitchclip(clip_rytp, clip_rytp.duration)
            if choice == "САС": clip_rytp = sas(clip_rytp)
            if choice == "НИЧЕГО": pass
          except:
            pass
      except OSError:
          print("Найден нечитаемый сурс:", rand_second_clip)
          sources.remove(rand_second_clip)
    all_clips.append(clip_rytp)
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
