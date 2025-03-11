from PIL import Image, ImageOps
import random
import os

def process_image(filename, target_size=600):
    # Use os.path.join() to ensure proper path formatting
    upload_folder = "static/uploads"
    file_path = os.path.join(upload_folder, filename)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The image {filename} does not exist in {upload_folder}. File path: {file_path}")
    
    try:
        # Open the image and convert to RGBA mode
        img = Image.open(file_path).convert("RGBA")
        
        # Create a new image with a black background
        new_img = Image.new("RGBA", img.size)
        pixels = img.load()
        new_pixels = new_img.load()
        
        # Replace transparent pixels with solid black
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                r, g, b, a = pixels[x, y]
                if a == 0:
                    new_pixels[x, y] = (0, 0, 0, 255)  # black background for transparency
                else:
                    new_pixels[x, y] = (r, g, b, a)
        
        # Use new image
        img = new_img
        
        # Make image square by adding a black border
        width, height = img.size
        if width > height:
            change = (width - height) // 2
            img = ImageOps.expand(img, border=(0, change, 0, change), fill="black")
        else:
            change = (height - width) // 2
            img = ImageOps.expand(img, border=(change, 0, change, 0), fill="black")
        
        # Resize the image to the target size, keeping the aspect ratio
        img = img.resize((target_size, target_size), resample=Image.NEAREST)
        
        # Generate a random filename for the output
        name = f"{random.randint(1, 99999)}.png"
        output_path = os.path.join(upload_folder, name)
        
        # Save the processed image
        img.save(output_path)
        
        # Return the filename of the saved image
        return name

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e