from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip
import textwrap
import csv
import fnmatch
import os
import random

font_size = 24
font = "Roboto"
max_clip_duration = 8

def file_count(path):
    count = len(fnmatch.filter(os.listdir(path), '*.*'))
    return count

def create_text_clip(text, duration, max_text_width):
    wrapped_text = textwrap.fill(text, width=30)
    text_clip = TextClip(wrapped_text, fontsize=font_size, font=font, color='white', size=(max_text_width, None))
    text_clip = text_clip.set_position("center", "center")
    text_clip = text_clip.set_duration(duration)

    return text_clip

def add_quote_to_video(i, video_path, title, part_1, part_2):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Calculate the position and size of the text clips based on fixed aspect ratio (9:16)
    target_width = video_clip.h * 9 // 16  # Calculate width based on 9:16 aspect ratio
    target_height = video_clip.h

    # Calculate the font size based on the video height
    max_text_width = target_width - 200  # Adjust as needed

    crop_x = (video_clip.w - target_width) // 2
    crop_y = (video_clip.h - target_height) // 2

    # Crop the video to 9:16 aspect ratio
    cropped_video_clip = video_clip.crop(x1=crop_x, y1=crop_y, x2=crop_x + target_width, y2=crop_y + target_height)

    # Set the opacity of the video to 0.8
    cropped_video_clip = cropped_video_clip.set_opacity(0.3)


    part1_duration = max_clip_duration/2
    part2_duration = max_clip_duration - part1_duration
    title_duration = max_clip_duration

    # Create the title text clip
    title_clip = TextClip(title, fontsize=(font_size*2), font=font, color='white', size=(max_text_width, None))
    title_clip = title_clip.set_position(("center", target_height * 0.05))
    title_clip = title_clip.set_duration(title_duration)

    # Create the center text clips
    center_text_clips = []

    part1_clip = create_text_clip(part_1, part1_duration, max_text_width)
    center_text_clips.append(part1_clip)

    part2_clip = create_text_clip(part_2, part2_duration, max_text_width)
    center_text_clips.append(part2_clip)

    clips = [
        cropped_video_clip.set_duration(video_clip.duration),
        cropped_video_clip.set_opacity(0.8),
        part1_clip.set_start(0),
        part2_clip.set_start(part1_duration),
        title_clip.set_start(0)
    ]

    # Overlay the text clips on top of the video
    video_with_quotes = CompositeVideoClip(clips, size=(target_width, target_height))
    new_clip = video_with_quotes.subclip(0, 8)
    print(new_clip.duration)

    # Export the final video with the quote
    output_path = "./output/video"+str(i)+".mp4"
    new_clip.write_videofile(output_path, codec="libx264", bitrate="5000k")

if __name__ == "__main__":
    data_sheet_location = input("Enter the csv file: ")
    rows = []

    with open(data_sheet_location) as file_obj:
        #Remove heading
        heading = next(file_obj)

        #Create a reader object
        reader_obj = csv.reader(file_obj)

        for row in reader_obj:
            rows.append(row)


    total_rows = len(rows)

    #Iterate over each row in rows
    for i,row in enumerate(rows):
        print(f"Progress: [{i+1}/{total_rows}]")

        title = row[0]
        part_1 = row[1]
        part_2 = row[2]

        files_count = file_count('./vid_templates/')
        random_template_num = random.randint(1, files_count-1)
        #add_quote_to_video(i, "./vid_templates/temp4.mp4", title, part_1, part_2)
        add_quote_to_video(i, "./vid_templates/temp"+str(random_template_num)+".mp4", title, part_1, part_2)

    print("Done creating the videos!")
    
