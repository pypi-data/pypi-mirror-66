# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 16:57:48 2020

@author: etienne.engel
"""

# Aim :
# Create a log file
# Create a class for unitary test

import unittest
import logging
from Package.SubPackage.calculator import SimpleCalculator


class Test(unittest.TestCase):
    """ Objective: Allow unitary test
                   Fill the log file
    """

    def test_personnal_sum(self):
        """ Objective: Test of personnal_sum's
        basic working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing personnal_sum in basic case")
        job = SimpleCalculator(2, 1)
        res = job.personnal_sum()
        self.assertEqual(res, 3)
        job = SimpleCalculator(1, 2)
        res = job.personnal_sum()
        self.assertEqual(res, 3)
        LOGGER.info("end testing personnal_sum in basic case\n")

    def test_personnal_sum_by_0(self):
        """ Objective: Test of personnal_sum's
        sum by 0 working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing personnal_sum in sum by 0 case")
        job = SimpleCalculator(0, 1)
        res = job.personnal_sum()
        self.assertEqual(res, 1)
        job = SimpleCalculator(1, 0)
        res = job.personnal_sum()
        self.assertEqual(res, 1)
        job = SimpleCalculator(0, 0)
        res = job.personnal_sum()
        self.assertEqual(res, 0)
        LOGGER.info("end testing personnal_sum in sum by 0 case\n")

    def test_personnal_sum_limit(self):
        """ Objective: Test of personnal_sum's
        sum with high numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing personnal_sum in high number case")
        job = SimpleCalculator(1000000, 1000000)
        res = job.personnal_sum()
        self.assertEqual(res, 2000000)
        job = SimpleCalculator(-1000000, 1000000)
        res = job.personnal_sum()
        self.assertEqual(res, 0)
        job = SimpleCalculator(1000000, -1000000)
        res = job.personnal_sum()
        self.assertEqual(res, 0)
        job = SimpleCalculator(-1000000, -1000000)
        res = job.personnal_sum()
        self.assertEqual(res, -2000000)
        LOGGER.info("end testing personnal_sum in high number case\n")

    def test_personnal_sum_negative(self):
        """ Objective: Test of personnal_sum's
        sum with negative numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing personnal_sum in negative number case")
        job = SimpleCalculator(2, -1)
        res = job.personnal_sum()
        self.assertEqual(res, 1)
        job = SimpleCalculator(-1, 2)
        res = job.personnal_sum()
        self.assertEqual(res, 1)
        job = SimpleCalculator(-2, -1)
        res = job.personnal_sum()
        self.assertEqual(res, -3)
        LOGGER.info("end testing personnal_sum in negative number case\n")

    def test_personnal_sum_float(self):
        """ Objective: Test of personnal_sum's
        sum with float numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing personnal_sum in float number case")
        with self.assertRaises(ValueError):
            SimpleCalculator(2, 1.2)
        LOGGER.info("end testing personnal_sum in float number case\n")

    def test_substraction(self):
        """ Objective: Test of substraction's
        substraction basic working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing substraction in basic case")
        job = SimpleCalculator(2, 1)
        res = job.substraction()
        self.assertEqual(res, 1)
        job = SimpleCalculator(1, 2)
        res = job.substraction()
        self.assertEqual(res, -1)
        LOGGER.info("end testing substraction in basic case\n")

    def test_substraction_by_0(self):
        """ Objective: Test of substraction's
        substraction by 0 working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing substraction in substraction by 0 case")
        job = SimpleCalculator(0, 3)
        res = job.substraction()
        self.assertEqual(res, -3)
        job = SimpleCalculator(3, 0)
        res = job.substraction()
        self.assertEqual(res, 3)
        job = SimpleCalculator(0, 0)
        res = job.substraction()
        self.assertEqual(res, 0)
        LOGGER.info("end testing substraction in substraction by 0 case\n")

    def test_substraction_limit(self):
        """ Objective: Test of substraction's
        substraction with high numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing substraction in high number case")
        job = SimpleCalculator(1000000, 1000000)
        res = job.substraction()
        self.assertEqual(res, 0)
        job = SimpleCalculator(-1000000, 1000000)
        res = job.substraction()
        self.assertEqual(res, -2000000)
        job = SimpleCalculator(1000000, -1000000)
        res = job.substraction()
        self.assertEqual(res, 2000000)
        job = SimpleCalculator(-1000000, -1000000)
        res = job.substraction()
        self.assertEqual(res, 0)
        LOGGER.info("end testing substraction in high number case\n")

    def test_substraction_negative(self):
        """ Objective: Test of substraction's
        substraction with negative numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing substraction in negative number case")
        job = SimpleCalculator(2, -1)
        res = job.substraction()
        self.assertEqual(res, 3)
        job = SimpleCalculator(-1, 2)
        res = job.substraction()
        self.assertEqual(res, -3)
        job = SimpleCalculator(-2, -1)
        res = job.substraction()
        self.assertEqual(res, -1)
        LOGGER.info("end testing substraction in negative number case\n")

    def test_substraction_float(self):
        """ Objective: Test of substraction's
        substraction with float numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing substraction in float number case")
        with self.assertRaises(ValueError):
            SimpleCalculator(2, 1.2)
        LOGGER.info("end testing substraction in float number case\n")

    def test_multiplication(self):
        """ Objective: Test of multiplication's
        multiplication basic working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing multiplication in basic case")
        job = SimpleCalculator(2, 1)
        res = job.multiplication()
        self.assertEqual(res, 2)
        job = SimpleCalculator(1, 2)
        res = job.multiplication()
        self.assertEqual(res, 2)
        LOGGER.info("end testing multiplication in basic case\n")

    def test_multiplication_by_0(self):
        """ Objective: Test of multiplication's
        multiplication by 0 working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing multiplication in multiplication by 0 case")
        job = SimpleCalculator(0, 3)
        res = job.multiplication()
        self.assertEqual(res, 0)
        job = SimpleCalculator(3, 0)
        res = job.multiplication()
        self.assertEqual(res, 0)
        job = SimpleCalculator(0, 0)
        res = job.multiplication()
        self.assertEqual(res, 0)
        LOGGER.info("end testing multiplication in multiplication by 0 case\n")

    def test_multiplication_limit(self):
        """ Objective: Test of multiplication's
        multiplication with high numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing multiplication in high number case")
        job = SimpleCalculator(-1000000, 1000000)
        res = job.multiplication()
        self.assertEqual(res, -1000000000000)
        job = SimpleCalculator(1000000, -1000000)
        res = job.multiplication()
        self.assertEqual(res, -1000000000000)
        job = SimpleCalculator(1000000, 1000000)
        res = job.multiplication()
        self.assertEqual(res, 1000000000000)
        job = SimpleCalculator(-1000000, -1000000)
        res = job.multiplication()
        self.assertEqual(res, 1000000000000)
        LOGGER.info("end testing multiplication in high number case\n")

    def test_multiplication_negative(self):
        """ Objective: Test of multiplication's
        multiplication with negative numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing multiplication in negative number case")
        job = SimpleCalculator(2, -1)
        res = job.multiplication()
        self.assertEqual(res, -2)
        job = SimpleCalculator(-1, 2)
        res = job.multiplication()
        self.assertEqual(res, -2)
        job = SimpleCalculator(-2, -1)
        res = job.multiplication()
        self.assertEqual(res, 2)
        LOGGER.info("end testing multiplication in negative number case\n")

    def test_multiplication_float(self):
        """ Objective: Test of multiplication's
        multiplication with float numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing multiplication in float number case")
        with self.assertRaises(ValueError):
            SimpleCalculator(2, 1.2)
        LOGGER.info("end testing multiplication in float number case\n")

    def test_division(self):
        """ Objective: Test of division's
        division basic working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing division in basic case")
        job = SimpleCalculator(2, 1)
        res = job.division()
        self.assertEqual(res, 2)
        job = SimpleCalculator(1, 2)
        res = job.division()
        self.assertEqual(res, 0.5)
        LOGGER.info("end testing division in basic case\n")

    def test_division_by_0(self):
        """ Objective: Test of division's
        division by 0 working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing division in division by 0 case")
        job = SimpleCalculator(0, 2)
        res = job.division()
        self.assertEqual(res, 0)
        job = SimpleCalculator(2, 0)
        with self.assertRaises(ZeroDivisionError):
            res = job.division()
        job = SimpleCalculator(0, 0)
        with self.assertRaises(ZeroDivisionError):
            res = job.division()
        LOGGER.info("end testing division in division by 0 case\n")

    def test_division_limit(self):
        """ Objective: Test of division's
        division with high numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing division in high number case")
        job = SimpleCalculator(-1000000, 1000000)
        res = job.division()
        self.assertEqual(res, -1)
        job = SimpleCalculator(1000000, -1000000)
        res = job.division()
        self.assertEqual(res, -1)
        job = SimpleCalculator(1000000, 1000000)
        res = job.division()
        self.assertEqual(res, 1)
        job = SimpleCalculator(-1000000, -1000000)
        res = job.division()
        self.assertEqual(res, 1)
        LOGGER.info("end testing division in high number case\n")

    def test_division_negative(self):
        """ Objective: Test of division's
        division with negative numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing division in negative number case")
        job = SimpleCalculator(2, -1)
        res = job.division()
        self.assertEqual(res, -2)
        job = SimpleCalculator(-1, 2)
        res = job.division()
        self.assertEqual(res, -0.5)
        job = SimpleCalculator(-2, -1)
        res = job.division()
        self.assertEqual(res, 2)
        LOGGER.info("end testing division in negative number case\n")

    def test_division_float(self):
        """ Objective: Test of division's
        division with float numbers working
                       Fill the log file when this test methode start and end

        """
        LOGGER.info("start testing division in float number case")
        with self.assertRaises(ValueError):
            SimpleCalculator(1, 0.5)
        LOGGER.info("end testing division in float number case\n")


if __name__ == "__main__":
    LOGGER = logging.getLogger("test")
    LOGGER.setLevel(logging.INFO)

    HANDLER = logging.FileHandler(filename="news_file.log", mode="w")
    HANDLER.setLevel(logging.DEBUG)

    FORMATTER = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    HANDLER.setFormatter(FORMATTER)

    LOGGER.addHandler(HANDLER)

    unittest.main()
