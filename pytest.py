# REAL Magenta AI - Using Neural Networks for Music Generation
# This uses actual machine learning models, not manual note placement!

import note_seq
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
import tempfile
import os


def download_model_if_needed():
    """
    Download a pre-trained Magenta model if we don't have it.
    """
    model_name = 'basic_rnn.mag'
    if not os.path.exists(model_name):
        print("Downloading pre-trained AI model...")
        import urllib.request
        url = 'https://storage.googleapis.com/magentadata/models/melody_rnn/basic_rnn.mag'
        try:
            urllib.request.urlretrieve(url, model_name)
            print(f"✓ Downloaded {model_name}")
        except Exception as e:
            print(f"Could not download model: {e}")
            return None
    return model_name


def create_primer_sequence(notes):
    """
    Create a primer sequence from your Gotye notes that the AI can continue.
    """
    print("Creating primer sequence for AI...")

    # Your Gotye notes: D4, D5, A4, C4, C5, G4, A4, F5
    # MIDI: [62, 74, 69, 60, 72, 67, 69, 77]

    sequence = note_seq.NoteSequence()
    sequence.tempos.add(time=0, qpm=120)

    # Only use first few notes as "primer" - let AI generate the rest
    primer_notes = notes[:4]  # Just the first 4 notes
    print(f"Primer notes (for AI to learn from): {primer_notes}")

    for i, pitch in enumerate(primer_notes):
        sequence.notes.add(
            pitch=pitch,
            start_time=i * 0.5,
            end_time=(i + 1) * 0.5,
            velocity=80,
            instrument=0
        )

    # Important: Quantize the sequence for the AI model
    quantized_sequence = note_seq.quantize_note_sequence(sequence, steps_per_quarter=4)

    return quantized_sequence


def generate_with_ai(primer_sequence, model_path):
    """
    Use actual Magenta AI to generate music based on the primer.
    """
    print("\n" + "=" * 50)
    print("USING REAL MAGENTA AI!")
    print("=" * 50)

    try:
        # Load the pre-trained neural network
        print("Loading AI model...")
        bundle = sequence_generator_bundle.read_bundle_file(model_path)

        # Get the generator (this is the actual AI!)
        generator_map = melody_rnn_sequence_generator.get_generator_map()
        melody_rnn = generator_map['basic_rnn'](bundle=bundle)
        melody_rnn.initialize()
        print("✓ AI model loaded and ready!")

        # Set generation options
        generator_options = melody_rnn_sequence_generator.MelodyRnnSequenceGeneratorOptions()
        generator_options.num_outputs = 3  # Generate 3 different variations
        generator_options.num_steps = 32  # Generate 32 more notes
        generator_options.temperature = 1.0  # Creativity level (0.5=conservative, 1.5=wild)

        print(f"Asking AI to continue your melody...")
        print(f"Primer: First 4 notes of your sequence")
        print(f"AI will generate: {generator_options.num_steps} more notes")
        print(f"Creating: {generator_options.num_outputs} different variations")

        # THIS IS THE MAGIC - AI GENERATES MUSIC!
        generated_sequences = melody_rnn.generate(primer_sequence, generator_options)

        print(f"✓ AI generated {len(generated_sequences)} melodies!")

        return generated_sequences

    except Exception as e:
        print(f"AI generation failed: {e}")
        print("This might be due to model compatibility issues.")
        return None


def analyze_ai_output(original_notes, generated_sequences):
    """
    Compare what the AI generated vs your original melody.
    """
    print("\n" + "=" * 50)
    print("AI ANALYSIS - Did it learn your pattern?")
    print("=" * 50)

    print(f"Your original melody: {original_notes}")

    for i, sequence in enumerate(generated_sequences):
        ai_notes = [note.pitch for note in sequence.notes]
        print(f"\nAI Generation #{i + 1}: {ai_notes}")

        # Check if AI used similar note patterns
        original_intervals = [original_notes[i + 1] - original_notes[i] for i in range(len(original_notes) - 1)]
        ai_intervals = [ai_notes[i + 1] - ai_notes[i] for i in range(min(len(ai_notes) - 1, len(original_intervals)))]

        print(f"  Original intervals: {original_intervals[:5]}...")
        print(f"  AI intervals: {ai_intervals[:5]}...")

        # Check if AI stayed in similar pitch range
        original_range = (min(original_notes), max(original_notes))
        ai_range = (min(ai_notes), max(ai_notes))
        print(f"  Original range: {original_range}")
        print(f"  AI range: {ai_range}")


def save_sequences(sequences, prefix="ai_generated"):
    """
    Save all the AI-generated sequences as MIDI files.
    """
    for i, sequence in enumerate(sequences):
        filename = f"{prefix}_{i + 1}.mid"
        note_seq.sequence_proto_to_midi_file(sequence, filename)
        print(f"✓ Saved: {filename}")


def main():
    """
    Main function - demonstrates real Magenta AI in action!
    """
    print("=" * 60)
    print("REAL MAGENTA AI TEST")
    print("Can AI learn and continue your Gotye melody pattern?")
    print("=" * 60)

    # Your original Gotye notes
    gotye_notes = [62, 74, 69, 60, 72, 67, 69, 77]  # D4, D5, A4, C4, C5, G4, A4, F5

    # Step 1: Download AI model
    model_path = download_model_if_needed()
    if not model_path:
        print("Could not get AI model. Try manual download.")
        return

    # Step 2: Create primer for AI
    primer = create_primer_sequence(gotye_notes)

    # Step 3: Let AI generate continuations
    ai_sequences = generate_with_ai(primer, model_path)

    if ai_sequences:
        # Step 4: Analyze what AI created
        analyze_ai_output(gotye_notes, ai_sequences)

        # Step 5: Save AI generations
        save_sequences(ai_sequences, "gotye_ai")

        print("\n" + "=" * 60)
        print("EXPERIMENT COMPLETE!")
        print("=" * 60)
        print("Check the generated MIDI files:")
        for i in range(len(ai_sequences)):
            print(f"- gotye_ai_{i + 1}.mid")
        print("\nThe AI learned from your melody and created variations!")
        print("This is REAL machine learning in action!")

    else:
        print("AI generation failed, but we learned about the process!")


if __name__ == "__main__":
    main()