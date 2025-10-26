"""
Recording Protocol for Parkinson's Voice Analysis
Standardized tasks to ensure consistent measurements
"""

from datetime import datetime
from pathlib import Path

class RecordingSession:
    """Manages a recording session with standardized tasks"""
    
    def __init__(self, participant_id, session_type="baseline"):
        """
        Initialize recording session
        Args:
            participant_id: Identifier (e.g., "uncle", "patient_001")
            session_type: "baseline", "week_1", "week_2", etc.
        """
        self.participant_id = participant_id
        self.session_type = session_type
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.tasks = self.get_tasks()
        
    def get_tasks(self):
        """Define standardized recording tasks"""
        return {
            "task_1_sustained_vowel": {
                "name": "Sustained Vowel (AAAAH)",
                "instruction_english": "Say AAAAH as loudly and steadily as you can for 5 seconds",
                "instruction_urdu": "جتنی زور سے ہو سکے AAAAH کہیں، 5 سیکنڈ تک",
                "duration": "5 seconds",
                "purpose": "Measure pitch stability, loudness, jitter, shimmer",
                "filename": f"{self.participant_id}_{self.session_type}_vowel_{self.timestamp}.wav"
            },
            
            "task_2_pitch_glide": {
                "name": "Pitch Glide",
                "instruction_english": "Say AAAAH starting from your lowest pitch, sliding up to your highest pitch",
                "instruction_urdu": "AAAAH کہیں، سب سے نیچی آواز سے شروع کر کے سب سے اونچی آواز تک",
                "duration": "3-5 seconds",
                "purpose": "Measure pitch range capability",
                "filename": f"{self.participant_id}_{self.session_type}_glide_{self.timestamp}.wav"
            },
            
            "task_3_counting": {
                "name": "Counting in Urdu",
                "instruction_english": "Count from 1 to 20 in Urdu, speaking clearly and loudly",
                "instruction_urdu": "1 سے 20 تک گنتی کریں، صاف اور زور سے",
                "duration": "15-20 seconds",
                "purpose": "Measure connected speech, articulation, consistency",
                "filename": f"{self.participant_id}_{self.session_type}_counting_{self.timestamp}.wav"
            },
            
            "task_4_sentences": {
                "name": "Standard Sentences",
                "instruction_english": "Read these sentences loudly and clearly:",
                "instruction_urdu": "یہ جملے زور سے اور صاف پڑھیں:",
                "sentences": [
                    "آج موسم بہت اچھا ہے",  # The weather is very nice today
                    "میں صبح کی نماز پڑھتا ہوں",  # I pray the morning prayer
                    "میرے بچے سکول جاتے ہیں"  # My children go to school
                ],
                "duration": "10-15 seconds",
                "purpose": "Measure real-world speech clarity",
                "filename": f"{self.participant_id}_{self.session_type}_sentences_{self.timestamp}.wav"
            },
            
            "task_5_spontaneous": {
                "name": "Spontaneous Speech",
                "instruction_english": "Tell me about what you had for breakfast today",
                "instruction_urdu": "مجھے بتائیں آج ناشتے میں کیا کھایا",
                "duration": "30 seconds",
                "purpose": "Measure natural conversation clarity",
                "filename": f"{self.participant_id}_{self.session_type}_spontaneous_{self.timestamp}.wav"
            }
        }
    
    def print_instructions(self):
        """Print recording instructions for the session"""
        print("\n" + "="*60)
        print(f"RECORDING SESSION: {self.session_type.upper()}")
        print(f"Participant: {self.participant_id}")
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("="*60)
        
        print("\n📋 SETUP CHECKLIST:")
        print("□ Quiet room (no TV, fan, or background noise)")
        print("□ Phone/recorder ready")
        print("□ Microphone 6-8 inches from mouth")
        print("□ Participant is comfortable and relaxed")
        print("□ Recording format: WAV (preferred) or MP3")
        print("□ Sample rate: 44100 Hz or higher")
        
        print("\n🎙️ RECORDING TASKS:")
        print("Complete all tasks in order. Take short breaks if needed.\n")
        
        for i, (task_id, task) in enumerate(self.tasks.items(), 1):
            print(f"\n--- TASK {i}: {task['name']} ---")
            print(f"English: {task['instruction_english']}")
            print(f"Urdu: {task['instruction_urdu']}")
            if 'sentences' in task:
                print("Sentences:")
                for j, sentence in enumerate(task['sentences'], 1):
                    print(f"  {j}. {sentence}")
            print(f"Expected duration: {task['duration']}")
            print(f"Save as: {task['filename']}")
            print(f"Purpose: {task['purpose']}")
            print("-" * 60)
        
        print("\n✅ AFTER RECORDING:")
        print("□ Check all files are saved correctly")
        print("□ Files are in WAV format (or convert from MP3)")
        print(f"□ Move files to: data/{self.session_type}/")
        print("□ Run analysis script")
        print("\n" + "="*60 + "\n")
    
    def save_session_log(self, output_dir="data"):
        """Save session information to file"""
        output_path = Path(output_dir) / self.session_type / f"session_log_{self.timestamp}.txt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Recording Session Log\n")
            f.write(f"{'='*60}\n")
            f.write(f"Participant: {self.participant_id}\n")
            f.write(f"Session Type: {self.session_type}\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"{'='*60}\n\n")
            
            f.write("Tasks Completed:\n\n")
            for i, (task_id, task) in enumerate(self.tasks.items(), 1):
                f.write(f"{i}. {task['name']}\n")
                f.write(f"   Filename: {task['filename']}\n")
                f.write(f"   Purpose: {task['purpose']}\n\n")
        
        print(f"Session log saved to: {output_path}")
        return output_path


def start_baseline_session(participant_id="uncle"):
    """Quick start for baseline recording"""
    session = RecordingSession(participant_id, "baseline")
    session.print_instructions()
    session.save_session_log()
    return session


def start_followup_session(participant_id="uncle", week_number=1):
    """Quick start for follow-up recording"""
    session = RecordingSession(participant_id, f"week_{week_number}")
    session.print_instructions()
    session.save_session_log()
    return session


if __name__ == "__main__":
    print("\n🎙️ Parkinson's Voice Recording Protocol\n")
    print("Choose session type:")
    print("1. Baseline (first recording)")
    print("2. Follow-up (after exercises)")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        start_baseline_session()
    elif choice == "2":
        week = input("Enter week number (e.g., 1, 2, 4, 8): ").strip()
        start_followup_session(week_number=week)
    else:
        print("Invalid choice. Run script again.")