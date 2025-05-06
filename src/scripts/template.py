"""
Script template module for A250 project.
Defines the structure and validation for 60-second video scripts.
"""

from dataclasses import dataclass
from typing import List, Optional
import json
from pathlib import Path

@dataclass
class ScriptSection:
    """A section of the script with timing and content."""
    start_time: float  # in seconds
    end_time: float    # in seconds
    content: str       # text or description
    visual_prompt: str # prompt for video generation
    audio_prompt: Optional[str] = None  # prompt for audio generation

@dataclass
class VideoScript:
    """Complete script for a 60-second video."""
    title: str
    description: str
    sections: List[ScriptSection]
    hashtags: List[str]
    call_to_action: str
    target_audience: str = "13-18"
    duration: float = 60.0  # in seconds
    
    def validate(self) -> bool:
        """Validate the script structure and timing."""
        if not self.sections:
            return False
            
        # Check total duration
        total_duration = max(section.end_time for section in self.sections)
        if total_duration > self.duration:
            return False
            
        # Check for gaps or overlaps
        sorted_sections = sorted(self.sections, key=lambda x: x.start_time)
        for i in range(len(sorted_sections) - 1):
            if sorted_sections[i].end_time > sorted_sections[i + 1].start_time:
                return False
                
        return True
        
    def to_json(self) -> str:
        """Convert script to JSON format."""
        return json.dumps({
            "title": self.title,
            "description": self.description,
            "sections": [
                {
                    "start_time": section.start_time,
                    "end_time": section.end_time,
                    "content": section.content,
                    "visual_prompt": section.visual_prompt,
                    "audio_prompt": section.audio_prompt
                }
                for section in self.sections
            ],
            "hashtags": self.hashtags,
            "call_to_action": self.call_to_action,
            "target_audience": self.target_audience,
            "duration": self.duration
        }, indent=2)
        
    @classmethod
    def from_json(cls, json_str: str) -> 'VideoScript':
        """Create a VideoScript from JSON string."""
        data = json.loads(json_str)
        sections = [
            ScriptSection(
                start_time=section["start_time"],
                end_time=section["end_time"],
                content=section["content"],
                visual_prompt=section["visual_prompt"],
                audio_prompt=section.get("audio_prompt")
            )
            for section in data["sections"]
        ]
        return cls(
            title=data["title"],
            description=data["description"],
            sections=sections,
            hashtags=data["hashtags"],
            call_to_action=data["call_to_action"],
            target_audience=data.get("target_audience", "13-18"),
            duration=data.get("duration", 60.0)
        )

def create_script_template() -> VideoScript:
    """Create a template script structure."""
    return VideoScript(
        title="Template: [Historical Event]",
        description="A 60-second story about [historical event] and its impact on [relevant right/amendment].",
        sections=[
            ScriptSection(
                start_time=0.0,
                end_time=15.0,
                content="Hook: [Engaging opening]",
                visual_prompt="Cinematic shot of [scene description]",
                audio_prompt="Background music: [mood/type]"
            ),
            ScriptSection(
                start_time=15.0,
                end_time=30.0,
                content="Context: [Historical background]",
                visual_prompt="Historical footage or recreation of [event]",
                audio_prompt="Narration: [tone/style]"
            ),
            ScriptSection(
                start_time=30.0,
                end_time=45.0,
                content="Impact: [Why it matters today]",
                visual_prompt="Modern connection to [historical event]",
                audio_prompt="Music shift to [mood]"
            ),
            ScriptSection(
                start_time=45.0,
                end_time=60.0,
                content="Call to Action: [Engagement prompt]",
                visual_prompt="Text overlay with question or challenge",
                audio_prompt="Final music cue"
            )
        ],
        hashtags=["#AmericanHistory", "#BillOfRights", "#Education"],
        call_to_action="What would you do in this situation? Share your thoughts below! 👇"
    )

def save_script(script: VideoScript, path: str):
    """Save a script to a file."""
    with open(path, 'w') as f:
        f.write(script.to_json())

def load_script(path: str) -> VideoScript:
    """Load a script from a file."""
    with open(path, 'r') as f:
        return VideoScript.from_json(f.read()) 