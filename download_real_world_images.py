import os
import requests
from PIL import Image
from io import BytesIO
from torchvision import transforms
import concurrent.futures

def download_image(url, save_dir):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content)).convert('RGB')
            filename = os.path.basename(url)
            save_path = os.path.join(save_dir, filename)
            img.save(save_path)
            return filename
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    return None

def prepare_image(img_path, output_dir, size=(256, 256)):
    try:
        transform = transforms.Compose([
            transforms.Resize(size),
            transforms.CenterCrop(size),
            transforms.ToTensor()
        ])
        img = Image.open(img_path).convert('RGB')
        img = transform(img)
        filename = os.path.basename(img_path)
        output_path = os.path.join(output_dir, filename)
        transforms.ToPILImage()(img).save(output_path)
        return filename
    except Exception as e:
        print(f"Failed to process {img_path}: {e}")
    return None

def process_images(input_dir, output_dir, size=(256, 256)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(input_dir):
            img_path = os.path.join(input_dir, filename)
            if filename.endswith('.jpg') or filename.endswith('.png'):
                futures.append(executor.submit(prepare_image, img_path, output_dir, size))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(f"Processed {result}")

def batch_download_and_process(url_file, download_dir, processed_dir, size=(256, 256)):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    with open(url_file, 'r') as file:
        urls = file.read().splitlines()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for url in urls:
            futures.append(executor.submit(download_image, url, download_dir))
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(f"Downloaded {result}")

    process_images(download_dir, processed_dir, size)

# Example usage:
# Save URLs in 'image_urls.txt'
url_file = 'image_urls.txt'
download_dir = 'data/photos'
processed_dir = 'data/photos_prepared'
batch_download_and_process(url_file, download_dir, processed_dir)
