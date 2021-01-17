"""
GitInfo Class
"""


class GitInfo:
    """
    Information about git properties
    """

    def __init__(self, remote_url, branch):
        self.remote_name = "origin-new-repo"
        self.remote_url = remote_url
        self.branch = branch

    def create_new_branch_cmd(self):
        return f"git branch -D {self.branch}; git checkout -b {self.branch}"

    def add_new_remote_cmd(self):
        return f"git remote add {self.remote_name} {self.remote_url}"

    def remove_new_remote_cmd(self):
        return f"git remote remove {self.remote_name}"

    def push_branch_to_remote_cmd(self):
        return f"git push {self.remote_name} {self.branch} --force"
