import cv2
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Initialize BLIP model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")


def generate_caption_for_frame(frame):
    """
    Generates a caption for a given video frame using the BLIP model.

    Args:
        frame (numpy.ndarray): The video frame in BGR format.

    Returns:
        str: The generated caption for the frame.
    """
    # Convert OpenCV frame (BGR) to PIL image (RGB)
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    # Prepare the image for the model
    inputs = processor(image, return_tensors="pt")

    # Generate a caption for the image
    with torch.no_grad():
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)

    return caption


def process_video(video_path, frames_interval=60):
    """
    Processes the video to generate captions for frames at the specified interval.

    Args:
        video_path (str): The path to the video file.
        frames_interval (int): The interval at which to process frames. Default is 60.

    Returns:
        str: The concatenated captions of the processed frames.
    """
    cap = cv2.VideoCapture(video_path)
    frame_index = 0

    captions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Only process every nth frame based on frames_interval
        if frame_index % frames_interval == 0:
            caption = generate_caption_for_frame(frame)
            captions.append(caption)
            print(f"Frame {frame_index}: {caption}")

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()

    # Generate the final summary based on captions
    summary = " ".join(captions)
    return summary


def handle_video_captioning(video_path):
    """
    Main handler to process video and print the generated captions summary.

    Args:
        video_path (str): The path to the video file.

    Returns:
        None
    """
    summary = process_video(video_path)
    print("\nFinal Summary:")
    print(summary)


# Example usage: calling the main handler function
video_path = "C:/Users/Win10/Desktop/KaleidooProject/sub.mp4"
handle_video_captioning(video_path)
