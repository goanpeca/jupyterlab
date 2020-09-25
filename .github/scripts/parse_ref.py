# Standard library imports
import os
import sys


def parse_ref(current_ref):
    if not current_ref.startswith("ref/tags/"):
        raise Exception(f"Invalid ref `{current_ref}`!")

    tag_name = current_ref.replace("ref/tags/", "")

    if tag_name.startswith("@release-") and tag_name.count("-") == 2:
        _, release_branch, bumpversion_type = tag_name.split("-")
        # FIXME: Need to handle the patch case?
        print(f"::set-env name=JLAB_REL_BRANCH::{release_branch}")
        print(f"::set-env name=BUMP2VERSION_RELEASE_TYPE::{bumpversion_type}")


if __name__ == "__main__":
    current_ref = os.environ.get("GITHUB_REF")

    # FIXME: For testing on CI
    current_ref = "ref/tags/@release-master-minor"

    parse_ref(current_ref)
