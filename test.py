import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu
import requests
import json
from retry import retry
from KDEpy import FFTKDE
from scipy.stats import norm
import time
from concurrent.futures import ProcessPoolExecutor


@retry(tries=3)
def get_data(url):
    # needed to avoid 403 lol
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        # sometimes we get 502 because our backend is a bit brittle, retry 3 times for good measure
        raise Exception(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

def kde_calculation(data, bw):
    return FFTKDE(kernel='gaussian', bw=bw).fit(data).evaluate()



def process(base_rev, new_rev):
    url = f"https://treeherder.mozilla.org/api/perfcompare/results/?base_repository=try&base_revision={base_rev}&new_repository=try&new_revision={new_rev}&framework=15&no_subtests=true"

    data = get_data(url)

    without_patch = [item.get('base_runs', []) for item in data][0]
    with_patch = [item.get('new_runs', []) for item in data][0]

    start = time.time()


    def kde_worker():
        x_without, y_without = kde_calculation(without_patch, 'silverman')
        x_with, y_with = kde_calculation(with_patch, 'silverman')

        y_without = kde_calculation(without_patch, 'ISJ')[1]
        y_with = kde_calculation(with_patch, 'ISJ')[1]

    # Run 1000 times
    with ProcessPoolExecutor() as executor:
        executor.map(lambda _: kde_worker(), range(1, 1000))

    end = time.time()
    print(end - start)

# 40 points each
process("6c1938160f7b56b15bacb55be910bed4407bb1cc",  "a1ce9fce48c2b4d62b947568736cfc24b396d479")
