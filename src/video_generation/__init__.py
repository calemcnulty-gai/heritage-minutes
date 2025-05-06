"""
Video generation package for A250 project.
"""

from .generator import VideoGenerator, VideoConfig, generate_video
from .cli import main as cli_main

__all__ = ['VideoGenerator', 'VideoConfig', 'generate_video', 'cli_main'] 