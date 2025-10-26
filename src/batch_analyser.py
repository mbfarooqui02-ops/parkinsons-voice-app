"""
Batch Analyzer - Process multiple audio files at once
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add src to path so we can import voice_analyzer
sys.path.append(str(Path(__file__).parent))
from voice_analyzer import VoiceAnalyzer


def analyze_folder(folder_path, output_csv="analysis_results.csv"):
    """
    Analyze all WAV files in a folder
    
    Args:
        folder_path: Path to folder containing WAV files
        output_csv: Where to save results
    """
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Error: Folder not found: {folder_path}")
        return None
    
    # Find all WAV files
    audio_files = list(folder.glob("*.wav")) + list(folder.glob("*.mp3"))
    
    if not audio_files:
        print(f"❌ No audio files found in {folder_path}")
        print("Supported formats: .wav, .mp3")
        return None
    
    print(f"\n📁 Found {len(audio_files)} audio files in {folder_path}")
    print("="*60)
    
    all_results = []
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] Analyzing: {audio_file.name}")
        print("-"*60)
        
        try:
            analyzer = VoiceAnalyzer(str(audio_file))
            features = analyzer.extract_all_features()
            
            # Generate report
            analyzer.generate_report(output_dir=folder / "reports")
            
            # Add to results
            all_results.append(features)
            
            # Print key metrics
            print(f"✓ Intensity: {features['intensity']} dB")
            print(f"✓ Pitch Mean: {features['pitch_mean']} Hz")
            print(f"✓ Pitch Range: {features['pitch_range']} Hz")
            print(f"✓ Jitter: {features['jitter']}%")
            print(f"✓ Shimmer: {features['shimmer']}%")
            print(f"✓ HNR: {features['hnr']} dB")
            
        except Exception as e:
            print(f"❌ Error analyzing {audio_file.name}: {str(e)}")
            continue
    
    if not all_results:
        print("\n❌ No files were successfully analyzed")
        return None
    
    # Save all results to CSV
    df = pd.DataFrame(all_results)
    output_path = folder / output_csv
    df.to_csv(output_path, index=False)
    
    print("\n" + "="*60)
    print(f"✅ Analysis complete!")
    print(f"📊 Results saved to: {output_path}")
    print(f"📈 Reports saved to: {folder / 'reports'}/")
    print("="*60 + "\n")
    
    return df


def compare_sessions(baseline_folder, followup_folder):
    """
    Compare baseline recordings with follow-up recordings
    """
    print("\n🔍 COMPARING BASELINE vs FOLLOW-UP")
    print("="*60)
    
    # Analyze both folders
    print("\n📊 Analyzing baseline recordings...")
    baseline_df = analyze_folder(baseline_folder, "baseline_results.csv")
    
    print("\n📊 Analyzing follow-up recordings...")
    followup_df = analyze_folder(followup_folder, "followup_results.csv")
    
    if baseline_df is None or followup_df is None:
        print("❌ Could not complete comparison")
        return
    
    # Calculate averages
    print("\n" + "="*60)
    print("📈 AVERAGE CHANGES")
    print("="*60)
    
    metrics = ['intensity', 'pitch_mean', 'pitch_range', 'jitter', 'shimmer', 'hnr']
    
    comparison_data = []
    
    for metric in metrics:
        baseline_avg = baseline_df[metric].mean()
        followup_avg = followup_df[metric].mean()
        change = followup_avg - baseline_avg
        percent_change = (change / baseline_avg * 100) if baseline_avg != 0 else 0
        
        comparison_data.append({
            'metric': metric,
            'baseline': baseline_avg,
            'followup': followup_avg,
            'change': change,
            'percent_change': percent_change
        })
        
        direction = "↑" if change > 0 else "↓"
        print(f"{metric:20s}: {baseline_avg:6.2f} → {followup_avg:6.2f} "
              f"({direction} {abs(change):6.2f}, {percent_change:+.1f}%)")
    
    # Save comparison
    comparison_df = pd.DataFrame(comparison_data)
    output_path = Path(baseline_folder).parent / "comparison_results.csv"
    comparison_df.to_csv(output_path, index=False)
    print(f"\n💾 Comparison saved to: {output_path}")
    
    # Interpretation
    print("\n" + "="*60)
    print("💡 INTERPRETATION")
    print("="*60)
    
    intensity_change = comparison_df[comparison_df['metric'] == 'intensity']['change'].values[0]
    pitch_range_change = comparison_df[comparison_df['metric'] == 'pitch_range']['change'].values[0]
    hnr_change = comparison_df[comparison_df['metric'] == 'hnr']['change'].values[0]
    jitter_change = comparison_df[comparison_df['metric'] == 'jitter']['change'].values[0]
    
    improvements = 0
    
    if intensity_change > 2:
        print("✅ LOUDNESS: Significant improvement (+{:.1f} dB)".format(intensity_change))
        print("   → Voice is noticeably louder - excellent progress!")
        improvements += 1
    elif intensity_change > 0:
        print("🟡 LOUDNESS: Slight improvement (+{:.1f} dB)".format(intensity_change))
        print("   → Some progress, keep practicing")
    else:
        print("❌ LOUDNESS: No improvement ({:.1f} dB)".format(intensity_change))
        print("   → Need to focus on speaking LOUDER")
    
    if pitch_range_change > 10:
        print("\n✅ PITCH VARIATION: Much less monotone (+{:.1f} Hz range)".format(pitch_range_change))
        print("   → Speech sounds more natural and expressive")
        improvements += 1
    elif pitch_range_change > 0:
        print("\n🟡 PITCH VARIATION: Slightly less monotone (+{:.1f} Hz range)".format(pitch_range_change))
    else:
        print("\n❌ PITCH VARIATION: Still monotone ({:.1f} Hz)".format(pitch_range_change))
        print("   → Need pitch glide exercises")
    
    if hnr_change > 2:
        print("\n✅ CLARITY: Voice is much clearer (+{:.1f} dB HNR)".format(hnr_change))
        print("   → Less breathiness, better voice quality")
        improvements += 1
    elif hnr_change > 0:
        print("\n🟡 CLARITY: Slightly clearer (+{:.1f} dB HNR)".format(hnr_change))
    else:
        print("\n❌ CLARITY: No improvement in clarity ({:.1f} dB HNR)".format(hnr_change))
    
    if jitter_change < -0.2:
        print("\n✅ STABILITY: Voice is more stable ({:.2f}% jitter reduction)".format(abs(jitter_change)))
        improvements += 1
    
    print("\n" + "="*60)
    print(f"OVERALL: {improvements}/4 areas showing significant improvement")
    
    if improvements >= 3:
        print("🎉 EXCELLENT PROGRESS! Exercises are working well.")
    elif improvements >= 2:
        print("👍 GOOD PROGRESS! Keep up the practice.")
    elif improvements >= 1:
        print("📈 SOME PROGRESS. Stay consistent with exercises.")
    else:
        print("⚠️  Limited progress. Consider:")
        print("   - Increasing practice frequency")
        print("   - Focusing on LOUDNESS specifically")
        print("   - Consulting with speech therapist")
    
    print("="*60 + "\n")
    
    return comparison_df


if __name__ == "__main__":
    print("\n🎙️ Batch Voice Analyzer")
    print("="*60)
    
    print("\nOptions:")
    print("1. Analyze all files in a folder")
    print("2. Compare baseline vs follow-up sessions")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        folder = input("Enter folder path (e.g., data/baseline): ").strip()
        analyze_folder(folder)
        
    elif choice == "2":
        baseline = input("Enter baseline folder path: ").strip()
        followup = input("Enter follow-up folder path: ").strip()
        compare_sessions(baseline, followup)
        
    else:
        print("Invalid choice")