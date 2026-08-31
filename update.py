import subprocess

if __name__ == "__main__":
    print("Updating SVGs...")
    subprocess.run(["python", "update_svgs.py"], check=True)
    print("Done!")
