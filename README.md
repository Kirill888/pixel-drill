# pixel-drill

## Installation

```
pip install git+https://github.com/Kirill888/pixel-drill.git
```

## Use

Create pixel drill object once in your app first (you can configure concurrency settings at this point)

```python
from pdrill import PixelDrill
pxd = PixelDrill(nthreads=32)
```

Then use it to load many files concurrently:

```python
pixels = pxd.read(urls, pixel=(2001, 1703))  # row, column in pixel space
## or use native coords (assumes same crs across files)
pixels = pxd.read(urls, xy=(-857425.0, -1750025.0)) # x,y in native CRS of the files
```

See [example notebook](https://github.com/Kirill888/pixel-drill/blob/94f43af69fb9d05eab60e6660587b8f453d296f7/example.ipynb) for more details.

## Other options

- `band` -- 1 based band index (defaults to 1)
- `remap_nodata` -- if `True` replace `nodata` values with `None` or with `output_nodata` if supplied
- `output_nodata` -- value to use instead of `nodata`, defaults to `None`
- `nodata` -- Override `nodata` value of the Tiff file
