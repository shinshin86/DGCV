# -*- coding: utf-8 -*-
from git import *
import time
import subprocess
import os

"""Find a this day's the last commit.
    
Args:
    item - git commit's data

Returns:
    this day in last commit data

"""
def find_last_commit_time(items):
    commit_day = []
    commit_time = []
    uniq_commit_days = {}
    uniq_commit_data = {}
    for item in items:
        commit_time = str(time.strftime("%Y%m%d%H%M%S", time.gmtime(item.committed_date)))
        if((commit_time[0:8] in uniq_commit_days)== False):
            uniq_commit_days[commit_time[0:8]] = commit_time
        
        # If this is a latest date, then update to date.
        if(uniq_commit_days[commit_time[0:8]] <= commit_time):
            uniq_commit_days[commit_time[0:8]] = commit_time
            uniq_commit_data[uniq_commit_days[commit_time[0:8]]] = item.hexsha

    return uniq_commit_data

"""Checkout and Copy
    
Args:
    uniq_commit_data
    repo
    git
    your_repository
    cp_dest_path
    repository_name
    
    """
def checkout_and_copy(uniq_commit_data, repo, git, your_repository, cp_dest_path, repository_name):

    
    for i in uniq_commit_data:
        key = i
        time.sleep(1)
        print("Process to ... " + str(i))
        git.checkout(uniq_commit_data.get(key), b=str(i))
        cp_cmd = "cp -r " + your_repository + " " + cp_dest_path
        subprocess.check_output(cp_cmd.strip().split(" "))
        print("Success Copy : " + str(cp_cmd))
        time.sleep(1)
        mkdir_cmd = "mkdir " + cp_dest_path + "/" + str(i)
        subprocess.check_output(mkdir_cmd.strip().split(" "))
        print("Success mkdir : " + str(mkdir_cmd))
        time.sleep(1)
        mv_cmd = "mv " + cp_dest_path + "/" +  repository_name + " " + cp_dest_path + "/" + str(i)
        subprocess.check_output(mv_cmd.strip().split(" "))
        print("Success Move : " + str(mv_cmd))
        time.sleep(1)
        # Branch change a 'master'
        git.checkout('master')
        # Delete this process's branch
        repo.delete_head(str(i),'-D')
        print("Success create dir : " + str(i))

def main():
    # When using a Absolute path, delete to "os.getcwd()"
    your_repository = os.getcwd() + "/" + "Your Repository(Relative path) is here." # Example : "./test_dir/your_repository"
    cp_dest_path = os.getcwd() + "/" + "Copy destination path(Relative path) is here." # Example : "./test_dir/copy_dest_path"
    repository_name = "repositry name is here" # Example : your_repository  => TODO -> This is a Tentative correspondence.

    repo = Repo(your_repository)
    uniq_commit_days = {}
    uniq_commit_data = find_last_commit_time(repo.iter_commits('master', max_count=100))
    git = repo.git


    print("Daily Git Collection Vehicle start...")

    checkout_and_copy(uniq_commit_data, repo, git, your_repository, cp_dest_path, repository_name)

    print("Daily Git Collection Vehicle end!!")


if __name__ == '__main__':
    main()