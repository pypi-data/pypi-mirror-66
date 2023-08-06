"""
tcx2gpx setup
"""
import setuptools

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()
setuptools.setup(use_scm_version=True,
                 description='Convert Garmin TPX to GPX',
                 long_description=LONG_DESCRIPTION,
                 long_description_content_type='text/markdown')
