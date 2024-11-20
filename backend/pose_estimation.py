import cv2
import mediapipe as mp
import numpy as np

## setting up >>>
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils  # For drawing pose landmarks on the image

def calculate_angle(a, b, c):
    try:
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        # Calculate vectors
        ab = a - b
        bc = c - b

        dot_product = np.dot(ab, bc)
        magnitude_ab = np.linalg.norm(ab)
        magnitude_bc = np.linalg.norm(bc)

        angle = np.arccos(dot_product / (magnitude_ab * magnitude_bc))
        return np.degrees(angle)
    except Exception as e:
        print(f"Error calculating angle: {e}")
        return None  # Return None if an error occurs

def process_video(input_path, output_path):


    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))


    while cap.isOpened():
        try:
            success, frame = cap.read()
            if not success:
                print("hululu")
                break
            # Convert the image to RGB (MediaPipe uses RGB, but OpenCV uses BGR)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame for pose landmarks
            result = pose.process(rgb_frame)

            if result.pose_landmarks:
                # Draw pose landmarks on the frame
                mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                landmarks = result.pose_landmarks.landmark

                h, w, _ = frame.shape

                def get_landmark(id):
                    try:
                        if landmarks[id].visibility > 0.5:
                            return [int(landmarks[id].x * w), int(landmarks[id].y * h)]
                        else:
                            return None
                    except Exception as e:
                        print(f"Error accessing landmark {id}: {e}")
                        return None

                # Key body parts landmarks
                left_shoulder = get_landmark(11)
                right_shoulder = get_landmark(12)
                left_elbow = get_landmark(13)
                right_elbow = get_landmark(14)
                left_wrist = get_landmark(15)
                right_wrist = get_landmark(16)
                left_hip = get_landmark(23)
                right_hip = get_landmark(24)
                left_knee = get_landmark(25)
                right_knee = get_landmark(26)
                left_ankle = get_landmark(27)
                right_ankle = get_landmark(28)

                # Function to calculate and display angle if the landmarks are available
                def display_angle(a, b, c, label):
                    if a and b and c:
                        angle = calculate_angle(a, b, c)
                        if angle is not None:
                            cv2.putText(frame, str(int(angle)), tuple(b), cv2.FONT_HERSHEY_SIMPLEX,
                                        1, (255, 0, 0), 2, cv2.LINE_AA)
                            print(f"{label} Angle: {angle}")

                # Calculate and display angles for all key joints
                display_angle(left_shoulder, left_elbow, left_wrist, "Left Elbow")
                display_angle(right_shoulder, right_elbow, right_wrist, "Right Elbow")
                display_angle(left_hip, left_knee, left_ankle, "Left Knee")
                display_angle(right_hip, right_knee, right_ankle, "Right Knee")
                display_angle(left_elbow, left_shoulder, left_hip, "Left Shoulder")
                display_angle(right_elbow, right_shoulder, right_hip, "Right Shoulder")
                display_angle(left_knee, left_hip, left_shoulder, "Left Hip")
                display_angle(right_knee, right_hip, right_shoulder, "Right Hip")

                pressure_points = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]  # Shoulders, elbows, hips, knees, ankles

                for point in pressure_points:
                    try:
                        cx, cy = int(landmarks[point].x * frame.shape[1]), int(landmarks[point].y * frame.shape[0])
                        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), cv2.FILLED)  # Mark as a red circle
                    except Exception as e:
                        print(f"Error drawing circle for point {point}: {e}")

            out.write(frame)

        except Exception as e:
            print(f"Error in main loop: {e}")

    cap.release()
    out.release()
    return "Video Done Congrats!!"
