import dotenv
import os 
from pinatapy import PinataPy

IMAGE_DIR_PATH="./imgs/out"
METADATA_DIR_PATH="./json/"

    # handle upload to ipfs
def upload_images():
    # load pinata api keys
    dotenv.load_dotenv()
    api_key = os.getenv("PINATA_API_KEY")
    secret = os.getenv("PINATA_SECRET_API_KEY")

    # open image to upload
    # create pinata instance and upload to pinata
    if api_key is None or secret is None:
        print("Pinata API key or secret key is not set")
        return


    pinata = PinataPy(pinata_api_key=api_key, pinata_secret_api_key=secret)
    pinata_response = pinata.pin_file_to_ipfs(IMAGE_DIR_PATH, save_absolute_paths=False)

    # return ipfs hash
    return pinata_response["IpfsHash"]

def main(): 
    print("beginning image upload process")
    # only operate on copies of the images to avoid any issue with corruption
    ipfs_hash = upload_images()
    print("image upload process complete")
    print(f"ipfs hash: {ipfs_hash}")
    print("beginning modification process")

    



if __name__ == "__main__":
    main()




