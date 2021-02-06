import pandas as pd, numpy as np
AA = pd.concat([pd.read_csv('../Datasets/AA-1.txt', sep=';', low_memory=False),
                pd.read_csv('../Datasets/AA-2.txt', sep=';', low_memory=False),
                pd.read_csv('../Datasets/AA-3.txt', sep=';', low_memory=False),
                pd.read_csv('../Datasets/AA-4.txt', sep=';', low_memory=False),
                pd.read_csv('../Datasets/AA-5.txt', sep=';', low_memory=False),
                pd.read_csv('../Datasets/AA-6.txt', sep=';', low_memory=False),
                pd.read_csv('../Datasets/AA-7.txt', sep=';', low_memory=False),
                pd.read_csv('../Datasets/AA-8.txt', sep=';', low_memory=False)],
                axis=0,
                ignore_index=True
                )


AS = pd.concat([pd.read_csv('../Datasets/AS-1.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/AS-2.txt', sep=';', low_memory=False)],
           axis=0, 
           ignore_index=True
         )


Passengers = pd.concat([pd.read_csv('../Datasets/Passengers-1.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/Passengers-2.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/Passengers-3.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/Passengers-4.txt', sep=';', low_memory=False)],
           axis=0, 
           ignore_index=True
         )


UA = pd.concat([pd.read_csv('../Datasets/UA-1.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/UA-2.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/UA-3.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/UA-4.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/UA-5.txt', sep=';', low_memory=False),
           pd.read_csv('../Datasets/UA-6.txt', sep=';', low_memory=False)],
           axis=0, 
           ignore_index=True
         )


B6 = pd.read_csv('../Datasets/B6.txt', sep=';', low_memory=False)
F9 = pd.read_csv('../Datasets/B6.txt', sep=';', low_memory=False)
G4 = pd.read_csv('../Datasets/G4.txt', sep=';', low_memory=False)

HA = pd.read_csv('../Datasets/HA.txt', sep=';', low_memory=False)
NK = pd.read_csv('../Datasets/NK.txt', sep=';', low_memory=False)
VX = pd.read_csv('../Datasets/VX.txt', sep=';', low_memory=False)

FuelConsumption = pd.read_csv('../Datasets/Fuel_Consumption.txt', sep=';', low_memory=False)