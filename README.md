# CV_tool
image_processing

# trim video 
`ffmpeg -i input.mp4 -ss 00:00:31 -to 00:00:48 -c copy output.avi`

# increase/decrease speed (-r is the output frame)
`ffmpeg -y -i output.avi -r 30  -b:v 3M -strict -2 -movflags faststart -filter:v "setpts=0.5*PTS" destination.mp4`

# convert video to images
`ffmpeg -i cars.mp4 -vf scale=640:480 fps=15 %05d.jpg`

# convert images to video
`ffmpeg -framerate 15 -pattern_type glob -i '*.jpg' -r 30 -pix_fmt yuv420p out.mp4`
