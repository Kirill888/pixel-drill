from .pprio import ParallelReader


def make_pixel_extractor(mode='pixel',
                         band=1,
                         remap_nodata=None,
                         output_nodata=None,
                         nodata=None):
    if nodata is not None:
        def _nodata(f, band):
            return nodata
    else:
        def _nodata(f, band):
            return f.nodatavals[band-1]

    if remap_nodata:
        def remap_pix(pix, f, band):
            if pix == _nodata(f, band):
                return output_nodata
            return pix

        def out_of_bounds_pix(f, band):
            return output_nodata
    else:
        def remap_pix(pix, *_):
            return pix

        def out_of_bounds_pix(f, band):
            return f.nodatavals[band-1]

    default_band = band

    def extract_pixel(f, pixel_coordinate, band=default_band):
        ri, ci = pixel_coordinate

        if 0 <= ri < f.height and 0 <= ci < f.width:
            window = ((ri, ri+1),
                      (ci, ci+1))

            pix = f.read(band, window=window)
            return remap_pix(pix[0][0], f, band)
        else:
            return out_of_bounds_pix(f, band)

    def extract_native(f, xy, band=default_band):
        return extract_pixel(f, f.index(*xy))

    extractors = dict(pixel=extract_pixel,
                      native=extract_native)

    extractor = extractors.get(mode)
    if extractor is None:
        raise ValueError('Only support mode=<pixel|native>')

    return extractor


class PixelDrill(object):
    def __init__(self,
                 nthreads,
                 region_name=None):
        self._proc = ParallelReader(nthreads,
                                    region_name=region_name)

    def read(self, urls, pixel=None, xy=None, band=1, **kwargs):
        if pixel is None and xy is None:
            raise ValueError('Have to specify one of pixel or xy')

        if pixel is not None:
            mode, coord = 'pixel', pixel
        else:
            mode, coord = 'native', xy

        extractor = make_pixel_extractor(mode=mode, band=band, **kwargs)

        out = [None]*len(urls)

        def cbk(f, userdata):
            idx, coord = userdata
            out[idx] = extractor(f, coord)

        self._proc.process((((idx, coord), url) for idx, url in enumerate(urls)),
                           cbk)

        return out
