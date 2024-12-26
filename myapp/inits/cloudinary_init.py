from decouple import config
import cloudinary
import os

def cloudinary_init():
    if os.getenv('RUN_MAIN') == 'true':
        print("Initializing Cloudinary configuration")
        print(f"CLOUDINARY_CLOUD_NAME: {config('CLOUDINARY_CLOUD_NAME')}")
        print(f"CLOUDINARY_API_KEY: {config('CLOUDINARY_API_KEY')}")
        print(f"CLOUDINARY_API_SECRET: {config('CLOUDINARY_API_SECRET')}")
        cloudinary.config(
            cloud_name=config('CLOUDINARY_CLOUD_NAME'),
            api_key=config('CLOUDINARY_API_KEY'),
            api_secret=config('CLOUDINARY_API_SECRET'),
            secure=True
        )