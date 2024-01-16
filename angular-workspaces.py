import json
import os

def is_angular_workspace(folder_name):
    package_json_path = os.path.join(folder_name, 'package.json')
    angular_json_path = os.path.join(folder_name, 'angular.json')
    nx_json_path = os.path.join(folder_name, 'nx.json')

    # Check for the existence of angular.json and absence of nx.json
    has_angular_json = os.path.exists(angular_json_path)
    has_nx_json = os.path.exists(nx_json_path)

    # Check package.json for @nrwl/angular or @nx/angular dependency
    has_valid_dependency = False
    if os.path.exists(package_json_path):
        with open(package_json_path, 'r') as file:
            data = json.load(file)
            dependencies = data.get('dependencies', {})
            dev_dependencies = data.get('devDependencies', {})

            # Check for additional @nrwl or @nx dependencies
            has_additional_nrwl_deps = any(dep.startswith('@nrwl/') and dep != '@nrwl/angular' for dep in dependencies) or any(dep.startswith('@nrwl/') and dep != '@nrwl/angular' for dep in dev_dependencies)
            has_additional_nx_deps = any(dep.startswith('@nx/') and dep != '@nx/angular' for dep in dependencies) or any(dep.startswith('@nx/') and dep != '@nx/angular' for dep in dev_dependencies)
            
            # Check if ngx-deploy-npm exists in dependencies or devDependencies
            has_ngx_deploy_npm = 'ngx-deploy-npm' in dependencies or 'ngx-deploy-npm' in dev_dependencies

            has_valid_dependency = has_ngx_deploy_npm and not (has_additional_nrwl_deps or has_additional_nx_deps)

    return has_angular_json and not has_nx_json and has_valid_dependency

def collect_info(folder_name):
    try:
        # Read existing info if it exists
        info_file = f'{folder_name}/ngx-dependant.ingo.json'
        existing_info = {}
        if os.path.exists(info_file):
            with open(info_file, 'r') as file:
                existing_info = json.load(file)

        # Read angular version from package.json
        package_json_path = f'{folder_name}/package.json'
        angular_version = None
        ngx_deploy_version = None
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as file:
                data = json.load(file)
                dependencies = data.get('dependencies', {})
                dev_dependencies = data.get('devDependencies', {})

                angular_version = dependencies.get('@angular/core')

                 # Get ngx-deploy-npm version from dependencies or devDependencies
                if 'ngx-deploy-npm' in dependencies:
                    ngx_deploy_version = dependencies.get('ngx-deploy-npm')
                elif 'ngx-deploy-npm' in dev_dependencies:
                    ngx_deploy_version = dev_dependencies.get('ngx-deploy-npm')
                

        # Collect required info
        collected_info = {
            'repo_name': existing_info.get('repo_name'),
            'stars': existing_info.get('stars'),
            'angular_version': angular_version,
            'ngx_deploy_version': ngx_deploy_version
        }

        # Read existing data from dependant.json or initialize empty list
        if os.path.exists('dependant.json'):
            with open('dependant.json', 'r') as file:
                existing_data = json.load(file)
        else:
            existing_data = []

         # Append the new item to the existing data
        existing_data.append(collected_info)

        # Write the updated data (with the appended item) back to the file
        with open('dependant.json', 'w') as file:
            json.dump(existing_data, file, indent=4)    

    except Exception as e:
        print(f"An error occurred: {e}")

def process_repositories():
    repos_directory = 'repos'

    for folder_name in os.listdir(repos_directory):
        full_path = os.path.join(repos_directory, folder_name)

        if os.path.isdir(full_path):
            if is_angular_workspace(full_path):
                print(f"Repository '{folder_name}' is an Angular workspace")
                collect_info(full_path)
            # else:
            #     print(f"Repository '{folder_name}' is not an Angular workspace")

if __name__ == "__main__":
    process_repositories()
