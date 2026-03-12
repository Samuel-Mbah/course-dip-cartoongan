import os
import cv2
import numpy as np
from PIL import Image
from torchvision import transforms

def preprocess_images(input_dir, output_dir, size=(256, 256)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.CenterCrop(size),
        transforms.ToTensor()
    ])

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                img_path = os.path.join(root, file)
                img = Image.open(img_path).convert('RGB')
                img = transform(img)
                img = transforms.ToPILImage()(img)
                
                # Save the resized and cropped image
                processed_img_path = os.path.join(output_dir, file)
                img.save(processed_img_path)

                # Convert to OpenCV format
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                
                # Apply Canny edge detector
                edges = cv2.Canny(img_cv, 100, 200)
                
                # Dilate the edges
                kernel = np.ones((3, 3), np.uint8)
                edges_dilated = cv2.dilate(edges, kernel, iterations=1)
                
                # Apply Gaussian smoothing
                edges_smoothed = cv2.GaussianBlur(edges_dilated, (5, 5), 0)
                
                # Invert the edges for better visualization
                edges_inverted = cv2.bitwise_not(edges_smoothed)
                
                # Convert back to PIL format
                edges_img = Image.fromarray(cv2.cvtColor(edges_inverted, cv2.COLOR_BGR2RGB))
                
                # Save the edge-smoothed image
                edge_processed_img_path = os.path.join(output_dir, f'edge_{file}')
                edges_img.save(edge_processed_img_path)
                print(f"Processed and saved: {file} and edge_{file}")

# Example usage:
input_dir = 'Cartoon_data/cartoon_images'
output_dir = 'Cartoon_data/cartoon_images_preprocessed'
preprocess_images(input_dir, output_dir)
