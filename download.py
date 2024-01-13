import threading
import subprocess
import os
import json
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import utils

# 初始化日志记录器
logging.basicConfig(level=logging.ERROR, filename='download_error.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# 封装下载功能
class RepoDownloader:
    def __init__(self, repo_data, local_path=".", max_threads=10):
        self.repo_data = repo_data
        self.local_path = os.path.abspath(local_path)
        self.max_threads = max_threads
        self.failed_repos = []
        fail_download_file = "fail_download.json"

        # 创建目录（如果不存在）
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        # 更改工作目录
        os.chdir(self.local_path)

    def clone_repo(self, repo, progress_bar):
        try:
            repo_name = repo['project_name']
            url = repo['url']
            if not os.path.exists(repo_name):
                subprocess.run(["git", "clone", url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                progress_bar.update(1)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error cloning {url}: {e}")
            utils.save_to_file(repo, self.fail_download_file)

    def download_repos(self):
        with tqdm(total=len(self.repo_data)) as progress_bar:
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                for repo in self.repo_data:
                    executor.submit(self.clone_repo, repo, progress_bar)

if __name__ == "__main__":
    # 从JSON文件中读取仓库信息
    repo_data = utils.read_json("gather_result.json")
    
    downloader = RepoDownloader(repo_data, "/path/to/download", max_threads=5)
    downloader.download_repos()
    downloader.save_failed_repos()
