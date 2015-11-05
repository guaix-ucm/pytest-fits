import pytest

@pytest.mark.fits_image_compare
def test_succeeds():
    import numpy as np
    from astropy.io import fits

    n = np.arange(50.0)
    hdu = fits.PrimaryHDU(n)
    fig = fits.HDUList([hdu])
    return fig


@pytest.mark.fits_image_compare
def test_error():
    import numpy as np
    from astropy.io import fits

    n = np.arange(100.0)
    hdu = fits.PrimaryHDU(n)
    fig = fits.HDUList([hdu])
    return fig