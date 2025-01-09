import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


def clone_repository(repo_url, dest_folder):
    print(f"Cloning repository into {dest_folder}...")
    subprocess.run(["git", "clone", repo_url, dest_folder], check=True)


def install_packages(requirements_file):
    print("Installing necessary packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)


def install_fastreid():
    print("Installing FastReId...")
    subprocess.run([sys.executable, "-m", "pip", "install", "fastreid==1.4.0", "--no-deps"], check=True)


def replace_fastreid(src_folder, dest_folder):
    print("Replacing FastReId folder...")
    if os.path.exists(dest_folder):
        shutil.rmtree(dest_folder)
    shutil.copytree(src_folder, dest_folder)


def main():
    print("Welcome to the TransMob Installer!")

    # Ask where to place the project
    dest_folder = input("Enter the destination folder to store the project: ")
    dest_folder = os.path.abspath(dest_folder)
    os.makedirs(dest_folder, exist_ok=True)

    # Clone the repository
    repo_url = "https://github.com/AlixMenard/transmob"
    repo_folder = os.path.join(dest_folder, "transmob")
    clone_repository(repo_url, repo_folder)

    # Navigate to the cloned repository
    os.chdir(repo_folder)

    # Install necessary packages
    install_packages("requirements.txt")

    # Install FastReId
    install_fastreid()

    # Replace FastReId folder
    fastreid_src = os.path.join(dest_folder, "fastreid.zip")  # Adjust this path to your ZIP file
    fastreid_dest = str(Path(sys.executable).parent / "Lib" / "site-packages" / "fastreid")
    with zipfile.ZipFile(fastreid_src, 'r') as zip_ref:
        extracted_folder = os.path.join(dest_folder, "fastreid_extracted")
        zip_ref.extractall(extracted_folder)
    replace_fastreid(extracted_folder, fastreid_dest)

    print("Installation complete! Place the FastReId model in the FastReId_config folder as instructed.")


if __name__ == "__main__":
    main()
