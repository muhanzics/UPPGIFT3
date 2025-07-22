# Magenta Model Downloader - Updated URLs
import urllib.request
import os


def download_magenta_models():
    """
    Download pre-trained Magenta models from the correct URLs.
    """

    # Updated working URLs
    models = {
        'basic_rnn.mag': 'https://storage.googleapis.com/download.magenta.tensorflow.org/models/melody_rnn/basic_rnn.mag',
        'attention_rnn.mag': 'https://storage.googleapis.com/download.magenta.tensorflow.org/models/melody_rnn/attention_rnn.mag',
        'lookback_rnn.mag': 'https://storage.googleapis.com/download.magenta.tensorflow.org/models/melody_rnn/lookback_rnn.mag'
    }

    print("Downloading Magenta pre-trained models...")
    print("=" * 50)

    for filename, url in models.items():
        if os.path.exists(filename):
            print(f"✓ {filename} already exists, skipping...")
            continue

        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, filename)

            # Check file size
            file_size = os.path.getsize(filename) / (1024 * 1024)  # MB
            print(f"✓ Downloaded {filename} ({file_size:.1f} MB)")

        except Exception as e:
            print(f"✗ Failed to download {filename}: {e}")

    print("\n" + "=" * 50)
    print("Download complete!")

    # List downloaded files
    print("Available models:")
    for filename in models.keys():
        if os.path.exists(filename):
            size = os.path.getsize(filename) / (1024 * 1024)
            print(f"- {filename} ({size:.1f} MB)")


if __name__ == "__main__":
    download_magenta_models()