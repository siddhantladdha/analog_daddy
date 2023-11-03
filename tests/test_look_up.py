import unittest
import numpy as np
from analog_daddy.look_up import look_up

class NMOSTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        z = np.load('sample_files/GPDK45.npy', allow_pickle=True).item()
        cls.nmos_svt = z['nmos_svt']
        cls.pmos_svt = z['pmos_svt']

    def test_nmos_cgg_1(self):
        result = self.nmos_svt['cgg'][0][0][0][0]
        self.assertAlmostEqualPercent(result, 53.26e-15)

    def test_nmos_cgg_2(self):
        result = self.nmos_svt['cgg'][3][0][1][1]
        self.assertAlmostEqualPercent(result, 64.51e-15)

    def test_lookup_nmos_cgg_1(self):
        # single point lookup in mode 1
        result = look_up(self.nmos_svt, 'cgg', length=1e-06, gs=0, ds=0, sb=0)
        self.assertAlmostEqualPercent(result, 53.26e-15)

    def test_lookup_nmos_cgg_2(self):
        # multiple point lookup vsb dimension in mode 1
        result = look_up(self.nmos_svt, 'cgg', length=1e-06, gs=0, ds=0, sb=[0, 0.25])
        self.assertAlmostEqualPercent(result, [53.26e-15, 45.83e-15])

    def test_lookup_nmos_cgg_3(self):
        # average lookup to check interpolation linearity in mode 1
        result = look_up(self.nmos_svt, 'cgg', length=1e-06, gs=0, ds=0, sb=0.125)
        self.assertAlmostEqualPercent(result, 49.55e-15)

    def test_lookup_nmos_gm_id_1(self):
        # single point lookup mode 2
        result = look_up(self.nmos_svt, 'gm_id', length=1e-06, gs=0.9, ds=0.3, sb=0.5)
        self.assertAlmostEqualPercent(result, 3.405)

    def test_lookup_nmos_gm_id_2(self):
        # multiple point lookup vsb dimension, mode 2
        result = look_up(self.nmos_svt, 'gm_id', length=1e-06, gs=0.9, ds=0.3, sb=[0.25, 0.5])
        self.assertAlmostEqualPercent(result, np.array([3.14, 3.405]))

    def test_lookup_nmos_gm_id_3(self):
        # average lookup to check interpolation linearity in mode 2
        result = look_up(self.nmos_svt, 'gm_id', length=1e-06, gs=0.9, ds=0.3, sb=0.375)
        self.assertAlmostEqualPercent(result, 3.273)

    def assertAlmostEqualPercent(self, a, b, percent=1):
        """Assert that `a` and `b` are equal within a certain percentage."""
        # Convert inputs to numpy arrays for consistency
        a, b = np.asarray(a), np.asarray(b)
        
        # Ensure shapes match
        self.assertEqual(a.shape, b.shape, msg="Shapes of arrays do not match.")

        # Compute the delta and tolerance arrays
        delta = np.abs(a - b)
        tolerance = (np.abs(a) + np.abs(b)) / 2.0 * (percent / 100.0)
        
        # Assert that all differences are within the tolerance
        self.assertTrue(np.all(delta <= tolerance), msg=f"Arrays differ by more than {percent}%")
