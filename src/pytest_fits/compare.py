from astropy.io import fits
from astropy.io.fits.diff import FITSDiff, HeaderDiff, ImageDataDiff

def pruebas_varias():

    # from subprocess import Popen, PIPE
    # resultado = Popen(["fitsdiff", "-k", "filename,filtnam1,NUM-BS,NUM-OVPE,NUM-TRIM", "-n 1", "-d 1.e-1", "arc_rss.fits", "cArcCalibrationRecipe_arc_rss.fits" ], stdout=PIPE, stderr=PIPE)
    # if "Data contains differences" in resultado.stdout.read():
    #     print "Hay Diferencias"
    # else:
    #     print "Son iguales"


    # print "*" * 40

    # ejemplo = FITSDiff( "arc_rss.fits", "cArcCalibrationRecipe_arc_rss.fits",["filename","filtnam1","NUM-BS","NUM-OVPE","NUM-TRIM"])
    ejemplo = FITSDiff( "arc_rss.fits", "cArcCalibrationRecipe_arc_rss.fits",["NUM-BS","NUM-OVPE"])
    print ejemplo.report()
    if "Data contains differences" in ejemplo.report():
        print "Hay Diferencias"
    else:
        print "Son iguales"


    print "*" * 40
    # hd = HeaderDiff.fromdiff(ejemplo, "arc_rss.fits", "cArcCalibrationRecipe_arc_rss.fits")
    hd = HeaderDiff.fromdiff(ejemplo, "arc_image.fits", "cArcCalibrationRecipe_arc_rss.fits")
    print "Cabeceras identicas: ", hd.identical



def test_identical_number_keywords_headers(file1, file2):
    hdulist1 = fits.open(file1)
    header1 = hdulist1[0].header
    hdulist2 = fits.open(file2)
    header2 = hdulist2[0].header
    diff = HeaderDiff(header1, header2)
    assert diff.diff_keyword_count[0] == diff.diff_keyword_count[1]


def test_different_keyword_values(file1, file2):
    hdulist1 = fits.open(file1)
    header1 = hdulist1[0].header
    hdulist2 = fits.open(file2)
    header2 = hdulist2[0].header
    diff = HeaderDiff(header1, header2)
    assert not diff.identical


def test_data_images(file1, file2):
    hdulist1 = fits.open(file1)
    hdulist2 = fits.open(file2)
    diff = ImageDataDiff(hdulist1[0].data, hdulist2[0].data)
    assert diff.identical

def test_same_data_different_header(file1,file2, tolerance):
    hdulist1 = fits.open(file1)
    hdulist2 = fits.open(file2)

    header1 = hdulist1[0].header
    header2 = hdulist2[0].header
    header = HeaderDiff(header1, header2)
    assert not header.identical
    data = ImageDataDiff(hdulist1[0].data, hdulist2[0].data, tolerance=tolerance)
    assert data.identical



# test_identical_number_keywords_headers('arc_rss.fits','cArcCalibrationRecipe_arc_rss.fits')
test_different_keyword_values('arc_image.fits','cArcCalibrationRecipe_arc_rss.fits')
test_data_images('arc_rss.fits','cArcCalibrationRecipe_arc_rss.fits')
test_same_data_different_header('arc_image.fits','cArcCalibrationRecipe_arc_rss.fits')
