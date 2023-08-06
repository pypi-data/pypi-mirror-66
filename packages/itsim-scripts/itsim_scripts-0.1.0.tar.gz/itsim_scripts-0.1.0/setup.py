from setuptools import setup, find_packages
from pipenv.project import Project
from pathlib import Path


# https://github.com/pypa/sampleproject/blob/master/setup.py
# https://packaging.python.org/guides/distributing-packages-using-setuptools


# taken from https://github.com/gsemet/pipenv-to-requirements/blob/master/pipenv_to_requirements/__init__.py
def pkg_clean_version(pkg_name, pkg_info):
    if isinstance(pkg_info, str):
        if pkg_info.strip() == "*":
            return pkg_name
        return "{}{}".format(pkg_name, pkg_info)
    if not pkg_info:
        return pkg_name
    version = pkg_info.get("version", "").strip()
    editable = pkg_info.get("editable", False)
    markers = pkg_info["markers"].strip() if pkg_info.get("markers") else ""
    extras = pkg_info.get("extras", [])
    subdir = pkg_info.get("subdirectory", [])
    git = pkg_info.get("git", "").strip()
    path = pkg_info.get("path", "").strip()
    ref = pkg_info.get("ref", "").strip()
    rstr = ""
    if not editable:
        rstr += pkg_name
    if extras:
        rstr += "[{}]".format(', '.join([s.strip() for s in extras]))
    if not editable:
        if version and version != "*":
            rstr += version.strip()
    elif git:
        ref = "@" + ref if ref else ref
        rstr = "-e git+" + git + ref + "#egg=" + pkg_name
        if subdir:
            rstr += '&subdirectory=' + subdir
    else:
        rstr = "-e " + path
    if markers:
        rstr += " ; " + markers
    return rstr


def parse_pip_file(pipfile, section):
    return [pkg_clean_version(name, info) for name, info in pipfile.get(section, {}).items()]


requirements = parse_pip_file(Project()._lockfile, 'default')


setup(
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    package_data={
        'itsim_scripts': ['*.json'],
    },
    include_package_data=True,
    install_requires=requirements,
    scripts=['src/' + s for s in (
        'check_layer_data',
        'create_json_project',
        'gtfs_date_choice',
        'gtfs_to_geojson',
        'merge_and_inject_route_color',
        'shp2geojson',
        'simplify_shapefile',
        'simplify_shapes_routes',
        'split_gtfs',
    )],
    data_files=[
        ('bash', [str(p) for p in Path('src/bash/').rglob('*') if not p.is_dir()]),
        ('node_modules', [str(p) for p in Path('src/node_modules/').rglob('*') if not p.is_dir()]),
    ],
)
