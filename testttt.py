import subprocess
import os


def generate_chord_pitches_variations():
    """Generate multiple variations using only chord_pitches_improv"""

    os.makedirs("./chord_pitches_variations", exist_ok=True)

    # Different chord progressions to try
    progressions = [
        ("pop_classic", "C G Am F C G Am F"),
        ("folk_style", "G D Em C G D Em C"),
        ("minor_sad", "Am F C G Am F C G"),
        ("blues_feel", "C7 F7 C7 G7 C7 F7 C7 G7"),
        ("jazz_simple", "Cmaj7 Am7 Dm7 G7 Cmaj7 Am7 Dm7 G7"),
        ("rock_power", "C F G C C F G C"),
        ("emotional", "Am C F G Am C F G")
    ]

    # Different starting patterns
    primers = [
        ("single_c", "[60]"),
        ("high_start", "[72]"),
        ("low_start", "[48]"),
        ("chord_c", "[60, 64, 67]"),
        ("scale_up", "[60, 62, 64, 65, 67]"),
        ("scale_down", "[67, 65, 64, 62, 60]"),
        ("jump_pattern", "[60, 67, 64, 69, 65]")
    ]

    count = 0

    for prog_name, chords in progressions:
        for primer_name, primer in primers:

            output_name = f"{prog_name}_{primer_name}"
            count += 1

            print(f"🎵 ({count}) Generating {output_name}...")

            cmd = [
                "improv_rnn_generate",
                "--config=pretrainedModels/chord_pitches_improv.mag",
                "--bundle_file=pretrainedModels/chord_pitches_improv.mag",
                "--output_dir=./chord_pitches_variations",
                "--num_outputs=1",
                f"--primer_melody={primer}",
                f"--backing_chords={chords}",
                "--render_chords"
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"   ✅ {output_name} completed")
            except Exception as e:
                print(f"   ❌ {output_name} failed")


generate_chord_pitches_variations()
print(f"\n🎉 Generated variations using chord_pitches_improv model!")
print("Check the chord_pitches_variations folder for all your melodies!")