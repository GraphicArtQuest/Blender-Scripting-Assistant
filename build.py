import os

from src.bundler import bundle

if __name__ == '__main__':
    project_dir = os.path.abspath(__file__)
    src_dir = os.path.join(os.path.dirname(project_dir), "src")
    dist_dir = os.path.join(os.path.dirname(project_dir), "dist")

    bundle(
        source_files=[src_dir], 
        output_folder=dist_dir, 
        name="blender-scripting-assistant", 
        overwrite=True)
