from tqdm import tqdm
from multiprocessing import Pool
from utils import get_file_paths, detect_pii, read_progress, write_header_file_ref

progress = read_progress()

def run(path:str) -> None:
    if path in progress:
        print('Skip', flush=True)
        pass
    else:
        detect_pii(path)


def main():
    paths_list = get_file_paths()
    write_header_file_ref()
    len_paths = len(paths_list)
    p = Pool(4)

    for _ in tqdm(p.imap_unordered(run, paths_list), total=len_paths):
        pass

    print("Program finished!")

if __name__ == "__main__":
    main()

