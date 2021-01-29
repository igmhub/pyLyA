"""This file contains tests related to Mask and its childs"""
import os
import unittest
import numpy as np

from picca.delta_extraction.errors import MaskError
from picca.delta_extraction.mask import Mask

from picca.delta_extraction.masks.sdss_dla_mask import SdssDlaMask
from picca.delta_extraction.masks.sdss_absorber_mask import SdssAbsorberMask
from picca.delta_extraction.userprint import UserPrint

from picca.delta_extraction.tests.abstract_test import AbstractTest
from picca.delta_extraction.tests.test_utils import forest1_log_lambda, forest1
from picca.delta_extraction.tests.test_utils import forest2_log_lambda, forest2
from picca.delta_extraction.tests.test_utils import forest3_log_lambda, forest3

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

class TestMask(AbstractTest):
    """Test the configuration."""

    def test_mask(self):
        """Tests Abstract class Mask

        Load a Mask instace and check that method apply_mask is not initialized.
        """
        with self.assertRaises(MaskError):
            mask = Mask()

            # run apply_correction, this should raise MaskError
            mask.apply_mask(forest1)

    def test_dla_mask(self):
        """Tests correct initialisation and inheritance for class
        SdssDlaMask

        Load a SdssDlaMask instace and check that it is
        correctly initialized.
        """
        in_file = f"{THIS_DIR}/data/dummy_absorbers_cat.fits.gz"
        out_file = f"{THIS_DIR}/results/sdss_dla_mask_print.txt"
        test_file = f"{THIS_DIR}/data/sdss_dla_mask_print.txt"

        # setup printing
        UserPrint.initialize_log(out_file)

        # initialize mask
        mask = SdssDlaMask({"dla catalogue": in_file})
        self.assertTrue(isinstance(mask, Mask))
        self.compare_ascii(test_file, out_file, expand_dir=True)

        # reset printing
        UserPrint.reset_log()

        # apply mask to forest with 1 DLA
        mask.apply_mask(forest1)
        # TODO: check that the profile is correct

        # apply mask to forest with 2 DLAs
        mask.apply_mask(forest2)
        # TODO: check that the profile is correct

        # apply mask to forest without DLAs
        mask.apply_mask(forest3)
        self.assertTrue(np.allclose(forest3.flux, np.ones_like(forest3_log_lambda)))
        self.assertTrue(np.allclose(forest3.log_lambda, forest3_log_lambda))
        self.assertTrue(np.allclose(forest3.ivar, np.ones_like(forest3_log_lambda)*4))
        self.assertTrue(np.allclose(forest3.transmission_correction,
                                    np.ones_like(forest3_log_lambda)))

    def test_absorber_mask(self):
        """Tests correct initialisation and inheritance for class
        SdssAbsorberMask

        Load a SdssAbsorberMask instace and check that it is
        correctly initialized.
        """
        in_file = f"{THIS_DIR}/data/dummy_absorbers_cat.fits.gz"
        out_file = f"{THIS_DIR}/results/sdss_absorber_mask_print.txt"
        test_file = f"{THIS_DIR}/data/sdss_absorber_mask_print.txt"

        # setup printing
        UserPrint.initialize_log(out_file)

        # initialize mask
        mask = SdssAbsorberMask({"absorbers catalogue": in_file})
        self.assertTrue(isinstance(mask, Mask))
        self.compare_ascii(test_file, out_file, expand_dir=True)

        # reset printing
        UserPrint.reset_log()

        # apply mask to forest with 1 absorber
        mask.apply_mask(forest1)

        w = np.ones(forest1_log_lambda.size, dtype=bool)
        w &= np.fabs(1.e4 * (forest1_log_lambda - np.log10(5600))) > 2.5
        self.assertTrue(np.allclose(forest1.flux, np.ones_like(forest1_log_lambda[w])))
        self.assertTrue(np.allclose(forest1.log_lambda, forest1_log_lambda[w]))
        self.assertTrue(np.allclose(forest1.ivar, np.ones_like(forest1_log_lambda[w])*4))
        self.assertTrue(np.allclose(forest1.transmission_correction,
                                    np.ones_like(forest1_log_lambda[w])))

        # apply mask to forest with 2 absorbers
        mask.apply_mask(forest2)

        w = np.ones(forest2_log_lambda.size, dtype=bool)
        w &= np.fabs(1.e4 * (forest2_log_lambda - np.log10(5600))) > 2.5
        w &= np.fabs(1.e4 * (forest2_log_lambda - np.log10(5650))) > 2.5
        self.assertTrue(np.allclose(forest2.flux, np.ones_like(forest2_log_lambda[w])))
        self.assertTrue(np.allclose(forest2.log_lambda, forest2_log_lambda[w]))
        self.assertTrue(np.allclose(forest2.ivar, np.ones_like(forest2_log_lambda[w])*4))
        self.assertTrue(np.allclose(forest2.transmission_correction,
                                    np.ones_like(forest2_log_lambda[w])))

        # apply mask to forest without absorbers
        mask.apply_mask(forest3)
        self.assertTrue(np.allclose(forest2.flux, np.ones_like(forest3_log_lambda)))
        self.assertTrue(np.allclose(forest2.log_lambda, forest3_log_lambda))
        self.assertTrue(np.allclose(forest2.ivar, np.ones_like(forest3_log_lambda)*4))
        self.assertTrue(np.allclose(forest2.transmission_correction,
                                    np.ones_like(forest3_log_lambda)))



if __name__ == '__main__':
    unittest.main()