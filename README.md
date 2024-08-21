
# LWMEval
模型参考链接：

pangu：https://github.com/198808xc/Pangu-Weather

fuxi：https://github.com/tpys/FuXi

FourCastNet：https://github.com/NVlabs/FourCastNet

FengWu：https://github.com/OpenEarthLab/FengWu

graphcast：https://github.com/google-deepmind/graphcast


## Requirement
我的模型是基于jax==0.4.16 torch==2.3.0，安装命令

pip install requirements.txt

## Assets
To download the assets before running a model, use the following command:

ai-models --download-assets <model-name>

## Evaluation
python Evaluation.py

To help you enhance the content of your GitHub repository for the project "LWMEval," I'll provide some improvements and suggestions for the `README.md` file and the directory structure.

### README.md (Enhanced Version)

```markdown
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
ai-models --download-assets <model-name>
```

## Running the Models

To run the models, use the provided shell script:

```bash
sh run_models.sh
```

## Evaluation

You can evaluate the models using the `Evaluation.py` script:

```bash
python Evaluation.py
```

## Plotting Results

The results of the evaluation can be visualized using the `plot.ipynb` notebook. Open it in Jupyter Notebook and run the cells to generate the plots.

## GPU Time Calculation

To measure the GPU time for model inference, use the `Gpu_time.py` script:

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Suggestions for Directory Structure

1. **Add a `LICENSE` file:** If you haven’t added a license yet, it’s good practice to include one. MIT License is commonly used for open-source projects.

2. **Include Examples:** If possible, include a folder with example outputs or pre-trained models to help users get started quickly.

3. **Documentation:** Consider expanding your documentation with more details on each model’s implementation, including citations or links to relevant papers.

4. **Automate Tests:** If possible, add a testing script or unit tests for your evaluation code to ensure everything works as expected when contributors make changes.

5. **Badges:** Add badges to your `README.md` for things like build status, license, and version to make the repository look more professional.

This enhanced `README.md` should help users understand your project more clearly and guide them through setting it up and using it.
