# BarbellSpeed

## How to run it?

- First, make sure you have python, pip and git installed on your machine
- Clone the repo and run pip install -r requirements.txt
- Create an aruco marker that can be put on the end of a barbell. I used a piece of plywood with the marker glued on it and the other end attached to a neodymium magnet.
- Record a video from the side with the ArUco marker attached, place your camera on a stable surface(**Do not film from hand**) and preferably cut out the racking/deracking phase.
- Add the video to the video folder.
- Run the tracker:

```bash
python tracker.py --video (name_of_your_video.mp4) --output (name_of_output_no_mp4)
```

If you want to, edit weight and a boolean that controls if the weight and reps are shown on the video.

<!-- thoughts -->
In squat its printing positive number for y_velocity and is_eccentric is True
