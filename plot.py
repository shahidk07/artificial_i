import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# print(sns.get_dataset_names())
penguins=sns.load_dataset('penguins')

# print(penguins.head())
print(penguins["island"].value_counts()
)