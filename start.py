#!/usr/bin/python
# -*- coding: utf-8 -*-
__AUTHOR__='Danevych V.'
__COPYRIGHT__='Danevych V. 2016 Kiev, Ukraine'
__version__ = "2.0.0"
__status__ = "Production"
#vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import sys
import num_to_eng
import num_to_ukr
from num_to_ukr import print_utf


def print_lang_menu():
    """ Function shows menu of launguage selection"""    
    print 10 * "-" , "MENU" , 10 * "-"
    print "1. English launguage"
    print "2. Українська мова"
    print "3. Type number again"
    print "4. Exit"

    
def main():
    """ Main code is here"""
    loop = True
    while loop:          
        print("Please, enter number")
        #print(u"Будь ласка, введіть число ціле та дробне")
        x = input()
        print_lang_menu()    ## Displays language menu
        choice = input("Enter your choice [1-4]: ")
        if choice == 1:
            num = float(x)
            print_utf(num_to_eng.dollars(num))
            # uncomment the line below for extra capabilities - integer numbers and fractional numerals (float type) to words translation
            #print_utf(num_to_eng.in_words(num))
        if choice == 2:
            num = float(x)
            print_utf(num_to_ukr.gryvens(num))
            # uncomment the line below for extra capabilities - integer numbers and fractional numerals (float type) to words translation
            #print_utf(num_to_ukr.in_words(num))
        if choice == 3:     
            main()
        if choice == 4:
            print("Bye!")
            sys.exit()
        
                        
if __name__ == '__main__':
    main()
