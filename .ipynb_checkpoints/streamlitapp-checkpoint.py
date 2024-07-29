{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d2e25e28-24ed-4140-9c9b-b6537a751be9",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "\n",
    "st.title('Simple Streamlit App')\n",
    "\n",
    "st.write(\"Here's our first attempt at using data to create a table:\")\n",
    "data = pd.DataFrame({\n",
    "    'Column 1': [1, 2, 3, 4],\n",
    "    'Column 2': [10, 20, 30, 40]\n",
    "})\n",
    "st.write(data)\n",
    "\n",
    "st.write(\"And here's a line chart:\")\n",
    "chart_data = pd.DataFrame(\n",
    "    np.random.randn(20, 3),\n",
    "    columns=['a', 'b', 'c']\n",
    ")\n",
    "st.line_chart(chart_data)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
