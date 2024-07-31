from PIL import Image
import numpy as np
import requests
import matplotlib.pyplot as plt
import pickle

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return Image.open(save_path)
    else:
        raise Exception(f"Failed to download image. Status code: {response.status_code}")

def shift_color_channels(pixels, shift_amount):
    return np.roll(pixels, shift_amount, axis=-1)

def add_noise(pixels, noise_level):
    noise = np.random.randint(0, noise_level, pixels.shape, dtype=np.uint8)
    noisy_pixels = (pixels + noise) % 256
    return noisy_pixels, noise

def remove_noise(pixels, noise):
    clean_pixels = (pixels - noise) % 256
    return clean_pixels

def shuffle_pixels(pixels):
    rows, cols, channels = pixels.shape
    flat_pixels = pixels.reshape(-1, channels)
    indices = np.arange(flat_pixels.shape[0])
    np.random.shuffle(indices)
    shuffled_pixels = flat_pixels[indices]
    return shuffled_pixels.reshape(rows, cols, channels), indices

def unshuffle_pixels(pixels, indices):
    rows, cols, channels = pixels.shape
    flat_pixels = pixels.reshape(-1, channels)
    unshuffled_pixels = np.empty_like(flat_pixels)
    unshuffled_pixels[indices] = flat_pixels
    return unshuffled_pixels.reshape(rows, cols, channels)

def encrypt_image(image_path_or_url, output_path, noise_path, shuffle_path, operation='add', key=50, noise_level=50, shift_amount=1):
    if image_path_or_url.startswith('http'):
        img = download_image(image_path_or_url, 'original_image.jpg')
    else:
        img = Image.open(image_path_or_url)
    
    img = img.convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    
    if operation == 'add':
        pixels = (pixels + key) % 256
    elif operation == 'multiply':
        pixels = (pixels * key) % 256
    elif operation == 'swap':
        if key is None or len(key) != 4:
            raise ValueError("Key for 'swap' operation must be a tuple of four integers")
        x1, y1, x2, y2 = key
        pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]
    else:
        raise ValueError("Unsupported operation. Supported operations: 'add', 'multiply', 'swap'")
    
    pixels, noise = add_noise(pixels, noise_level)
    pixels, indices = shuffle_pixels(pixels)
    pixels = shift_color_channels(pixels, shift_amount)
    
    pixels = np.array(pixels, dtype=np.uint8)
    encrypted_img = Image.fromarray(pixels)
    encrypted_img.save(output_path)
    print(f"Encrypted image saved to {output_path}")

    with open(noise_path, 'wb') as f:
        pickle.dump(noise, f)
    print(f"Noise data saved to {noise_path}")

    with open(shuffle_path, 'wb') as f:
        pickle.dump(indices, f)
    print(f"Shuffle order saved to {shuffle_path}")

def decrypt_image(image_path_or_url, output_path, noise_path, shuffle_path, operation='add', key=50, shift_amount=1):
    if image_path_or_url.startswith('http'):
        img = download_image(image_path_or_url, 'encrypted_image.jpg')
    else:
        img = Image.open(image_path_or_url)
    
    img = img.convert('RGB')
    pixels = np.array(img, dtype=np.uint8)
    
    with open(noise_path, 'rb') as f:
        noise = pickle.load(f)
    
    with open(shuffle_path, 'rb') as f:
        indices = pickle.load(f)
    
    pixels = shift_color_channels(pixels, -shift_amount)
    
    if operation == 'add':
        pixels = (pixels - key) % 256
    elif operation == 'multiply':
        pixels = (pixels // key) % 256
    elif operation == 'swap':
        if key is None or len(key) != 4:
            raise ValueError("Key for 'swap' operation must be a tuple of four integers")
        x1, y1, x2, y2 = key
        pixels[x1, y1], pixels[x2, y2] = pixels[x2, y2], pixels[x1, y1]
    else:
        raise ValueError("Unsupported operation. Supported operations: 'add', 'multiply', 'swap'")
    
    pixels = remove_noise(pixels, noise)
    pixels = unshuffle_pixels(pixels, indices)
    
    pixels = np.array(pixels, dtype=np.uint8)
    decrypted_img = Image.fromarray(pixels)
    decrypted_img.save(output_path)
    print(f"Decrypted image saved to {output_path}")

def show_images(original_path, encrypted_path, decrypted_path):
    original_img = Image.open(original_path)
    encrypted_img = Image.open(encrypted_path)
    decrypted_img = Image.open(decrypted_path)

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    axs[0].imshow(original_img)
    axs[0].set_title('Original Image')
    axs[0].axis('off')

    axs[1].imshow(encrypted_img)
    axs[1].set_title('Encrypted Image')
    axs[1].axis('off')

    axs[2].imshow(decrypted_img)
    axs[2].set_title('Decrypted Image')
    axs[2].axis('off')

    plt.show()

image_url_or_path = input("Enter the image URL or file path: ")
encrypted_path = 'encrypted_image.png'
decrypted_path = 'decrypted_image.png'
noise_path = 'noise.pkl'
shuffle_path = 'shuffle.pkl'
original_path = 'original_image.jpg'

encrypt_image(image_url_or_path, encrypted_path, noise_path, shuffle_path, operation='add', key=50, noise_level=50, shift_amount=2)
decrypt_image(encrypted_path, decrypted_path, noise_path, shuffle_path, operation='add', key=50, shift_amount=2)
show_images(original_path, encrypted_path, decrypted_path)
