# synesthesia: AI Music Video Generation
synesthesia is a Python project that allows you to create unique video experiences by combining existing videos with AI-generated music. It leverages the power of moviepy for video editing and audiocraft for music generation based on your textual prompts.

## Installation
To get started, you'll need Python 3.7 or later installed on your system. You can check your Python version by running python --version or python3 --version in your terminal.

Once you have Python, install the required libraries using pip:

```Bash
pip install moviepy.editor audiocraft
```
Note: Make sure you have FFmpeg installed for moviepy to function correctly. You can find FFmpeg download and installation instructions on the FFmpeg website: https://ffmpeg.org/download.html

## Usage
Save your video file: Ensure your video file is in a format supported by moviepy (e.g., MP4, AVI).
Run the script: Navigate to your project directory in the terminal and run the script using Python:
```Bash
python synesthesia.py
```

Follow the prompts: The script will ask you for:

- Input video filename (with a default value provided)
- Output video filename (with a default value provided)
- Audio prompt (a textual description for the music generation)


## Configuration
The script relies on the **synesthesia_config.py** file for default filenames. You can edit this file to set your preferred default names for the input and output videos, as well as the audio prompt.

### Additional Notes
This project is for educational and creative purposes.
The quality of the generated AI music depends on the capabilities of the audiocraft library and the chosen model.
Experiment with different audio prompts to explore the creative possibilities.