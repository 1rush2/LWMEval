# LWMEval

**LWMEval** is a benchmarking framework designed to evaluate the performance of various large-scale neural networks for 6-hour short-term forecasting. This repository includes the scripts and assets necessary to reproduce the experiments.

## Model References

Below are the references for the models used in this project:

- **Pangu:** [GitHub Repository](https://github.com/198808xc/Pangu-Weather)
- **FuXi:** [GitHub Repository](https://github.com/tpys/FuXi)
- **FourCastNet:** [GitHub Repository](https://github.com/NVlabs/FourCastNet)
- **FengWu:** [GitHub Repository](https://github.com/OpenEarthLab/FengWu)
- **GraphCast:** [GitHub Repository](https://github.com/google-deepmind/graphcast)

## Requirements

This project is built using `jax==0.4.16` and `torch==2.3.0`. To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Assets

Before running a model, make sure to download the necessary assets. You can do this using the following command:

```bash
ai-models --download-assets 
```

## Running the Models

To run the models, use the provided shell script:

```bash
sh run_models.sh
```

## Evaluation

You can evaluate the models using the Evaluation.py script:

```bash
python Evaluation.py
```

## Plotting Results

The results of the evaluation can be visualized using the plot.ipynb notebook. Open it in Jupyter Notebook and run the cells to generate the plots.

## GPU Time Calculation

To measure the GPU time for model inference, use the Gpu_time.py script:

```bash
python Gpu_time.py
```

## Directory Structure

- **Evaluation.py:** Script for evaluating the models.
- **Gpu_time.py:** Script to calculate GPU time for model inference.
- **plot.ipynb:** Jupyter Notebook for plotting the evaluation results.
- **requirements.txt:** List of required Python packages.
- **run_models.sh:** Shell script to run the models.
- **README.md:** Project overview and instructions.
## Contributing

If you wish to contribute to this project, feel free to fork the repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details.

```csharp

You can paste this directly into your `README.md` on GitHub, and it should format correctly.
```
