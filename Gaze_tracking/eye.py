import cv2
from Gaze_tracking.gaze_tracking import GazeTracking

def gaze_tracking(video_path, threshold=1.0):
    gaze = GazeTracking()
    video = cv2.VideoCapture(video_path)

    # Initialize the counter and the start time
    center_count = 0
    total_time = 0
    duration = 0.0
    made_comment = False
    fps = video.get(cv2.CAP_PROP_FPS)
    s_fps = 1.0 / fps
    eye_list = []

    def current_eye_status(gaze):
        if gaze.is_blinking():
            return False
        elif gaze.is_right():
            return True
        elif gaze.is_left():
            return True
        elif gaze.is_center():
            return True
        return False

    def is_center(gaze):
        if gaze.is_center():
            return True
        return False
    


    was_center = False
    for i in range(int(video.get(cv2.CAP_PROP_FRAME_COUNT))):
        # We get a new frame from the video
        ret, frame = video.read()

        # We send this frame to GazeTracking to analyze it
        
        gaze.refresh(frame)
        frame = gaze.annotated_frame()

        if not current_eye_status(gaze):
            pass
        else:
            if (not is_center(gaze)) and was_center:
                if duration < threshold:
                    duration = 0.0
                    was_center = False
                    made_comment = False
                else:
                    pass
            elif (is_center(gaze)) and (not was_center):
                if duration < threshold:
                    duration = 0.0
                    was_center = True
                    made_comment = False
                else:
                    eye_list.append([total_time, is_center(gaze), duration])
                    duration = 0.0
                    was_center = True
                    made_comment = False
            else:
                if (duration > threshold) and (not made_comment) and (not is_center(gaze)):
                    print("You are not looking at the camera")
                    made_comment = True
                else:
                    pass
                    

        if is_center(gaze):
            center_count += s_fps

            

            
        duration += s_fps

        # Increment the counter by the time elapsed since the last frame

        total_time += s_fps



    video.release()

    return eye_list
