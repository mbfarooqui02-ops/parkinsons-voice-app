"""
Parkinson's Voice Feature Extraction Tool
Extracts key acoustic features for tracking speech clarity over time
"""

import librosa
import parselmouth
from parselmouth.praat import call
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

class VoiceAnalyzer:
    def __init__(self, audio_file):
        """
        Initialize analyzer with audio file
        Args:
            audio_file: path to WAV file
        """
        self.audio_file = audio_file
        self.y, self.sr = librosa.load(audio_file, sr=None)
        self.sound = parselmouth.Sound(audio_file)
        self.features = {}
        
    def extract_all_features(self):
        """Extract all relevant features"""
        print(f"Analyzing: {self.audio_file}")
        
        # Basic features (easy)
        self.features['intensity'] = self.get_intensity()
        self.features['pitch_mean'] = self.get_pitch_statistics()['mean']
        self.features['pitch_std'] = self.get_pitch_statistics()['std']
        self.features['pitch_min'] = self.get_pitch_statistics()['min']
        self.features['pitch_max'] = self.get_pitch_statistics()['max']
        self.features['pitch_range'] = self.get_pitch_statistics()['range']
        
        # Advanced features (harder but important)
        self.features['jitter'] = self.get_jitter()
        self.features['shimmer'] = self.get_shimmer()
        self.features['hnr'] = self.get_hnr()
        
        # Duration
        self.features['duration'] = len(self.y) / self.sr
        
        # Add metadata
        self.features['timestamp'] = datetime.now().isoformat()
        self.features['file'] = str(self.audio_file)
        
        return self.features
    
    def get_intensity(self):
        """
        Calculate average intensity (loudness) in dB
        Priority 1 feature - most important for PD
        """
        intensity = self.sound.to_intensity()
        mean_intensity = call(intensity, "Get mean", 0, 0, "energy")
        return round(mean_intensity, 2)
    
    def get_pitch_statistics(self):
        """
        Extract pitch (F0) statistics
        Priority 2 feature - shows monotone/pitch problems
        """
        pitch = self.sound.to_pitch()
        
        # Get pitch values (only voiced regions)
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values > 0]  # Remove unvoiced
        
        if len(pitch_values) == 0:
            return {
                'mean': 0,
                'std': 0,
                'min': 0,
                'max': 0,
                'range': 0
            }
        
        return {
            'mean': round(np.mean(pitch_values), 2),
            'std': round(np.std(pitch_values), 2),
            'min': round(np.min(pitch_values), 2),
            'max': round(np.max(pitch_values), 2),
            'range': round(np.max(pitch_values) - np.min(pitch_values), 2)
        }
    
    def get_jitter(self):
        """
        Calculate local jitter (pitch stability)
        Higher = more vocal instability (common in PD)
        Normal: < 1.04%
        """
        point_process = call(self.sound, "To PointProcess (periodic, cc)", 75, 500)
        jitter = call(point_process, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        return round(jitter * 100, 3)  # Convert to percentage
    
    def get_shimmer(self):
        """
        Calculate local shimmer (amplitude stability)
        Higher = more breathiness/hoarseness (common in PD)
        Normal: < 3.5%
        """
        point_process = call(self.sound, "To PointProcess (periodic, cc)", 75, 500)
        shimmer = call(point_process, "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        return round(shimmer * 100, 3)  # Convert to percentage
    
    def get_hnr(self):
        """
        Calculate Harmonics-to-Noise Ratio
        Lower = more breathiness, less clarity (common in PD)
        Normal: > 20 dB
        """
        harmonicity = call(self.sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        hnr = call(harmonicity, "Get mean", 0, 0)
        return round(hnr, 2)
    
    def generate_report(self, output_dir='reports'):
        """Generate visual report of features"""
        Path(output_dir).mkdir(exist_ok=True)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'Voice Analysis Report\n{Path(self.audio_file).name}', 
                     fontsize=16, fontweight='bold')
        
        # 1. Waveform
        axes[0, 0].plot(np.linspace(0, self.features['duration'], len(self.y)), self.y)
        axes[0, 0].set_title('Waveform')
        axes[0, 0].set_xlabel('Time (s)')
        axes[0, 0].set_ylabel('Amplitude')
        
        # 2. Pitch contour
        pitch = self.sound.to_pitch()
        pitch_values = pitch.selected_array['frequency']
        pitch_times = pitch.xs()
        axes[0, 1].plot(pitch_times, pitch_values)
        axes[0, 1].set_title(f'Pitch Contour (Mean: {self.features["pitch_mean"]} Hz)')
        axes[0, 1].set_xlabel('Time (s)')
        axes[0, 1].set_ylabel('Frequency (Hz)')
        axes[0, 1].set_ylim([0, 500])
        
        # 3. Intensity contour
        intensity = self.sound.to_intensity()
        intensity_values = intensity.values[0]
        intensity_times = intensity.xs()
        axes[1, 0].plot(intensity_times, intensity_values)
        axes[1, 0].set_title(f'Intensity (Mean: {self.features["intensity"]} dB)')
        axes[1, 0].set_xlabel('Time (s)')
        axes[1, 0].set_ylabel('Intensity (dB)')
        
        # 4. Feature summary
        axes[1, 1].axis('off')
        summary_text = f"""
        KEY FEATURES:
        
        Intensity: {self.features['intensity']} dB
        (Normal: 60-70 dB)
        
        Pitch Mean: {self.features['pitch_mean']} Hz
        Pitch Range: {self.features['pitch_range']} Hz
        (Normal range: 100-200 Hz variation)
        
        Jitter: {self.features['jitter']}%
        (Normal: < 1.04%)
        
        Shimmer: {self.features['shimmer']}%
        (Normal: < 3.5%)
        
        HNR: {self.features['hnr']} dB
        (Normal: > 20 dB)
        
        Duration: {self.features['duration']:.2f} seconds
        """
        axes[1, 1].text(0.1, 0.5, summary_text, fontsize=11, 
                       verticalalignment='center', family='monospace')
        
        plt.tight_layout()
        
        # Save report
        report_path = Path(output_dir) / f"{Path(self.audio_file).stem}_report.png"
        plt.savefig(report_path, dpi=150, bbox_inches='tight')
        print(f"Report saved: {report_path}")
        
        return report_path
    
    def save_features(self, output_file='voice_features.csv'):
        """Save features to CSV for tracking over time"""
        df = pd.DataFrame([self.features])
        
        # Append to existing file or create new
        if Path(output_file).exists():
            existing = pd.read_csv(output_file)
            df = pd.concat([existing, df], ignore_index=True)
        
        df.to_csv(output_file, index=False)
        print(f"Features saved to: {output_file}")
        
        return output_file


def analyze_audio_file(audio_path):
    """
    Main function to analyze a single audio file
    """
    analyzer = VoiceAnalyzer(audio_path)
    features = analyzer.extract_all_features()
    
    # Print results
    print("\n" + "="*50)
    print("VOICE ANALYSIS RESULTS")
    print("="*50)
    for key, value in features.items():
        if key not in ['timestamp', 'file']:
            print(f"{key:20s}: {value}")
    print("="*50 + "\n")
    
    # Generate visual report
    analyzer.generate_report()
    
    # Save to CSV for tracking
    analyzer.save_features()
    
    return features


def compare_recordings(baseline_file, followup_file):
    """
    Compare two recordings to see improvement
    """
    print("Analyzing baseline recording...")
    baseline = VoiceAnalyzer(baseline_file)
    baseline_features = baseline.extract_all_features()
    
    print("Analyzing follow-up recording...")
    followup = VoiceAnalyzer(followup_file)
    followup_features = followup.extract_all_features()
    
    # Calculate changes
    print("\n" + "="*50)
    print("COMPARISON: BASELINE vs FOLLOW-UP")
    print("="*50)
    
    key_metrics = ['intensity', 'pitch_mean', 'pitch_range', 'jitter', 'shimmer', 'hnr']
    
    for metric in key_metrics:
        baseline_val = baseline_features[metric]
        followup_val = followup_features[metric]
        change = followup_val - baseline_val
        percent_change = (change / baseline_val * 100) if baseline_val != 0 else 0
        
        direction = "↑" if change > 0 else "↓"
        print(f"{metric:20s}: {baseline_val:6.2f} → {followup_val:6.2f} "
              f"({direction} {abs(change):6.2f}, {percent_change:+.1f}%)")
    
    print("="*50 + "\n")
    
    # Interpretation
    print("INTERPRETATION:")
    if followup_features['intensity'] > baseline_features['intensity']:
        print("✓ Voice is LOUDER - Good improvement!")
    else:
        print("✗ Voice is quieter - Need more practice")
        
    if followup_features['pitch_range'] > baseline_features['pitch_range']:
        print("✓ More pitch variation - Less monotone!")
    else:
        print("✗ Still monotone - Need pitch exercises")
        
    if followup_features['jitter'] < baseline_features['jitter']:
        print("✓ More stable voice - Better control!")
    else:
        print("✗ Voice still shaky")
        
    if followup_features['hnr'] > baseline_features['hnr']:
        print("✓ Clearer voice - Less breathiness!")
    else:
        print("✗ Voice still breathy")


# Example usage
if __name__ == "__main__":
    print("Parkinson's Voice Feature Extraction Tool")
    print("="*50)
    print("\nUsage:")
    print("1. Place your audio file (WAV format) in the same folder")
    print("2. Update the filename below")
    print("3. Run this script")
    print("\n" + "="*50 + "\n")
    
    # Single file analysis
    # analyze_audio_file("uncle_voice_baseline.wav")
    
    # Compare two recordings
    # compare_recordings("baseline.wav", "week4_followup.wav")
    
    print("\nUncomment the lines above and add your audio file path")
