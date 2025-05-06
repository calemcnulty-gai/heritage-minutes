# A250: American History Shorts

## Overview
A250 is a project to create 250 cinematic, 60-second videos that bring American history and the Bill of Rights to life for students on platforms like TikTok. Partnering with Stand Together and the Bill of Rights Institute, we aim to reach 10 million students by July 4, 2027, turning history into must-watch, must-share content.

## Goals
- Produce engaging, swipe-length stories scripted for social media
- Include interactive elements like polls to spark debate on issues like free speech
- Provide free lesson packs for teachers to use in classrooms
- Achieve viral reach through stitching and dueting on TikTok

## Project Structure
```
project_root/
 |-- .cursor/
 |     |-- rules/
 |     |-- project_plan.md
 |     |-- changelog.md
 |
 |-- src/
 |     |-- video_generation/    # Code for generating videos
 |     |-- scripts/            # Video script templates
 |
 |-- videos/                   # Generated video assets
 |
 |-- scripts/                  # Project scripts and utilities
 |
 |-- README.md
```

## Setup & Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Hugging Face API access:
   ```bash
   export HUGGINGFACE_API_KEY=your_api_key_here
   ```

## Usage
1. Generate a new video:
   ```bash
   python src/video_generation/generate.py --script path/to/script.md
   ```
2. Process and optimize for TikTok:
   ```bash
   python src/video_generation/optimize.py --input path/to/video.mp4
   ```

## Testing
Run the test suite:
```bash
pytest tests/
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License - See LICENSE file for details 