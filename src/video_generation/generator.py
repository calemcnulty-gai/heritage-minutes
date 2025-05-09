"""
Core video generation module for A250 project.
Handles the generation of 60-second history videos using Hugging Face models.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Union
import requests
import json
import logging
import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoGenerator:
    """Main class for generating history videos."""
    
    def __init__(self, model_name: str = "Lightricks/LTX-Video"):
        """
        Initialize the video generator with a specific model.
        
        Args:
            model_name: Name of the Hugging Face model to use
        """
        self.model_name = model_name
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if not self.api_token:
            raise ValueError("HUGGINGFACE_API_TOKEN not found in environment variables")
        
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        
    def _save_video_with_cv2(self, frames, output_path: str, fps: int = 24):
        """Save video frames using OpenCV with high quality settings."""
        if not frames:
            raise ValueError("No frames to save")
            
        # Convert frames to numpy arrays if they aren't already
        frames = [np.array(frame) for frame in frames]
        
        # Get video dimensions from first frame
        height, width = frames[0].shape[:2]
        
        # Create video writer with high quality settings
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (width, height),
            True
        )
        
        # Write frames
        for frame in frames:
            out.write(frame)
            
        out.release()
        logger.info(f"Video saved with OpenCV at: {output_path}")

    def generate_video(
        self,
        prompt: str,
        output_path: Union[str, Path],
        negative_prompt: Optional[str] = None,
        num_frames: int = 32,
        num_inference_steps: int = 50,
        width: int = 1024,
        height: int = 576,
        fps: int = 24,
        seed: Optional[int] = None
    ) -> str:
        """
        Generate a video from a text prompt using Hugging Face API.
        
        Args:
            prompt: Text description of the video to generate
            output_path: Path to save the generated video
            negative_prompt: Text description of what to avoid in the video
            num_frames: Number of frames to generate
            num_inference_steps: Number of denoising steps
            width: Video width
            height: Video height
            fps: Frames per second
            seed: Random seed for reproducibility
            
        Returns:
            Path to the generated video
        """
        try:
            # Default negative prompt if none provided
            if negative_prompt is None:
                negative_prompt = "worst quality, inconsistent motion, blurry, jittery, distorted"
            
            # Prepare the API request payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "negative_prompt": negative_prompt,
                    "num_frames": num_frames,
                    "num_inference_steps": num_inference_steps,
                    "width": width,
                    "height": height,
                    "seed": seed
                }
            }
            
            # Make the API request
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed with status {response.status_code}: {response.text}")
            
            # Get the video frames from the response
            video_frames = response.json().get("frames", [])
            if not video_frames:
                raise Exception("No frames received from API")
            
            # Export video using OpenCV for better quality
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_video_with_cv2(video_frames, str(output_path), fps=fps)
            
            logger.info(f"Successfully generated video at: {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"Error generating video: {str(e)}")
            raise

def create_historical_prompt(event: str, style: str = "cinematic") -> Dict[str, str]:
    """
    Create a detailed prompt for historical video generation.
    
    Args:
        event: Historical event to depict
        style: Visual style of the video
        
    Returns:
        Dictionary containing description and prompt
    """
    prompts = {
        "constitutional_convention": {
            "description": "The Constitutional Convention of 1787 in Philadelphia",
            "prompt": "A grand assembly hall in Philadelphia, 1787. Distinguished delegates in period clothing engage in passionate debate. Sunlight streams through tall windows, illuminating the ornate wooden architecture. Men in powdered wigs and colonial attire stand and gesture emphatically. The atmosphere is charged with the weight of history being made. The scene is captured in a cinematic style with dramatic lighting and careful attention to historical detail."
        },
        "bill_of_rights": {
            "description": "The drafting of the Bill of Rights",
            "prompt": "An intimate study in the late 18th century. James Madison sits at a wooden desk, quill in hand, surrounded by candlelight. Parchment papers and historical documents are spread before him. The room is filled with the warm glow of candlelight, casting long shadows. The scene is captured in a cinematic style with careful attention to period details and atmospheric lighting."
        },
        "first_amendment": {
            "description": "A peaceful protest demonstrating freedom of speech",
            "prompt": "A diverse crowd of peaceful protesters in Washington DC. People of all ages and backgrounds hold signs advocating for civil rights. The scene is captured in golden hour sunlight, with the Washington Monument visible in the background. The atmosphere is one of peaceful determination and unity. The camera moves smoothly through the crowd, capturing the emotion and purpose of the demonstration."
        }
    }
    
    return prompts.get(event, {
        "description": "Custom historical event",
        "prompt": f"A cinematic recreation of {event}. The scene is captured with dramatic lighting and careful attention to historical detail, creating an immersive and authentic representation of the period."
    }) 