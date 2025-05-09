import os
from pathlib import Path
from video_generation.generator import VideoGenerator, create_historical_prompt

def test_models():
    # Create output directory
    output_dir = Path("output/test_clips")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Test events
    events = [
        "constitutional_convention",
        "bill_of_rights",
        "first_amendment"
    ]
    
    # Use the API-available model
    model_name = "ali-vilab/text-to-video-ms-1.7b"
    print(f"\nTesting model: {model_name}")
    generator = VideoGenerator(model_name=model_name)
    
    for event in events:
        print(f"\nGenerating video for: {event}")
        prompt_info = create_historical_prompt(event)
        
        output_path = output_dir / f"{model_name.split('/')[-1]}_{event}.mp4"
        
        try:
            video_path = generator.generate_video(
                prompt=prompt_info["prompt"],
                output_path=output_path,
                num_frames=32,
                num_inference_steps=50,
                width=1024,
                height=576,
                fps=24
            )
            print(f"Successfully generated video: {video_path}")
        except Exception as e:
            print(f"Error generating video for {event} with {model_name}: {str(e)}")

if __name__ == "__main__":
    test_models() 