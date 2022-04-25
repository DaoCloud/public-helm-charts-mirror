import os
import yaml

mirror_filename = 'mirror.yaml'
config_filename = 'config.yaml'
sync_config_dir = "config"


def generate_sync_file(chart_name, src_repo_url, dest_repo_name, dest_repo_url,
                       container_repository=None, container_registry=None):
    sync_config_filename = dest_repo_name + "-" + chart_name + '.yaml'
    print("generate %s %s sync to %s in %s" %
          (src_repo_url, chart_name, dest_repo_url, sync_config_filename))

    data = {"charts": [chart_name],
            "source": {
                "repo": {
                    "kind": "HELM",
                    "url": src_repo_url
                }
            },
            "target": {
                "repo": {
                    "kind": "HARBOR",
                    "url": dest_repo_url
                }
            }
        }

    if container_repository:
        data.get("target")["containerRepository"] = container_repository
    if container_registry:
        data.get("target")["containerRegistry"] = container_registry
    with open(os.path.join(sync_config_dir, sync_config_filename), "w") as f:
        yaml.dump(data, f)

def genreate():
    mirror = {}
    config = {}

    with open(mirror_filename) as f:
        mirror = yaml.load(f, Loader=yaml.FullLoader)
    with open(config_filename) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    for dest_repo_name, charts in mirror.get("mirrors", {}).items():
        for chart_name in charts:
            repo = charts.get(chart_name)
            src_repo_url = repo
            container_repository = None
            container_registry = None
            if type(repo) is dict:
                src_repo_url = repo.get("repo")
                container_repository = repo.get("containerRepository")
                container_registry = repo.get("containerRegistry")
            dest_repo_url = config.get("mirrorRepos", {}).get(dest_repo_name)
            generate_sync_file(chart_name, src_repo_url, dest_repo_name,
                               dest_repo_url, container_repository, container_registry)


if __name__ == '__main__':
    genreate()
