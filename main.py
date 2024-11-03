import pandas as pd
import sqlite3
import os

# modules
from scripts import url_methods, structures

URL = "https://varieties.worldcoffeeresearch.org/"
subpages = ["arabica","robusta"]

db_path = os.path.join(os.path.curdir, "data/test_db.db")
test_db_con = sqlite3.connect(db_path)

if __name__ == "__main__":
    # extract step
    print("fetching coffee data")
    c_names = url_methods.get_coffee_names(URL, subpages)
    c_struct = url_methods.get_coffee_info(c_names)

    # transform step
    print("converting data into dataframe")
    coffee_info = structures.parse_coffee_info_dict(c_struct)

    # load step
    varietal_and_information = pd.DataFrame.from_records(coffee_info)
    print(varietal_and_information.columns)

    # load step
    print("loading data into sql")
    varietal_and_information.to_sql(
        name='coffee',
        con=test_db_con,
        index=False,
        if_exists='replace'
    )
    test_db_con.close()
    print("done")
