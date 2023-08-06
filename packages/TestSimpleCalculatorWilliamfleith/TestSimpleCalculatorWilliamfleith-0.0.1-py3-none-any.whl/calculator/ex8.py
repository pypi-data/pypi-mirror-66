# -*- coding: utf-8 -*-
"""
Created on 03/04/2020
by William FLEITH
"""
import logging

MODULELOG = logging.getLogger("test.calculator")
#In This programm we are adding logging modules to enables more checks and informations on errors.

class SimpleCalculator:
    """
    Will calculate the operation of 2 variables
    """

    def __init__(self, init1, init2):
        """
        Init function
        isinstance test if our number are integer or not
        """
        if (isinstance(init1, int) and isinstance(init2, int)) is False:
            self.logger = logging.getLogger("test.calculator.ex7")
            self.logger.warning("No instance created for SimpleCalculator")
            raise ValueError("Need integers input")
        self.number1 = init1
        self.number2 = init2
        self.logger = logging.getLogger("test.calculator.ex7")
        self.logger.info("an instance has been created for SimpleCalculator")

    def sum(self):
        """
        addition function
        """


        result = self.number1 + self.number2
        return result

    def substract(self):
        """
        substract function
        """

        result = self.number1 - self.number2
        return result

    def multiply(self):
        """
        multiply function
        """

        result = self.number1 * self.number2
        return result

    def divide(self):
        """
        divide function
        It also check whether to divide by 0 or not.
        """
        if self.number2 == 0:
            self.logger.warning("Cannot divide by zero")
            raise ZeroDivisionError("Cannot divide by zero")


        result = self.number1 / self.number2
        return result
