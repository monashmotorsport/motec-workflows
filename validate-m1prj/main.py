"""
Validate a MoTeC .m1prj
=======================

Validate a MoTeC .m1prj XML file against the provided XML schema.

Usage
-----
>>> python validate_m1prj path/to/Project.m1prj

Requirements
------------
- lxml: `pip install lxml`
"""

import os
import sys
import glob
import argparse

# Set python path to include the action directory for imports
action_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(action_dir)

if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from typing import Optional
from util import load_schema, validate, load_xml


def get_version(path: str) -> Optional[str]:
    """Extract the version from the XML document."""
    doc = load_xml(path)
    version = doc.xpath("/MoTeCM1BuildSession/@ProductVersion")
    return version[0] if version else None


def check_help_tag(path: str) -> int:
    """Check for the presence of a self-closing <Help/> tag in the XML document.
    These corrupt the MoTeC build file if you are using build 1.4 or earlier
    """

    doc = load_xml(path)
    help_tags = doc.xpath("//Help[not(node())]")
    if help_tags:
        print("INVALID: Self-closing <Help/> tag found in the project file.")
        return 1
    return 0


def check_comment_tag(path: str) -> int:
    """Check for the presence of a self-closing <Comment/> tag in the XML document.
    These corrupt the MoTeC build file if you are using build 1.4 or earlier
    """

    doc = load_xml(path)
    comment_tags = doc.xpath("//Comment[not(node())]")
    if comment_tags:
        print("INVALID: Self-closing <Comment/> tag found in the project file.")
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate MoTeC .m1prj files")
    parser.add_argument(
        "path", help="Path or glob pattern for .m1prj files to validate"
    )
    args = parser.parse_args()

    schema_path = os.path.join(os.path.dirname(__file__), "../schemas/m1prj.xsd")

    schema = load_schema(schema_path)
    exit_code = 0

    for path in glob.glob(args.path):
        exit_code |= validate(path, schema)

        # Check for self-closing tags, if version is earlier than 1.5
        version = get_version(path)
        if version and version < "1.5":
            exit_code |= check_help_tag(path)
            exit_code |= check_comment_tag(path)

    sys.exit(exit_code)
