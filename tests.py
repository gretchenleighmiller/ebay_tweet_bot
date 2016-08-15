# -*- coding: utf-8 -*-
import unittest

def main():
	tests = unittest.TestLoader().discover('.')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	main()