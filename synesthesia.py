import moviepy.editor
from moviepy.editor import VideoFileClip, AudioFileClip
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import synesthesia_config


def get_video_length(video_path):
    """
    Returns the duration of the input video in seconds.

    Args:
        video_path (str): Path to the video file.

    Returns:
        float: The duration of the video in seconds.

    Raises:
        ValueError: If the video file cannot be opened using moviepy.editor.
    """

    try:
        video = moviepy.editor.VideoFileClip(video_path)
        return video.duration
    except Exception as e:
        raise ValueError(f"Error opening video file: {video_path}. ({e})")


def create_audio(prompt, duration):
    """
    Creates an audio file using MusicGen with the given prompt and duration.

    Args:
        prompt (str): Textual prompt for the music generation.
        duration (float): Desired duration of the audio in seconds.

    Returns:
        str: Path to the generated audio file (.wav format).

    Raises:
        ValueError: If the duration is not a positive number.
    """

    if duration <= 0:
        raise ValueError("Duration must be a positive number.")

    output_audio_path = "outbox/audio"
    model = MusicGen.get_pretrained("melody")
    model.set_generation_params(duration=duration)
    wav = model.generate([prompt])

    # Potential usage of NumPy for audio manipulation (uncomment if needed)
    # wav = np.array(wav[0].cpu())  # Convert to NumPy array for further processing

    audio_write(
        output_audio_path,
        wav[0].cpu(),
        model.sample_rate,
        strategy="loudness",
        loudness_compressor=True,
    )
    return output_audio_path + ".wav"


def add_audio_to_video(video_path, audio_path, output_path):
    """
    Adds an audio file to a video file and saves the resulting video.

    Args:
        video_path (str): Path to the video file.
        audio_path (str): Path to the audio file.
        output_path (str): Path to save the resulting video file.

    Raises:
        ValueError: If any of the video or audio files cannot be opened
                    using moviepy.editor.AudioFileClip.
    """

    try:
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
    except Exception as e:
        raise ValueError(f"Error opening video or audio file. ({e})")

    # Loading the vertical video requires you to rotate them
    if video_clip.rotation == 90:
        print("Rotating Video")
        video_clip = video_clip.resize(video_clip.size[::-1])
        video_clip.rotation = 0

    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(output_path)


def synesthesia():
    """
    Combines a video with AI-generated music based on a prompt.

    This function gathers user input for video and audio filenames, retrieves
    the video length, generates audio based on the prompt with matching duration,
    and adds the audio to the video, saving the final output.

    It relies on the following functions:
        - get_video_length: Retrieves the duration of a video file.
        - create_audio: Generates an audio file using MusicGen with a prompt and duration.
        - add_audio_to_video: Adds an audio file to a video file and saves the result.

    These functions are expected to be defined elsewhere in your code.
    """

    # Load default filenames from synesthesia_config
    default_video_in = synesthesia_config.input_video
    default_video_out = synesthesia_config.output_video
    default_prompt = synesthesia_config.audio_prompt

    # Prompt user for filenames with default values
    video_in = (
        input(f"Input File Name (default: {default_video_in}): ") or default_video_in
    )
    video_out = (
        input(f"Output File Name (default: {default_video_out}): ") or default_video_out
    )
    prompt = input(f"Audio Prompt (default: {default_prompt}): ") or default_prompt

    # Get video length
    video_length = get_video_length(video_in)
    print(f"Video length: {video_length} seconds")

    # Generate audio with matching duration
    audio_in = create_audio(prompt, video_length)

    # Add audio to video and save
    add_audio_to_video(video_in, audio_in, video_out)

    print("Finished processing video!")


if __name__ == "__main__":
    synesthesia()
