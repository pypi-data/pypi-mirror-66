"""
Provide lists in the United Nation's World Economic Situation and Prospects
as sequences of Pycountry elements.
"""
__author__ = "Fábio Mendes"
__version__ = "0.1.0"

from . import db

#
# Developed countries
#
north_america = db.Database(name="North America", keys={"USA", "CAN"})

developed_asia_and_pacific = db.Database(
    name="Developed Asia and Pacific", keys={"JPN", "AUS", "NZL"}
)

eu15 = db.Database(
    name="European Union's original 15 member states",
    keys={
        "AUT",
        "BEL",
        "DEU",
        "DNK",
        "ESP",
        "FIN",
        "FRA",
        "GBR",
        "GRC",
        "IRL",
        "ITA",
        "LUX",
        "NLD",
        "PRT",
        "SWE",
    },
)

eu13 = db.Database(
    name="European Union's original 15 member states",
    keys={
        "CYP",
        "MLT",
        "SVN",
        "HRV",
        "EST",
        "SVK",
        "ROU",
        "POL",
        "HUN",
        "CZE",
        "LTU",
        "BGR",
        "LVA",
    },
)

developed_europe_other = db.Database(name="Other Europe", keys={"CHE", "NOR", "ISL"})

g7 = db.Database(name="G7", keys={"DEU", "FRA", "CAN", "GBR", "USA", "ITA", "JPN"})

developed_europe = db.aggregate("Europe", eu13, eu15, developed_europe_other)
developed_countries = db.aggregate(
    "Developed Countries", north_america, developed_asia_and_pacific, developed_europe, g7
)


#
# Countries in transition
#
transitional_europe = db.Database(
    name="South-Eastern Europe", keys={"BIH", "MNE", "SRB", "ALB", "MKD"}
)

transitional_commonwealth = db.Database(
    name="Commonwealth of Independent States and Georgia",
    keys={
        "UZB",
        "AZE",
        "UKR",
        "TKM",
        "BLR",
        "RUS",
        "GEO",
        "MDA",
        "TJK",
        "ARM",
        "KGZ",
        "KAZ",
    },
)
transitional_countries = db.aggregate(
    "Economies in transition", transitional_europe, transitional_commonwealth
)


#
# Developing countries
#
north_africa = db.Database(
    name="North Africa", keys={"TUN", "MRT", "EGY", "LBY", "DZA", "SDN", "MAR"}
)

central_africa = db.Database(
    name="Central Africa", keys={"STP", "TCD", "CMR", "COG", "GAB", "CAF", "GNQ"}
)

east_africa = db.Database(
    name="East Africa",
    keys={
        "SOM",
        "UGA",
        "MDG",
        "DJI",
        "BDI",
        "ETH",
        "COM",
        "RWA",
        "COD",
        "SSD",
        "KEN",
        "ERI",
        "TZA",
    },
)

southern_africa = db.Database(
    name="Southern Africa",
    keys={"LSO", "MUS", "SWZ", "AGO", "NAM", "BWA", "ZMB", "MOZ", "ZWE", "MWI", "ZAF"},
)

west_africa = db.Database(
    name="West Africa",
    keys={
        "SLE",
        "NER",
        "SEN",
        "BFA",
        "NGA",
        "BEN",
        "CPV",
        "CIV",
        "GIN",
        "MLI",
        "GMB",
        "GNB",
        "LBR",
        "GHA",
        "TGO",
    },
)

east_asia = db.Database(
    name="East Asia",
    keys={
        "VUT",
        "PRK",
        "TWN",
        "KIR",
        "BRN",
        "PNG",
        "TLS",
        "IDN",
        "SGP",
        "MYS",
        "PHL",
        "VNM",
        "SLB",
        "MNG",
        "MMR",
        "THA",
        "CHN",
        "FJI",
        "KHM",
        "WSM",
        "LAO",
    },
)

south_asia = db.Database(
    name="South Asia",
    keys={"IND", "BTN", "BGD", "AFG", "MDV", "IRN", "NPL", "PAK", "LKA"},
)

western_asia = db.Database(
    name="Western Asia",
    keys={
        "BHR",
        "PSE",
        "SAU",
        "QAT",
        "OMN",
        "YEM",
        "ARE",
        "SYR",
        "KWT",
        "LBN",
        "IRQ",
        "ISR",
        "TUR",
        "JOR",
    },
)

caribbean = db.Database(
    name="Caribbean", keys={"BRB", "BLZ", "JAM", "BHS", "SUR", "TTO", "GUY"}
)

mexico_and_central_america = db.Database(
    name="Mexico and Central America",
    keys={"MEX", "HTI", "CRI", "HND", "PAN", "SLV", "DOM", "CUB", "NIC", "GTM"},
)

south_america = db.Database(
    name="South America",
    keys={"ARG", "CHL", "BRA", "PRY", "PER", "VEN", "ECU", "COL", "URY", "BOL"},
)

africa = db.aggregate(
    "Developing Africa",
    north_africa,
    central_africa,
    west_africa,
    east_africa,
    southern_africa,
)
asia = db.aggregate("Developing Asia", east_asia, south_asia, western_asia)
latin_america_and_caribbean = db.aggregate(
    "Latin America and the Caribbean",
    caribbean,
    mexico_and_central_america,
    south_america,
)
developing_countries = db.aggregate(
    "Developing countries", africa, asia, latin_america_and_caribbean
)


#
# Least developed countries
#
least_developed_africa = db.Database(
    name="Africa, least developed countries",
    keys={
        "MRT",
        "ETH",
        "COM",
        "SDN",
        "GNB",
        "ERI",
        "BDI",
        "DJI",
        "SSD",
        "LBR",
        "SOM",
        "MWI",
        "TGO",
        "SLE",
        "STP",
        "NER",
        "UGA",
        "MDG",
        "BEN",
        "MLI",
        "CAF",
        "MOZ",
        "BFA",
        "TZA",
        "SEN",
        "TCD",
        "LSO",
        "AGO",
        "RWA",
        "COD",
        "GIN",
        "GMB",
        "ZMB",
    },
)

least_developed_east_asia = db.Database(
    name="East Asia, least developed countries",
    keys={"KIR", "TLS", "TUV", "COK", "VUT", "SLB", "KHM", "LAO", "MMR"},
)

least_developed_south_asia = db.Database(
    name="South Asia, least developed countries", keys={"NPL", "AFG", "BTN", "BGD"}
)

least_developed_western_asia = db.Database(
    name="Western Asia, least developed countries", keys={"YEM"}
)

least_developed_latin_america_and_caribbean = db.Database(
    name="Latin America and the Caribbean, least developed countries", keys={"HTI"}
)

least_developed_countries = db.aggregate(
    "Least Developed Countries",
    least_developed_africa,
    least_developed_east_asia,
    least_developed_latin_america_and_caribbean,
    least_developed_south_asia,
    least_developed_western_asia,
)


#
# Income classifications
#
high_income_countries = db.Database(
    name="High Income",
    keys={
        "CHL",
        "NZL",
        "PAN",
        "FIN",
        "POL",
        "KWT",
        "BEL",
        "PRK",
        "AUS",
        "TWN",
        "DEU",
        "PRT",
        "NOR",
        "BRN",
        "ISL",
        "IRL",
        "BHR",
        "ARE",
        "CZE",
        "BHS",
        "ISR",
        "GBR",
        "LTU",
        "ESP",
        "URY",
        "JPN",
        "CYP",
        "GRC",
        "LVA",
        "MLT",
        "AUT",
        "SGP",
        "EST",
        "FRA",
        "CAN",
        "USA",
        "TTO",
        "HUN",
        "ITA",
        "BRB",
        "CHE",
        "SWE",
        "SVN",
        "DNK",
        "LUX",
        "SAU",
        "SVK",
        "OMN",
        "NLD",
        "CHN",
        "QAT",
        "HRV",
    },
)

upper_middle_income_countries = db.Database(
    name="Upper Middle Income",
    keys={
        "MNE",
        "AZE",
        "RUS",
        "GNQ",
        "GUY",
        "KAZ",
        "MKD",
        "ARG",
        "BIH",
        "MUS",
        "BRA",
        "NAM",
        "GEO",
        "GAB",
        "LBN",
        "DOM",
        "BWA",
        "COL",
        "SUR",
        "TUR",
        "ARM",
        "TKM",
        "MEX",
        "JAM",
        "MYS",
        "PRY",
        "MDV",
        "ROU",
        "SRB",
        "BLR",
        "ALB",
        "ECU",
        "CUB",
        "LKA",
        "GTM",
        "THA",
        "CRI",
        "BLZ",
        "LBY",
        "IRN",
        "PER",
        "CHN",
        "VEN",
        "DZA",
        "FJI",
        "IRQ",
        "BGR",
        "WSM",
        "JOR",
        "ZAF",
    },
)

lower_middle_income_countries = db.Database(
    name="Lower Middle Income",
    keys={
        "MRT",
        "BTN",
        "CMR",
        "PSE",
        "LAO",
        "COM",
        "SLV",
        "VUT",
        "SDN",
        "MAR",
        "GHA",
        "ZWE",
        "KIR",
        "DJI",
        "CPV",
        "UKR",
        "KEN",
        "PNG",
        "IND",
        "UZB",
        "STP",
        "TLS",
        "IDN",
        "HND",
        "PHL",
        "NGA",
        "COG",
        "VNM",
        "SLB",
        "MDA",
        "PAK",
        "KGZ",
        "MNG",
        "MMR",
        "TUN",
        "SEN",
        "BGD",
        "LSO",
        "EGY",
        "SWZ",
        "AGO",
        "CIV",
        "ZMB",
        "KHM",
        "NIC",
        "BOL",
    },
)

low_income_countries = db.Database(
    name="Low Income",
    keys={
        "HTI",
        "ETH",
        "COM",
        "YEM",
        "PRK",
        "GNB",
        "ERI",
        "TJK",
        "BDI",
        "SYR",
        "NPL",
        "SSD",
        "LBR",
        "SOM",
        "MWI",
        "TGO",
        "SLE",
        "NER",
        "UGA",
        "MDG",
        "BEN",
        "MLI",
        "CAF",
        "MOZ",
        "BFA",
        "TZA",
        "TCD",
        "AFG",
        "RWA",
        "COD",
        "GIN",
        "GMB",
    },
)
