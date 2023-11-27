from datetime import datetime

def get_TOP_10_FEATURES():
    """
    Method to return the 10 most relevant features for training the model
    """
    return [
        "OPERA_Latin American Wings", 
        "MES_7",
        "MES_10",
        "OPERA_Grupo LATAM",
        "MES_12",
        "TIPOVUELO_I",
        "MES_4",
        "MES_11",
        "OPERA_Sky Airline",
        "OPERA_Copa Air"
    ]

def get_period_day(date):
    date_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S').time()
    morning_min = datetime.strptime("05:00", '%H:%M').time()
    morning_max = datetime.strptime("11:59", '%H:%M').time()
    afternoon_min = datetime.strptime("12:00", '%H:%M').time()
    afternoon_max = datetime.strptime("18:59", '%H:%M').time()
    evening_min = datetime.strptime("19:00", '%H:%M').time()
    evening_max = datetime.strptime("23:59", '%H:%M').time()
    night_min = datetime.strptime("00:00", '%H:%M').time()
    night_max = datetime.strptime("4:59", '%H:%M').time()
    
    if(date_time > morning_min and date_time < morning_max):
        return 'mañana'
    elif(date_time > afternoon_min and date_time < afternoon_max):
        return 'tarde'
    elif(
        (date_time > evening_min and date_time < evening_max) or
        (date_time > night_min and date_time < night_max)
    ):
        return 'noche'


def is_high_season(fecha):
    fecha_año = int(fecha.split('-')[0])
    fecha = datetime.strptime(fecha, '%Y-%m-%d %H:%M:%S')
    range1_min = datetime.strptime('15-Dec', '%d-%b').replace(year = fecha_año)
    range1_max = datetime.strptime('31-Dec', '%d-%b').replace(year = fecha_año)
    range2_min = datetime.strptime('1-Jan', '%d-%b').replace(year = fecha_año)
    range2_max = datetime.strptime('3-Mar', '%d-%b').replace(year = fecha_año)
    range3_min = datetime.strptime('15-Jul', '%d-%b').replace(year = fecha_año)
    range3_max = datetime.strptime('31-Jul', '%d-%b').replace(year = fecha_año)
    range4_min = datetime.strptime('11-Sep', '%d-%b').replace(year = fecha_año)
    range4_max = datetime.strptime('30-Sep', '%d-%b').replace(year = fecha_año)
    
    if ((fecha >= range1_min and fecha <= range1_max) or 
        (fecha >= range2_min and fecha <= range2_max) or 
        (fecha >= range3_min and fecha <= range3_max) or
        (fecha >= range4_min and fecha <= range4_max)):
        return 1
    else:
        return 0


def get_min_diff(data):
    fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
    fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
    min_diff = ((fecha_o - fecha_i).total_seconds())/60
    return min_diff


def get_allowed_airlines():
    """
    Method used to list the allowed airlines to make a prediction.
    Should be replaced by data retrieved from a database model
    """
    return [
            "Aerolineas Argentinas",
            "Aeromexico",
            "Air Canada",
            "Air France",
            "Alitalia",
            "American Airlanes",
            "Austral",
            "Avianca",
            "British Airways",
            "Copa Air",
            "Delta Air",
            "Gol Trans",
            "Grupo LATAM",
            "Iberia",
            "JetSmart SPA",
            "K.L.M.",
            "Lacsa",
            "Latin American Wings",
            "Oceanair Linhas Aereas",
            "Plus Ultra Lineas Aereas",
            "Qantas Airways",
            "Sky Airline",
            "United Airlines"
        ]

def prepare_data(data):
    """
    Method to prepare the data for predicting
    """
    prepared_data = []
    for feature in get_TOP_10_FEATURES():
        if feature.startswith("OPERA") and f'OPERA_{data.OPERA}' == feature:
            prepared_data.append(1)
        elif feature.startswith("MES") and f'MES_{data.MES}' == feature:
            prepared_data.append(1)
        elif feature.startswith("TIPOVUELO") and f'TIPOVUELO_{data.TIPOVUELO}' == feature:
            prepared_data.append(1)
        else:
            prepared_data.append(0)
    return prepared_data
