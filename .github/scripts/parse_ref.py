# Standard library imports
import os
import subprocess
import sys

# Constants
HERE = os.path.abspath(os.path.dirname(__file__))
REPO_ROOT = os.path.dirname(os.path.dirname(HERE))


def get_valid_branches():
    p = subprocess.Popen(
        ["git", "branch"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=REPO_ROOT,
    )
    stdout, stderr = p.communicate()
    stdout = stdout.decode()
    branches = [line.split()[-1] for line in stdout.split("\n") if line]
    return branches


def parse_ref(current_ref):
    if not current_ref.startswith("ref/tags/"):
        raise Exception(f"Invalid ref `{current_ref}`!")

    valid_bum2version_type = ["major", "minor", "patch", "release", "build"]
    valid_branches = get_valid_branches()
    tag_name = current_ref.replace("ref/tags/", "")

    if tag_name.startswith("@release-") and tag_name.count("-") == 2:
        _, release_branch, bumpversion_type = tag_name.split("-")

        # Check `bumpversion_type` is valid
        if bumpversion_type not in valid_bum2version_type:
            print(
                f"\nBum2version type '{bumpversion_type}' is invalid!\n"
                f"Valid types are: {valid_bum2version_type}\n"
            )
            sys.exit(1)

        # Check `release_branch` is valid
        if release_branch not in valid_branches:
            print(
                f"\nRelease branch '{release_branch}' is invalid!\n"
                f"Valid branches are: {valid_branches}\n"
            )
            sys.exit(1)

        # FIXME: Need to handle the patch case?
        print(f"::set-env name=JLAB_RELEASE_BRANCH::{release_branch}")
        print(f"::set-env name=BUMP2VERSION_RELEASE_TYPE::{bumpversion_type}")


if __name__ == "__main__":
    current_ref = os.environ.get("GITHUB_REF")

    # FIXME: For testing on CI
    current_ref = "ref/tags/@release-master-build"

    get_valid_branches()
    parse_ref(current_ref)
