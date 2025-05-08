import pandas as pd
import requests
from io import StringIO

class DataWeb:
    def __init__(self):
        self.url = "https://www.worldometers.info/world-population/population-by-country/"

    def obtener_datos(self):
        try:
            # Establecer un encabezado User-Agent para simular una solicitud de navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # Realizar la solicitud GET
            response = requests.get(self.url, headers=headers)

            # Verificar si la solicitud fue exitosa
            if response.status_code != 200:
                print(f"Error al acceder a la página: {response.status_code}")
                return pd.DataFrame()

            # Leer el contenido HTML y extraer las tablas
            tablas = pd.read_html(StringIO(response.text))
            if not tablas:
                print("No se encontraron tablas en la página.")
                return pd.DataFrame()

            df = tablas[0]  # La tabla que queremos es la primera

            # Renombrar columnas
            df = df.rename(columns={
                '#': 'num',
                'Country (or dependency)': 'pais',
                'Population (2024)': 'poblacion_2024',
                'Yearly Change': 'cambio_anual',
                'Net Change': 'cambio_neto',
                'Density (P/Km²)': 'densidad_p_km2',
                'Land Area (Km²)': 'superficie_km2',
                'Migrants (net)': 'migrantes_neto',
                'Fert. Rate': 'tasa_fertilidad',
                'Median Age': 'edad_mediana',
                'Urban Pop %': 'porcentaje_poblacion_urbana',
                'World Share': 'participacion_mundial'
            })

            # Limpiar los datos
            df = self.limpiar_datos(df)

            return df

        except Exception as err:
            print(f"Error al obtener los datos: {err}")
            return pd.DataFrame()

    def limpiar_datos(self, df):
        # Limpiar las columnas numéricas
        df['cambio_anual'] = df['cambio_anual'].replace({'%': '', ',': '', '−': '-'}, regex=True).astype(float) / 100
        df['cambio_neto'] = df['cambio_neto'].replace({',': '', '−': '-'}, regex=True).astype(float)
        df['densidad_p_km2'] = df['densidad_p_km2'].replace({',': ''}, regex=True).astype(float)
        df['superficie_km2'] = df['superficie_km2'].replace({',': ''}, regex=True).astype(float)
        df['migrantes_neto'] = df['migrantes_neto'].replace({',': '', '−': '-'}, regex=True).astype(float)
        df['tasa_fertilidad'] = df['tasa_fertilidad'].replace({',': ''}, regex=True).astype(float)
        df['edad_mediana'] = df['edad_mediana'].replace({',': ''}, regex=True).astype(float)
        df['porcentaje_poblacion_urbana'] = df['porcentaje_poblacion_urbana'].replace({'%': '', ',': ''}, regex=True).astype(float) / 100
        df['participacion_mundial'] = df['participacion_mundial'].replace({'%': '', ',': ''}, regex=True).astype(float) / 100

        return df
