"""
SageMaker-based video generation module for historical moments.
Handles the generation of 10-second portrait videos using the LTX-Video model.
"""

import os
import json
import boto3
import logging
from pathlib import Path
from typing import Optional, Dict, Union
import cv2
import numpy as np
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SageMakerVideoGenerator:
    """Main class for generating history videos using SageMaker endpoint."""
    
    def __init__(self, endpoint_name: str = "ltx-video-realtime-endpoint"):
        """
        Initialize the video generator with SageMaker endpoint.
        
        Args:
            endpoint_name: Name of the SageMaker endpoint
        """
        self.endpoint_name = endpoint_name
        self.sagemaker_runtime = boto3.client('sagemaker-runtime')
        
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
        num_frames: int = 24,  # For 10 seconds at 24fps
        num_inference_steps: int = 50,
        width: int = 576,  # Portrait mode
        height: int = 1024,  # Portrait mode
        fps: int = 24,
        seed: Optional[int] = None
    ) -> str:
        """
        Generate a video from a text prompt using SageMaker endpoint.
        
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
            
            # Prepare the request payload
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
            
            # Make the SageMaker endpoint request
            response = self.sagemaker_runtime.invoke_endpoint(
                EndpointName=self.endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            # Parse the response
            response_body = json.loads(response['Body'].read().decode())
            video_frames = response_body.get("frames", [])
            
            if not video_frames:
                raise Exception("No frames received from endpoint")
            
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
        "declaration_of_independence": {
            "description": "The signing of the Declaration of Independence",
            "prompt": "A grand hall in Philadelphia, 1776. Thomas Jefferson and other founding fathers gather around a wooden table, signing the Declaration of Independence. Sunlight streams through tall windows, illuminating the historic moment. Men in colonial attire with powdered wigs stand with quills in hand. The atmosphere is charged with revolutionary spirit. The scene is captured in portrait mode with dramatic lighting and careful attention to historical detail."
        },
        "suffrage_movement": {
            "description": "Women's suffrage movement march",
            "prompt": "A powerful march for women's suffrage in the early 1900s. Women in period clothing carry banners and signs demanding voting rights. The scene is filled with determination and hope. The camera captures the movement in portrait mode, emphasizing the strength and unity of the marchers. Historical buildings line the street, and the atmosphere is charged with the energy of social change."
        },
        "civil_rights_march": {
            "description": "Martin Luther King Jr. leading the March on Washington",
            "prompt": "The historic March on Washington, 1963. Martin Luther King Jr. stands at the Lincoln Memorial, addressing a vast crowd. The scene captures the iconic moment with the Washington Monument in the background. The atmosphere is one of hope and determination. The camera moves smoothly in portrait mode, capturing the emotion and scale of this pivotal moment in civil rights history."
        }
    }
    
    return prompts.get(event, {
        "description": "Custom historical event",
        "prompt": f"A cinematic recreation of {event} in portrait mode. The scene is captured with dramatic lighting and careful attention to historical detail, creating an immersive and authentic representation of the period."
    })

def main():
    """Generate three historical videos using the SageMaker endpoint."""
    generator = SageMakerVideoGenerator()
    output_dir = Path("output/videos")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate videos for three historical moments
    events = ["declaration_of_independence", "suffrage_movement", "civil_rights_march"]
    
    for event in events:
        prompt_info = create_historical_prompt(event)
        output_path = output_dir / f"{event}.mp4"
        
        logger.info(f"Generating video for: {prompt_info['description']}")
        generator.generate_video(
            prompt=prompt_info["prompt"],
            output_path=output_path,
            num_frames=240,  # 10 seconds at 24fps
            width=576,  # Portrait mode
            height=1024,  # Portrait mode
            fps=24
        )

if __name__ == "__main__":
    main() 