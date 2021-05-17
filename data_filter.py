import pandas as pd


def csv_io():
    df = pd.read_csv(filepath_or_buffer='data.csv')
    # 0 sqft rows will not be counted - considered erroneous rows
    df = df.loc[(df['price'] / df['sq__ft']) < 220]
    df.to_csv('output.csv')


if __name__ == "__main__":
    csv_io()
