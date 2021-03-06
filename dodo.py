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


def task_gitclean():
    """Clean all generated files not tracked by GIT."""
    return {
            'actions': ['git clean -xdf'],
           }


def task_test():
    """Perform tests."""
    return {
            'actions':['python -m unittest tests'],
            }


def task_fill_db():
    """Create and fill tables."""
    return {'actions': ['python3 src/database.py']}
    #yield {'actions': ['python3 src/database.py'], 'name': 'create'}
    #yield {'actions': ['python3 src/recipes_parsing.py'], 'name': 'fill'}


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o localization/telbot.pot src'],
            'file_dep': glob.glob('src/*.py'),
            'targets': ['localization/telbot.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D telbot -d localization -i localization/telbot.pot'],
            'file_dep': ['localization/telbot.pot'],
            'targets': ['localization/en/LC_MESSAGES/telbot.po'],
           }


def task_mo():
    """Compile translations."""
    return {
            'actions': [
                (create_folder, ['src/en/LC_MESSAGES']),
                'pybabel compile -l en -D telbot -d src -i localization/en/LC_MESSAGES/telbot.po'
                       ],
            'file_dep': ['localization/en/LC_MESSAGES/telbot.po'],
            'targets': ['src/en/LC_MESSAGES/telbot.mo'],
           }


def task_build():
    """Create full distribution."""
    return {
            'actions': ['python -m build'],
            'task_dep': ['gitclean', 'mo', 'docs'],
            }


def task_style():
    """Check style against flake8."""
    return {
            'actions': ['flake8 src']
           }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
            'actions': ['pydocstyle src']
           }


def task_check():
    """Perform all checks."""
    return {
            'actions': None,
            'task_dep': ['style', 'docstyle']
           }


def task_all():
    """Perform all build task."""
    return {
            'actions': None,
            'task_dep': ['check', 'mo', 'fill_db'],
            }
