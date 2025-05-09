# Heritage Minutes: American History Shorts

This project generates cinematic, swipe-length (60-second) videos that bring American history and the Bill of Rights to life using Hugging Face's text-to-video models.

## Prerequisites

1. Python 3.9 or higher
2. Hugging Face API token

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```bash
HUGGINGFACE_API_TOKEN=your_token_here
```

## Usage

The project provides a command-line interface for generating videos from scripts:

```bash
python src/video_generation/cli.py generate --script path/to/script.json
```

Example script format:
```json
{
    "title": "First Amendment",
    "description": "A cinematic exploration of freedom of speech",
    "scenes": [
        {
            "description": "A peaceful protest in Washington DC",
            "duration": 15
        }
    ]
}
```

## Project Structure

```
src/
├── video_generation/
│   ├── generator.py    # Core video generation logic
│   └── cli.py         # Command-line interface
├── scripts/
│   ├── template.py    # Script structure and validation
│   └── samples/       # Example scripts
└── utils/            # Helper functions
```

## Development

1. Create a new script in `src/scripts/samples/`
2. Test generation with the CLI
3. Review output in the `output/` directory

## Troubleshooting

1. If you encounter API errors:
   - Verify your Hugging Face API token
   - Check your internet connection
   - Ensure you have sufficient API credits

2. If video generation fails:
   - Check the input script format
   - Verify model availability
   - Check system resources

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details 