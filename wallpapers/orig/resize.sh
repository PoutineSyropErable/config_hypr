#!/bin/bash 


input="./anime_cyberpunk_girl_near4k.png"
output="./anime_cyberpunk_girl_1440p.png"
resolution="2560x1440"
target_aspect_ratio=1.7777777  # 16:9

# Get original dimensions
orig_w=$(identify -format "%w" "$input")
orig_h=$(identify -format "%h" "$input")
echo "Original size: ${orig_w}x${orig_h}"

# Calculate crop height to maintain 16:9 aspect ratio based on original width
crop_height=$(( orig_width * 9 / 16 ))



#method one. (too bad)
# convert "$input" -gravity center -crop "$resolution+0+0" +repage "$output"

#method 2, using bottom crop
# Crop bottom: keep top-left, cut off bottom part
convert "$input" -crop "${orig_w}x${crop_height}+0+0" +repage -resize "$resolution" "${output%.png}_bottomcrop.png"



#method 3: resize, allow stretch



