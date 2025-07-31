import os
import pandas as pd
import numpy as np
from prophet import Prophet
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Create the required folder structure
os.makedirs("data", exist_ok=True)
os.makedirs("forecast", exist_ok=True)  
os.makedirs("images", exist_ok=True)

print("Folder structure created successfully!")
print("Required folders:")
print("- data/")
print("- forecast/")
print("- images/")