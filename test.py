import pandas as pd
import numpy as np
import random as rn
import json
import time
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.utils import np_utils
from flask import Flask, request
from flask_restful import Resource, Api
from flask_oauthlib.provider import OAuth2Provider
import sys, os

print(os.listdir())