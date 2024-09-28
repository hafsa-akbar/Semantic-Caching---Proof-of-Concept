import os
import random
from client import get_image, clear_cache

SERVER_IMAGE_DIR = '../server/images'
LOG_FILE = 'download_log.txt'

def get_all_image_ids():
    image_ids = []
    for category in os.listdir(SERVER_IMAGE_DIR):
        category_path = os.path.join(SERVER_IMAGE_DIR, category)
        if os.path.isdir(category_path):
            for image_file in os.listdir(category_path):
                if image_file.endswith('.jpg'):
                    image_id = image_file.replace('.jpg', '')
                    image_ids.append(image_id)
    return image_ids

def pick_random_images(image_ids, num_images=30):
    return random.choices(image_ids, k=num_images)

def create_multiple_image_lists(image_ids, num_lists=10, num_images=30):
    return [pick_random_images(image_ids, num_images) for _ in range(num_lists)]

def process_images(image_list, simple_cache):
    clear_cache()
    total_download_bytes = 0
    for image_id in image_list:
       total_download_bytes += get_image(image_id, simple_cache=simple_cache, display=False)
        
    return total_download_bytes

def log_download_data(image_list, simple_cache_bytes, similarity_cache_bytes, list_index):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"Random Image List {list_index + 1}\n")
        log_file.write(f"Images: {', '.join(image_list)}\n")
        log_file.write(f"Data Downloaded with Simple Cache: {simple_cache_bytes / 1024:.2f} KB\n")
        log_file.write(f"Data Downloaded with Similarity Cache: {similarity_cache_bytes / 1024:.2f} KB\n\n")

def main():
    image_ids = get_all_image_ids()
    random_image_lists = create_multiple_image_lists(image_ids)

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)  # Clear the log file at the beginning

    for index, image_list in enumerate(random_image_lists):
        similarity_cache_bytes = process_images(image_list, simple_cache=False)
        simple_cache_bytes = process_images(image_list, simple_cache=True)

        log_download_data(image_list, simple_cache_bytes, similarity_cache_bytes, index)
    
    clear_cache()

if __name__ == "__main__":
    main()