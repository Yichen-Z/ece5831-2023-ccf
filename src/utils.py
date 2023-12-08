"""
Utility functions shared across scripts.
"""
import numpy as np

def normalize(data):
    return (data - np.mean(data)) / np.std(data)
