# CartoonGAN — Photo Cartoonisation with Generative Adversarial Networks

> **Suggested repository name:** `cartoongan` or `real2cartoon`

A PyTorch implementation of a GAN-based system that transforms real-world photographs into anime-style cartoon images, inspired by the styles of directors such as Makoto Shinkai, Mamoru Hosoda, and Miyazaki Hayao.

![Training result at epoch 327](results_at_epoch_327.png)

---

## Overview

This project trains a **Generator–Discriminator** (GAN) pair where:

- The **Generator** is a residual U-Net that converts a real photograph into a cartoon-styled image.
- The **Discriminator** learns to distinguish real cartoon frames from generated ones.
- Training uses a combination of **adversarial loss** and **VGG-based content loss** to preserve structural similarity while achieving a stylised appearance.

---

## Repository Structure

```
.
├── cartoongan_training.ipynb        # Main training notebook (model definitions, training loop, evaluation)
├── preprocess_cartoon_images.py     # Resize, crop, and apply Canny edge detection to cartoon frames
├── extract_cartoon_frames.py        # Extract frames from anime video files using ffmpeg
├── fetch_flickr_urls.py             # Fetch real-world photo URLs from Flickr API
├── download_real_world_images.py    # Download and preprocess real-world photos from a URL list
├── image_urls.txt                   # Pre-fetched Flickr image URLs (nature, city, landscape, etc.)
├── results_at_epoch_327.png         # Sample generator output at epoch 327
└── LICENSE
```

---

## Requirements

- Python 3.8+
- PyTorch ≥ 2.0 with CUDA support (GPU strongly recommended)
- `torchvision`
- `opencv-python` (`cv2`)
- `Pillow`
- `scipy`
- `flickrapi` _(only needed for `fetch_flickr_urls.py`)_
- `requests`
- `ffmpeg` on system PATH _(only needed for `extract_cartoon_frames.py`)_

Install Python dependencies:

```bash
pip install torch torchvision opencv-python Pillow scipy flickrapi requests
```

---

## Data Preparation

### 1. Fetch real-world photo URLs from Flickr

Set your Flickr API credentials as environment variables, then run:

```bash
export FLICKR_API_KEY=your_api_key
export FLICKR_API_SECRET=your_api_secret
python fetch_flickr_urls.py          # writes URLs to image_urls.txt
```

### 2. Download and preprocess real-world photos

```bash
python download_real_world_images.py  # downloads images and resizes to 256×256
```

### 3. Extract frames from cartoon videos

Place your video files in the project root (or update the paths in the script), then:

```bash
# Optionally set FFMPEG_PATH if ffmpeg is not on your system PATH
export FFMPEG_PATH=/usr/local/bin/ffmpeg
python extract_cartoon_frames.py
```

### 4. Preprocess cartoon frames (edge detection)

```bash
python preprocess_cartoon_images.py
```

This resizes cartoon frames to 256×256, applies Canny edge detection, dilates and smooths the edges, and saves both the resized image and the edge-processed version.

---

## Training

Open and run `cartoongan_training.ipynb` in Jupyter (or JupyterLab):

```bash
jupyter notebook cartoongan_training.ipynb
```

The notebook covers:

1. Data loading and augmentation
2. Generator and Discriminator architecture
3. Initialisation phase (content loss only)
4. Main training loop (adversarial + content loss)
5. FID / Inception Score evaluation
6. Inference on test images

Model checkpoints are saved as `checkpoint_epoch_<N>.pth.tar`.

---

## Results

Below is a sample output from the generator after 327 training epochs:

![Epoch 327 results](results_at_epoch_327.png)

---

## License

This project is licensed under the terms of the [LICENSE](LICENSE) file.
