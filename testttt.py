import subprocess
import os


def generate_all_improv_variations():
    """Generate a comprehensive set of improv variations"""

    os.makedirs("./all_improv_variations", exist_ok=True)

    # Configuration combinations
    configs = [
        {
            "model": "basic_improv",
            "chords": "C G Am F C G Am F",
            "primer": "[60]",
            "name": "basic_pop"
        },
        {
            "model": "attention_improv",
            "chords": "C G Am F C G Am F",
            "primer": "[60]",
            "name": "attention_pop"
        },
        {
            "model": "chord_pitches_improv",
            "chords": "C G Am F C G Am F",
            "primer": "[60]",
            "name": "chord_pitches_pop"
        },
        {
            "model": "attention_improv",
            "chords": "Am F C G Am F C G",
            "primer": "[69]",  # Start on A
            "name": "minor_melody"
        },
        {
            "model": "attention_improv",
            "chords": "G D Em C G D Em C",
            "primer": "[67]",  # Start on G
            "name": "folk_style"
        }
    ]

    for config in configs:
        print(f"Generating {config['name']}...")

        cmd = [
            "improv_rnn_generate",
            f"--config={config['model']}",
            f"--bundle_file={config['model']}.mag",
            "--output_dir=./all_improv_variations",
            "--num_outputs=2",
            f"--primer_melody={config['primer']}",
            f"--backing_chords={config['chords']}",
            "--render_chords"
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✓ {config['name']} completed")
        except subprocess.CalledProcessError as e:
            print(f"✗ {config['name']} failed: {e.stderr}")


generate_all_improv_variations()

print("\n🎵 Generated complete set of improv variations!")
print("The --render_chords flag means you'll hear both the melody AND the backing chords!")