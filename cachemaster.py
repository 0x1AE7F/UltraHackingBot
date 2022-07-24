import os
import time


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


curr_path = os.getcwd()
search_cache_path = curr_path+"/search_cache/"

if os.path.exists(path=curr_path+"/search_cache"):
    pass
else:
    os.mkdir(path=curr_path+"/search_cache")


def new_cache_entry(entry_name, description_data, url, see_more_url):
    # Deletes old cache
    if os.path.exists(f"{search_cache_path}{entry_name}.result"):
        os.remove(f"{search_cache_path}{entry_name}.result")
    try:
        with open(f"{search_cache_path}{entry_name}.result", 'w+') as f:
            f.write(str(description_data)+"\n"+str(url)+"\n"+str(see_more_url))
            f.close()
            print(
                f"{colors.OKGREEN}[CACHEMASTER_PASS]: Successfully added new entry to cache{colors.ENDC}")
            return None
    except Exception as e:
        return e


def check_cache(entry_name):
    if os.path.exists(f"{search_cache_path}{entry_name}.result"):
        st = os.stat(f"{search_cache_path}{entry_name}.result")
        time_diff = time.time() - st.st_mtime
        print(time_diff)
        if time_diff > 86400:
            print(
                f"{colors.WARNING}[CACHEMASTER_INFO]: File '{entry_name}' is older than 1 Day.. Fetching new results.{colors.ENDC}")
            return False
        print(
            f"{colors.OKBLUE}[CACHEMASTER_INFO]: Found cache entry.{colors.ENDC}")
        return True
    else:
        print(
            f"{colors.WARNING}[CACHEMASTER_INFO]: No cache entry found.{colors.ENDC}")
        return False


def read_cache(entry_name):
    if os.path.exists(f"{search_cache_path}{entry_name}.result"):
        pass
    else:
        print(
            f"{colors.FAIL}[CACHEMASTER_ERROR]: Cache entry does not exist.{colors.ENDC}")
        return None

    with open(f"{search_cache_path}{entry_name}.result", 'r') as f:
        cache_file_data = f.readlines()
        cve_mitre_url = cache_file_data[-1].strip()
        read_more_url = cache_file_data[len(cache_file_data)-2].strip()
        cache_file_data.pop(len(cache_file_data)-1)
        cache_file_data.pop(len(cache_file_data)-1)
        cache_file_data = str(cache_file_data[0])
        f.close()
        return cache_file_data, cve_mitre_url, read_more_url
