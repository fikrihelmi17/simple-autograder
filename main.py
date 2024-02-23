#! /usr/bin/env python3

import re
import time
import socket
import http.client
from checklist import Checklist, Checklists
from reporter import generate_report
from utils import find_file, get_params, run_npm_install, run_main_js, get_auto_review_config, stop_server
from utils import unhandled_exception

def new_checklists():
    return Checklists()

def get_project_path(submission_path):
    try:
        package_json_path, _ = find_file(submission_path, "package.json")
        
        if package_json_path is None:
            return None, Checklist(status=False, comment="Kami tidak bisa menemukan file package.json pada submission yang kamu kirimkan")
        
        project_path = package_json_path.replace("/package.json", "", 1)

        return project_path, Checklist(status=True)
    
    except Exception as e:
        unhandled_exception(e)

def get_main_js(submission_path):
    try:
        main_js_path, _ = find_file(submission_path, "main.js")

        if main_js_path is None:
            return None, Checklist(status=False, comment="Kami tidak bisa menemukan file main.json pada submission yang kamu kirimkan")
        
        return main_js_path, Checklist(status=True)
    
    except Exception as e:
        unhandled_exception(e)

def check_comment_in_main_js(student_id, file_js_path):
    try:
        with open(file_js_path, 'r') as file:
            code = file.read()

        match_string = re.search("//.*" + str(student_id) + "|/\\*.*" + str(student_id), code)

        if match_string:
            return Checklist(status=True)
        
        return Checklist(comment="Kami tidak bisa menemukan user id " + str(student_id) + " pada file main.js")
    
    except Exception as e:
        unhandled_exception(e)

def root_is_serving_html():
    conn = http.client.HTTPConnection("localhost", 5000, timeout=3)

    try:
        conn.request("GET", "/")
        response = conn.getresponse()
        content_type = response.getheader("Content-Type")
        if "html" not in content_type:
            return None, Checklist(status=True, comment="Content yang berada pada root bukanlah html, melainkan " + content_type)
        html = response.read().decode()
        return html, Checklist(status=True)
    except Exception as e:
        return None, Checklist(status=False, comment="Kami tidak bisa mendeteksi port 5000 setelah aplikasi dijalankan, mohon periksa kembali apakah port yang kamu gunakan adalah 5000")

def h1_element_is_correct(student_id, html):
    compile_regex = re.compile("<h1>" + str(student_id) + "</h1>")
    element_is_correct = compile_regex.search(html)
    if element_is_correct:
        return Checklist(status=True)
    return Checklist(comment="Kami tidak bisa menemukan user id " + str(student_id) + " di url root pada aplikasi yang kamu buat")

def wait_until_server_up():
    host = "localhost"
    port = 5000
    timeout = 3

    i = 0
    start = time.time()
    while True:
        if i % 10 == 0:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.settimeout(timeout)
            result = conn.connect_ex((host, port))

            if result == 0:
                conn.close()
                print("Port 5000 is running")
                return Checklist(status=True)

            if time.time() - start > timeout:
                print("Port is not running")
                return Checklist(status=False, comment="Kami tidak bisa mendeteksi port 5000 setelah aplikasi dijalankan, mohon periksa kembali apakah port yang kamu gunakan adalah 5000")
        i += 1


def main():
    submission_path, report_path = get_params()

    c = new_checklists()
    
    project_path, c.packageJsonExists = get_project_path(submission_path)

    file_js_path, c.mainJsExists = get_main_js(submission_path)
    
    if project_path:
        run_npm_install(project_path)
        
        if file_js_path:
            run_main_js(file_js_path)

            c.serveInPort5000 = wait_until_server_up()
            
            if c.serveInPort5000.status:
                html, c.rootShowingHtml = root_is_serving_html()
                if html:
                    c.htmlContainH1ElementWithStudentId = h1_element_is_correct(get_auto_review_config(submission_path)["submitter_id"], html)
    
    if file_js_path:
        c.mainJsHaveStudentIdComment = check_comment_in_main_js(get_auto_review_config(submission_path)["submitter_id"], file_js_path)
    
    stop_server()
    generate_report(c, report_path, get_auto_review_config(submission_path)["submitter_name"])

if __name__ == "__main__":
    main()
