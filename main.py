import dotenv
import json
import os 
from pinatapy import PinataPy

# make local copies of img and json directories here
IMAGE_DIR_PATH="./imgs/out"
METADATA_DIR_PATH="./json/"

UPLOAD_METADATA = False

# handle upload to ipfs
def upload_images(pinata):

    image_dir_path = os.path.abspath(IMAGE_DIR_PATH)
    pinata_response = pinata.pin_file_to_ipfs(image_dir_path, save_absolute_paths=False)
    return pinata_response["IpfsHash"]

# handle modification of metadata
def modify_metadata(ipfs_hash):
    for i in range(1, 501):
        # only operate on copies of the images to avoid any issue with corruption
        metadata_path = os.path.abspath(f"{METADATA_DIR_PATH}{i}")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r") as f:
                metadata = json.load(f)
             # Modify the 'image' field
             # For example, let's set it to 'new_image.png'
            if 'image' in metadata:
                 metadata['image'] = f"ipfs://{ipfs_hash}/{i}.png"
            else:
                 print("'image' field not found in the JSON file")

           # Save the modified JSON back to the file
            with open(metadata_path, 'w') as file:
                json.dump(metadata, file, indent=4)




def upload_metadata(pinata):
    metadata_dir_path = os.path.abspath(METADATA_DIR_PATH)
    pinata_response = pinata.pin_file_to_ipfs(metadata_dir_path, save_absolute_paths=False)
    return pinata_response["IpfsHash"]


def main(): 
    # load pinata api keys
    dotenv.load_dotenv()
    api_key = os.getenv("PINATA_API_KEY")
    secret_key = os.getenv("PINATA_SECRET_API_KEY")

    # open image to upload
    # create pinata instance and upload to pinata
    if api_key is None or secret_key is None:
        print("Pinata API key or secret key is not set")
        return

    # create pinata instance 
    pinata = PinataPy(pinata_api_key=api_key, pinata_secret_api_key=secret_key)

    # execute uplaoding and modification process

    if not UPLOAD_METADATA:
        print("beginning image upload process")
        ipfs_hash = upload_images(pinata)
        print("image upload process complete")
        print("beginning modification process")
        modify_metadata(ipfs_hash)
        print("modification process complete")

    else: 
        print("beginning metadata upload process")  
        upload_metadata(pinata)


if __name__ == "__main__":
    main()




