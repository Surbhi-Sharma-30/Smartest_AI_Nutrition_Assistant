import pandas as pd

def load_nutrition_data(filepath='MultipleFiles/All_Diets.csv'):
    """
    Loads nutrition data from a CSV file.
    This function can be expanded for data cleaning, validation, etc.
    """
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while loading nutrition data: {e}")
        return pd.DataFrame()


