"""
Command-line interface for A250 video generation.
"""

import argparse
import sys
from pathlib import Path

from .generator import VideoGenerator, VideoConfig
from ..scripts.template import VideoScript, load_script, save_script

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate A250 history videos")
    
    parser.add_argument(
        "script_path",
        type=str,
        help="Path to the script file (JSON format)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output.mp4",
        help="Output video path (default: output.mp4)"
    )
    
    parser.add_argument(
        "--width",
        type=int,
        default=1080,
        help="Video width (default: 1080)"
    )
    
    parser.add_argument(
        "--height",
        type=int,
        default=1920,
        help="Video height (default: 1920)"
    )
    
    parser.add_argument(
        "--fps",
        type=int,
        default=30,
        help="Frames per second (default: 30)"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="damo-vilab/text-to-video-ms-1.7b",
        help="Hugging Face model to use"
    )
    
    return parser.parse_args()

def main():
    """Main entry point for video generation."""
    args = parse_args()
    
    try:
        # Load and validate script
        script = load_script(args.script_path)
        if not script.validate():
            print("Error: Invalid script structure", file=sys.stderr)
            sys.exit(1)
            
        # Configure video generator
        config = VideoConfig(
            width=args.width,
            height=args.height,
            fps=args.fps,
            model_name=args.model
        )
        
        # Generate video
        generator = VideoGenerator(config)
        try:
            video_path = generator.generate_from_script(
                script.to_json(),
                args.output
            )
            print(f"Video generated successfully: {video_path}")
        finally:
            generator.cleanup()
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 