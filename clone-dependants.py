import json
import subprocess
from concurrent.futures import ThreadPoolExecutor

def clone_repository(dependent):
    try:
        repo_name = dependent['name']
        stars = dependent['stars']
        repo_URL = f"https://github.com/{repo_name}.git"
        folder_name = f"repos/{repo_name.split('/')[1]}"

        subprocess.run(['git', 'clone', '--depth=1', repo_URL, folder_name], check=True)
        print(f"Repository '{repo_name}' cloned successfully")

        # Create file info
        print(f"Writing info on '{repo_name}'")
        with open(f'{folder_name}/ngx-dependant.ingo.json', 'a') as file:
            data = {
                'repo_name': repo_name,
                'stars': stars
            }
            json.dump(data, file)

    except subprocess.CalledProcessError as e:
        print(f"Failed to clone repository '{repo_name}': {e}")
    except Exception as e:
        print(f"An error occurred for repository '{repo_name}': {e}")

if __name__ == "__main__":
    json_file_path = 'ngx-deploy-npm-dependants.json'

    with open(json_file_path, 'r') as file:
        dependents = json.load(file)['all_public_dependent_repos']

    # Maximum number of threads for parallel execution
    max_threads = 20  # Adjust this based on your requirements

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(clone_repository, dependents)
