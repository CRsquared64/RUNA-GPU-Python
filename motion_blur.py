import cv2
import numpy as np

def add_motion_blur(video_path, output_path, scale=0.5, alpha=0.75):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video opened successfully
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Resize dimensions based on scale factor
    new_width = int(frame_width * scale)
    new_height = int(frame_height * scale)

    # Create a VideoWriter object to save the output video with compression
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (new_width, new_height))

    # Variable to hold the previous frame
    prev_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the current frame to the lower resolution
        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Convert to float for blending
        resized_frame = resized_frame.astype(np.float32)

        # If there's a previous frame, blend it with the current frame
        if prev_frame is not None:
            # Blend the current frame with the previous frame using the alpha value
            blended_frame = cv2.addWeighted(resized_frame, 1 - alpha, prev_frame, alpha, 0)
        else:
            # If no previous frame, just use the current frame
            blended_frame = resized_frame

        # Convert back to uint8 for writing
        blended_frame = blended_frame.astype(np.uint8)

        # Write the blended frame to the output video
        out.write(blended_frame)

        # Update the previous frame for the next iteration
        prev_frame = resized_frame

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Motion blur applied and saved to {output_path}")

# Example usage
video_file = 'nbody_simulation.avi'  # Path to your input video
output_file = 'output_video_overlay.mp4'  # Path for the output video
add_motion_blur(video_file, output_file, scale=0.5, alpha=0.75)
