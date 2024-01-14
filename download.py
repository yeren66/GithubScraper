import threading
import subprocess
import os
import logging
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import utils
import time

# 初始化日志记录器
logging.basicConfig(filename='fail_message_catch.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 封装下载功能
class RepoDownloader:
    def __init__(self, repo_data, local_path=".", max_threads=10):
        self.repo_data = repo_data
        self.local_path = os.path.abspath(local_path)
        self.max_threads = max_threads
        self.fail_download_file = "fail_download.json"
        # 创建目录（如果不存在）
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)
        # 更改工作目录
        os.chdir(self.local_path)

    def clone_repo(self, repo):
        try:
            repo_name = repo['project_name']
            url = repo['url']
            if not os.path.exists(repo_name):
                subprocess.run(["git", "clone", url], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logging.error(f"Error cloning {url}: {e}")
            utils.save_to_file(repo, self.fail_download_file)
            # 遇到错误时暂停3分钟
            time.sleep(180)
            raise

    def download_repos(self):
        with tqdm(total=len(self.repo_data)) as progress_bar:
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = {executor.submit(self.clone_repo, repo): repo for repo in self.repo_data}
                for future in futures:
                    repo = futures[future]
                    try:
                        future.result(timeout=600)  # 设置超时为10分钟
                        progress_bar.update(1)
                    except TimeoutError:
                        logging.error(f"Timeout while cloning {repo['url']}")
                        utils.save_to_file(repo, self.fail_download_file)
                    except Exception as e:
                        logging.error(f"Exception while cloning {repo['url']}: {e}")
                        # 这里已经在 clone_repo 方法中处理了错误，所以不需要再次处理

if __name__ == "__main__":
    # 从JSON文件中读取仓库信息
    repo_data = utils.read_json("fail_result.json")
    
    downloader = RepoDownloader(repo_data, "D:\\GithubRepos\\repos", max_threads=5)
    downloader.download_repos()
