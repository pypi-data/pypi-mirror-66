import re
import os
import json
import glob
import nltk
import requests
import warnings

import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import ipywidgets as widgets

from tqdm import tqdm
from ipywidgets import interact
from collections import Counter
from nltk.corpus import stopwords
from pathlib import Path, PurePath
from matplotlib import pyplot as plt
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
from IPython.display import HTML, display, clear_output
from requests.exceptions import HTTPError, ConnectionError
