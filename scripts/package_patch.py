
from pathlib import Path
import os
import argparse
import re
import shutil
import tempfile

'''
Reads a pure data patch file and builds a dependency list of all the abstractions
so that they can all be bundled together in one zipped directory
'''

ROOT_PATH = Path(__file__).parent.parent
OUTPUT_DIR = os.path.join(ROOT_PATH, "releases")

DEPENDENCY_DIRECTORIES = [
    "effects", "synths", "utils"
]

def get_dependency_map():
    '''
    Trawls the directory locations to generate a list of all possible dependencies a patch may have 

    Returns a map where key is the dependency name (without extension) and value is the disk path
    '''

    dependency_map = {}

    for dir_name in DEPENDENCY_DIRECTORIES:
        for path, _, filenames in os.walk(os.path.join(ROOT_PATH, dir_name)):
            for filename in filenames:
                dependency_map[os.path.splitext(filename)[0]] = os.path.join(path, filename)

    return dependency_map



def get_patch_dependencies(patch_path):
    '''
    Returns a set of files which are dependencies of the patch
    '''

    dependencies_map = get_dependency_map()
    patch_depedencies = set()

    with open(patch_path, 'r') as patch:
        # go through line by line and find the dependencies
        # TODO: Only search lines beginnig with obj
        for line in patch:
            for dependency in dependencies_map:
                if re.search(dependency, line):
                        patch_depedencies.add(dependencies_map[dependency])

    return patch_depedencies


def get_patch_version(patch_path):
    '''
    Parse the patch text file for a version string
    '''

    with open(patch_path, 'r') as patch:
        for line in patch:
            m = re.search('v\d+.\d+', line)
            if m:
                return m.group(0)
            
    return ""


def package_patch(patch_path):
    '''
    Collects dependencies of a patch and zips them all together
    '''

    dependencies = get_patch_dependencies(patch_path)
    
    # Get all recursive dependencies
    for dependency in dependencies:
        dependencies = dependencies.union(get_patch_dependencies(dependency))

    print(dependencies)
    version = get_patch_version(patch_path)
    package_name = os.path.splitext(os.path.basename(patch_path))[0]

    if version != "":
        package_name += "_{}".format(version)

    zip_dir = tempfile.mkdtemp()

    try:
        shutil.copy(patch_path, zip_dir)
        [shutil.copy(dep, zip_dir) for dep in dependencies]
        
        shutil.make_archive(os.path.join(OUTPUT_DIR, package_name), format="zip", root_dir=zip_dir)
    finally:
        shutil.rmtree(zip_dir)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Package up a Pd patch and its dependencies into a zip file')
    parser.add_argument('path',  help="path to the patch to package", type=Path)
    args = parser.parse_args()

    patch_path = os.path.abspath(args.path)
    package_patch(patch_path)