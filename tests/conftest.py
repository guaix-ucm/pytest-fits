from functools import wraps
import shutil
import tempfile

import os
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('fits', 'Fits comparison')
    group.addoption('--runtest', action='store_true',
                    help="Enable comparison of fits images")
    group.addoption('--generate-images',
                    help="directory to generate reference images in, relative to location where py.test is run",
                    action='store')
    group.addoption('--define-path',
                    help="directory containing baseline images, relative to location where py.test is run",
                    action='store')


def pytest_configure(config):
    if config.getoption("--generate-images") is not None:
        if config.getoption("--define-path") is not None:
            raise ValueError(
                "Can't set --define-path when generating reference images with --generate-path")

    if config.getoption("--runtest") or config.getoption(
            "--generate-images") is not None:

        baseline_dir = config.getoption("--define-path")
        generate_dir = config.getoption("--generate-images")

        if baseline_dir is not None:
            baseline_dir = os.path.abspath(baseline_dir)
        if generate_dir is not None:
            baseline_dir = os.path.abspath(generate_dir)
        config.pluginmanager.register(
            ImageComparison(config, baseline_dir=baseline_dir,
                            generate_dir=generate_dir))


class ImageComparison(object):
    def __init__(self, config, baseline_dir=None, generate_dir=None):
        self.config = config
        self.baseline_dir = baseline_dir
        self.generate_dir = generate_dir

    def _fits_comparison(self, file1, file2, tolerance):
        from astropy.io import fits
        from astropy.io.fits.diff import ImageDataDiff

        hdulist1 = fits.open(file1)
        hdulist2 = fits.open(file2)

        data = ImageDataDiff(hdulist1[0].data, hdulist2[0].data,
                             tolerance=tolerance)
        assert data.identical

    def pytest_runtest_setup(self, item):
        compare = item.keywords.get('fits_image_compare')

        if compare is None:
            return

        tolerance = compare.kwargs.get('tolerance', 2)
        original = item.function

        @wraps(item.function)
        def item_function_wrapper(*args, **kwargs):
            import inspect

            baseline_dir = compare.kwargs.get('baseline_dir', None)

            if baseline_dir is None:
                if self.baseline_dir is None:
                    baseline_dir = os.path.join(
                        os.path.dirname(item.fspath.strpath), 'baseline')
                else:
                    baseline_dir = self.baseline_dir
            else:
                baseline_dir = os.path.join(
                    os.path.dirname(item.fspath.strpath), baseline_dir)

            if inspect.ismethod(original):
                fig = original(*args[1:], **kwargs)
            else:  # function
                fig = original(*args, **kwargs)

            # Find test name to use as plot name
            filename = compare.kwargs.get('filename', None)
            if filename is None:
                filename = inspect.getmodule(original).__name__ +'_' + original.__name__ + '.fits'

            # What we do now depends on whether we are generating the reference
            # images or simply running the test.
            if self.generate_dir is None:

                # Save the figure
                result_dir = tempfile.mkdtemp()
                test_image = os.path.abspath(
                    os.path.join(result_dir, filename))

                fig.writeto(test_image, clobber=True)

                # Find path to baseline image
                baseline_image_ref = os.path.abspath(
                    os.path.join(os.path.dirname(item.fspath.strpath),
                                 baseline_dir, filename))

                if not os.path.exists(baseline_image_ref):
                    raise Exception("""Image file not found for comparison test
                                    Generated Image:
                                    \t{test}
                                    This is expected for new tests.""".format(
                        test=test_image))

                # distutils may put the baseline images in non-accessible places,
                # copy to our tmpdir to be sure to keep them in case of failure
                baseline_image = os.path.abspath(
                    os.path.join(result_dir, 'baseline-' + filename))
                shutil.copyfile(baseline_image_ref, baseline_image)

                self._fits_comparison(baseline_image, test_image, tolerance)

            else:

                if not os.path.exists(self.generate_dir):
                    os.makedirs(self.generate_dir)

                fig.writeto(
                    os.path.abspath(os.path.join(self.generate_dir, filename)),
                    clobber=True)
                pytest.skip("Skipping test, since generating data")

        # Cuando es una funcion o es una clase
        if item.cls is not None:
            setattr(item.cls, item.function.__name__, item_function_wrapper)
        else:
            item.obj = item_function_wrapper
