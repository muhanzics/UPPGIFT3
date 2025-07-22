# Complete Mario-Style Music Generation Test
# This should generate much better results since the AI was trained on video game music!

import note_seq
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
import os


def generate_mario_style_music():
    """
    Generate Mario-style music using patterns the AI knows well.
    """

    print("=" * 60)
    print("MARIO-STYLE MUSIC GENERATOR")
    print("Using patterns the AI was trained on!")
    print("=" * 60)

    # Mario-style melody pattern (high notes, bouncy, 8-bit feel)
    mario_pattern = [72, 72, 72, 68, 72, 76, 64]  # Classic gaming melody

    # Alternative Mario patterns you can try
    mario_patterns = {
        "main_theme": [72, 72, 72, 68, 72, 76, 64],  # Main Mario theme style
        "underground": [60, 62, 60, 62, 60, 59, 60],  # Underground theme style
        "overworld": [76, 72, 76, 72, 74, 71, 69],  # Overworld bouncy style
        "power_up": [64, 67, 71, 74, 67, 74, 79]  # Power-up ascending style
    }

    print("Available Mario patterns:")
    for name, pattern in mario_patterns.items():
        print(f"  {name}: {pattern}")

    # Choose which pattern to use
    chosen_pattern = "main_theme"  # Change this to try different patterns
    mario_notes = mario_patterns[chosen_pattern]

    print(f"\nUsing pattern: {chosen_pattern}")
    print(f"Notes: {mario_notes}")

    try:
        # Load the model
        print("\nLoading AI model...")
        bundle = sequence_generator_bundle.read_bundle_file("basic_rnn.mag")

        # Get the generator
        generator_map = melody_rnn_sequence_generator.get_generator_map()
        generator = generator_map['basic_rnn'](bundle=bundle)
        generator.initialize()
        print("✓ Model loaded successfully!")

        # Create primer sequence with Mario timing
        print("Creating Mario-style primer sequence...")
        primer_sequence = note_seq.NoteSequence()
        primer_sequence.tempos.add(time=0, qpm=140)  # Faster tempo for gaming feel

        # Add Mario notes with bouncy timing
        for i, pitch in enumerate(mario_notes):
            start_time = i * 0.3  # Faster, bouncier timing
            end_time = start_time + 0.25  # Shorter, punchier notes

            primer_sequence.notes.add(
                pitch=pitch,
                start_time=start_time,
                end_time=end_time,
                velocity=90,  # Loud and punchy like 8-bit
                instrument=0
            )

        # Quantize for the AI
        primer_sequence = note_seq.quantize_note_sequence(primer_sequence, steps_per_quarter=4)
        print(f"✓ Mario primer created with {len(mario_notes)} notes")

        # Create output directory
        output_dir = "mario_generated"
        os.makedirs(output_dir, exist_ok=True)

        # Generate multiple Mario variations
        print(f"\nGenerating Mario-style music...")

        for i in range(3):  # Generate 3 variations
            print(f"  Generating Mario variation {i + 1}/3...")

            # Create generator options
            generator_options = generator_pb2.GeneratorOptions()
            generator_options.args['temperature'].float_value = 0.8  # Slightly conservative for gaming feel

            # Generate 32 more steps (about 8 seconds of music)
            generate_section = generator_options.generate_sections.add(
                start_time=len(mario_notes) * 0.3,  # Start after primer
                end_time=(len(mario_notes) + 32) * 0.3  # 32 more steps
            )

            # Generate the music
            generated_sequence = generator.generate(primer_sequence, generator_options)

            # Save as MIDI
            filename = f"mario_style_{chosen_pattern}_{i + 1}.mid"
            filepath = os.path.join(output_dir, filename)
            note_seq.sequence_proto_to_midi_file(generated_sequence, filepath)

            print(f"    ✓ Saved: {filename}")

            # Show what the AI generated
            ai_notes = [note.pitch for note in generated_sequence.notes]
            primer_notes = ai_notes[:len(mario_notes)]  # Original primer
            generated_notes = ai_notes[len(mario_notes):]  # AI generated part

            print(f"    Original: {primer_notes}")
            print(f"    AI added: {generated_notes[:10]}..." if len(
                generated_notes) > 10 else f"    AI added: {generated_notes}")

        print(f"\n✓ Generated 3 Mario-style MIDI files in '{output_dir}/'")
        print("\nFiles created:")
        for i in range(3):
            print(f"  - mario_style_{chosen_pattern}_{i + 1}.mid")

        print("\n" + "=" * 60)
        print("LISTEN TO THE RESULTS!")
        print("=" * 60)
        print("These should sound much more like coherent video game music")
        print("because the AI was trained on Nintendo/gaming MIDI files!")
        print("The AI should continue the bouncy, 8-bit Mario-style melody.")

        return True

    except FileNotFoundError:
        print("✗ Error: basic_rnn.mag not found!")
        print("Make sure you have downloaded the model file to the current directory.")
        return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def compare_with_gotye():
    """
    Optional: Generate both Mario and Gotye for comparison.
    """
    print("\n" + "=" * 60)
    print("BONUS: COMPARISON TEST")
    print("=" * 60)

    # Generate Gotye style (should sound random/wandering)
    gotye_notes = [62, 74, 69, 60]

    # Generate Mario style (should sound coherent/musical)
    mario_notes = [72, 72, 72, 68, 72, 76, 64]

    patterns_to_test = {
        "gotye_style": gotye_notes,
        "mario_style": mario_notes
    }

    for style_name, pattern in patterns_to_test.items():
        print(f"\nGenerating {style_name}...")

        try:
            # Quick generation
            bundle = sequence_generator_bundle.read_bundle_file("basic_rnn.mag")
            generator = melody_rnn_sequence_generator.get_generator_map()['basic_rnn'](bundle=bundle)
            generator.initialize()

            # Create primer
            primer = note_seq.NoteSequence()
            primer.tempos.add(time=0, qpm=120)
            for i, pitch in enumerate(pattern):
                primer.notes.add(pitch=pitch, start_time=i * 0.5, end_time=(i + 1) * 0.5, velocity=80)
            primer = note_seq.quantize_note_sequence(primer, steps_per_quarter=4)

            # Generate
            options = generator_pb2.GeneratorOptions()
            options.args['temperature'].float_value = 1.0
            options.generate_sections.add(start_time=len(pattern) * 0.5, end_time=(len(pattern) + 16) * 0.5)

            result = generator.generate(primer, options)
            note_seq.sequence_proto_to_midi_file(result, f"comparison_{style_name}.mid")

            print(f"✓ Saved: comparison_{style_name}.mid")

        except Exception as e:
            print(f"✗ Failed {style_name}: {e}")

    print("\nCompare the two files:")
    print("- comparison_mario_style.mid (should sound musical)")
    print("- comparison_gotye_style.mid (might sound random)")


if __name__ == "__main__":
    print("MARIO-STYLE MUSIC GENERATION TEST")
    print("This should work much better than Gotye!")
    print("\nChoose an option:")
    print("1. Generate Mario-style music (recommended)")
    print("2. Generate comparison (Mario vs Gotye)")
    print("3. Both")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        generate_mario_style_music()
    elif choice == "2":
        compare_with_gotye()
    elif choice == "3":
        generate_mario_style_music()
        compare_with_gotye()
    else:
        print("Invalid choice, running Mario generation...")
        generate_mario_style_music()