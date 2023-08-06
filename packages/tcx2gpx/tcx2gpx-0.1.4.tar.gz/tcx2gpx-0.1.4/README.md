# tcx2gpx


This module converts the Garmin [tcx](https://en.wikipedia.org/wiki/Training_Center_XML) GPS file format
to the more commonly used [gpx](https://en.wikipedia.org/wiki/GPS_Exchange_Format) file format.
Both formats are a form of [XML](https://en.wikipedia.org/wiki/XML) but there are some fields in the former that are not present in the later.
It uses two packages to do the grunt work [tcxparser](https://github.com/vkurup/python-tcxparser/) and
[gpxpy](https://github.com/tkrajina/gpxpy).

## Installation

```bash
git clone
cd
pip install .
```

## Usage

### Single file conversion

For convenience the `convert()` method runs all steps...

```python
from tcx2gpx import TCX2GPX

gps_object = tcx2gpx.TCX2GPX(tcx_path='file_to_convert.tcx')
gps_object.convert()
```

If you want to run the steps manually...

```python
gps_object.read_tcx
gps_object.extract_track_points()
gps_object.create_gpx()
gps_object.write_gpx()
```

If you wish to access individual features then these are simply the `@properties` or methods of
[`tcxparser`](https://github.com/vkurup/python-tcxparser/), for example...

```python
gps_object.tcx.activity_type
'running'
```

### Batch conversion

Often you will have many files you wish to convert, a convenience wrapper is provided.  You specify the
`--directory` that contains the files and they will be converted.  It runs jobs in parallel and the number
of jobs to be run concurrently can be specified with the `-j` flag.

```bash
python ./batch_convert.py --directory ~/my_tcx_workouts/ -j 6
```
