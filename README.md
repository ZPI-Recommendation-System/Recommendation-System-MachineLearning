# Machine Learning for Laptop Prices

The project uses machine learning for predicting laptop prices.

Laptops with price source set as "allegro" are saved, converted and used for training.

Then the model is used to set price for laptops without given price.

## Installation

```bash
pip install -r requirements.txt
```

Packages are listed only for the two scripts described below.

## Learning 

```bash
# make sure that DATA_FROM_DB is set to True in the file
python tree.py
```

## Setting prices in the database

```bash
python evaluator.py
```