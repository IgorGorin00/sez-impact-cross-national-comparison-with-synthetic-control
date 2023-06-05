# SEZ Impact Evaluation with Synthetic Control
## Overview

This project focuses on the impact evaluation of Special Economic Zones (SEZs) in the countries of India, Brazil, and Russia. The Synthetic Control Methodology (SCM) is employed to assess the effects of SEZs on various economic indicators, such as Gross Domestic Product (GDP), industrial production, direct investments, and fixed assets. The project utilizes the [SparseSC library](https://github.com/microsoft/SparseSC), a Python package specifically designed for conducting synthetic control analysis with sparse data.

## Dependencies

To run the code and reproduce the results of this project, the following dependencies are required (for more info see requirements.txt):

    Python 3.x
    SparseSC library
    Pandas
    NumPy
    Scikit-learn

## Project Structure

The project repository is organized as follows:

Main directory contains Jupyter notebooks and scripts that demonstrate the data preprocessing steps, SCM implementation, and result analysis for each country.
datasets/: Contains the datasets used for the analysis, and bash script to download them.
results/: Stores the generated output files, including SCM estimates and evaluation metrics (json files).
README.md: This file provides an overview of the project and instructions for running the code.

## Usage

Clone the repository to your local machine.
Install the required dependencies using pip or any other package manager of your choice.
Navigate to the directory and run the Jupyter notebooks in the desired order (SC-for-india-sez.ipynb, SC-for-brazil-sez.ipynb, SC-for-russian-sez.ipynb) to perform the analysis for each country.
Follow the instructions within the notebooks to preprocess the data, implement the SCM models using SparseSC, and interpret the results.
The output files with SCM estimates and evaluation metrics will be saved in the results/ directory for further analysis and reporting.

## Conclusion

This project employs the SparseSC library to evaluate the impact of SEZs in India, Brazil, and Russia. By utilizing the Synthetic Control Methodology, the project aims to provide insights into the effects of SEZs on key economic indicators in these countries. The code and analysis provided here serve as a foundation for further research and policy evaluation related to SEZs and their impact on economic development.

Please refer to the Jupyter notebooks and the respective sections within them for detailed explanations and step-by-step instructions on data preprocessing, SCM implementation, and result analysis.

Note: The data used in this project is for illustrative purposes only and may not reflect the latest available data.


You can also find the complete codebase on GitHub:
- [Vizualization of Results](https://github.com/IgorGorin00/research_sc_viz)
