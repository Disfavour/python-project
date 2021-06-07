import glob
from doit.tools import create_folder

# DOIT_CONFIG = {'default_tasks': ['all']}


def task_clean_docs():
    """Clean docs."""
    return {
        'actions': ['rm -rf docs/*'],
    }


def task_docs():
    """Generate new docs."""
    return {
        'actions': ['sphinx-build -d html docs_src/ docs/', 'rm -rf html'],
        'task_dep': ['clean_docs'],
    }

