# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 15:10:17 2020

@author: etienne.engel
"""

# Aim :
# Fill the log file which was created in test_code.py
# Create a class for :
# sum, substraction, multiplication and division between 2 integers
# Handle not integer input and division by zero cases

import logging

MODULE_LOGGER = logging.getLogger("test.SubPackage")


class SimpleCalculator:
    """ Objective: Do calculations on 2 integers
                   Handle not integer input and division by zer cases
                   Fill the log file when it's usefull (__init__ and division)

    Parameters:
        arguments1 (int): First variables for calculation
        arguments2 (int): Second variables for calculation

    Returns:
        ret (int or float): The calculation's result
    """

    def __init__(self, a, b):
        """ Objective: Initialize the 2 attributs of each SimpleCalculator object
            Verify that input are integers
            Fill the log file when instance is created or not

        Parameters:
            arguments1: First variables for calculation
            arguments2: Second variables for calculation
        """
        if not (isinstance(a, int) and isinstance(b, int)):
            self.logger = logging.getLogger("test.SubPackage.calculator")
            self.logger.warning("instance of SimpleCalculator not created")
            raise ValueError("Need integers input")
        self.chiffre1 = a
        self.chiffre2 = b
        self.logger = logging.getLogger("test.SubPackage.calculator")
        self.logger.info("instance of SimpleCalculator created")

    def personnal_sum(self):
        """ Objective: Add 2 integers

        Parameters:
            arguments1 (int): First variables for addition
            arguments2 (int): Second variables for addition

        Return:
            ret (int): The addition's result
        """

        res = self.chiffre1 + self.chiffre2
        return res

    def substraction(self):
        """ Objective: Substraction of 2 integers

        Parameters:
            arguments1 (int): First variables for substraction
            arguments2 (int): Second variables for substraction

        Return:
            ret (int): The substraction's result
        """
        res = self.chiffre1 - self.chiffre2
        return res

    def multiplication(self):
        """ Objective: Multiplication of 2 integers

        Parameters:
            arguments1 (int): First variables for multiplication
            arguments2 (int): Second variables for multiplication

        Return:
            ret (int): The multiplication's result
        """
        res = self.chiffre1 * self.chiffre2
        return res

    def division(self):
        """ Objective: Division of 2 integers
                       Handle the zero division case
                       Fill the log file when ZeroDivisionError

        Parameters:
            arguments1 (int): First variables for division
            arguments2 (int): Second variables for division

        Return:
            ret (int or float): The division's result
        """
        if self.chiffre2 == 0:
            self.logger.warning("Cannot divide by zero")
            raise ZeroDivisionError("Cannot divide by zero")
        res = self.chiffre1 / self.chiffre2
        return res
