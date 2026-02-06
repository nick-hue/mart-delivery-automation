from pathlib import Path
import pandas as pd

def make_excel(delivery_excel: Path):
    print(f"{delivery_excel=} ")

    exlcude_cols_delivery = ["Επωνυμία Πελάτη", "Διεύθυνση", "Ημ. Παράδ.", "            Βάρος", "Total", "61x86", "70x100", "EuroPa", "Big", "Other", "Οδηγίες"]
    

    df_deliveries = pd.read_excel(delivery_excel, 
                                sheet_name=0, 
                                header=0, 
                                # usecols=lambda c: c not in exlcude_cols_delivery,
                                usecols=lambda c: c in exlcude_cols_delivery,
                                # dtype={},
                                )
    
    print(df_deliveries.columns)
    
    df_deliveries.columns = ["" if str(c).startswith("Unnamed") else c for c in df_deliveries.columns]


    print(df_deliveries.head(5))

