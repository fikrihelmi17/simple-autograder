import subprocess
import argparse
import json
import os

def find_file(submission_path, file_name):
    for root, dirs, files in os.walk(submission_path):
        if "node_modules" in dirs:
            dirs.remove("node_modules")
        if ".git" in dirs:
            dirs.remove(".git")

        for file in files:
            if file == file_name:
                return os.path.join(root, file), None
    return None, None

def get_params():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-submission', type=str, help='Specify submissions path')
    parser.add_argument('-report', type=str, help='Specify report path')
    args = parser.parse_args()

    if not args.submission:
        print("submission path (-submission) tidak boleh kosong")
        exit(1)

    if not args.report:
        print("report path (-report) tidak boleh kosong")
        exit(1)

    return args.submission, args.report

def run_npm_install(project_path):
    subprocess.run(["npm", "install"], cwd=project_path)

def run_main_js(file_js_path):
    subprocess.Popen(["node", file_js_path])

def stop_server():
    os.system("kill -9 $(lsof -t -i:5000)")
    print("Server stopped")

def get_auto_review_config(submission_path):
    with open(os.path.join(submission_path, "auto-review-config.json"), 'r') as file:
        config = json.load(file)
    return config

def unhandled_exception(err):
    stop_server()
    raise err
