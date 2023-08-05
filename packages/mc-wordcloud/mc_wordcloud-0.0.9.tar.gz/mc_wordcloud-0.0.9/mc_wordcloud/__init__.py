
import sys
import os
__all__=['mc_wordcloud.py']
sys.path.append("..")

def Get(name):
    return os.path.dirname(os.path.realpath(__file__)) + '\\' + name