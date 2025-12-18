szczyty_tatr = {
    "Rysy" : {
        "name" : "Rysy",
        "lat" : 49.1794, # długość geograficzna
        "lon" : 20.0881, # szerokość geograficzna
        "elevation" : 2501,
        "region" : "Tatry Wysokie",
        "country" : "both" # leżą na granicy Polsko-Słowackiej
    },
    "Gerlach" : {
        "name" : "Gerlach",
        "lat" : 49.1639,
        "lon" : 20.1317,
        "elevation" : 2655,
        "region" : "Tatry Wysokie",
        "country" : "sk" # sk-słowacja
    },
    "Lomnica" : {
        "name" : "Lomnica",
        "lat" : 49.1950,
        "lon" : 20.2131,
        "elevation" : 2634,
        "region" : "Tatry Wysokie",
        "country" : "sk"
    },
    "Lodowy szczyt" : {
        "name" : "lodowy szczyt",
        "lat" : 49.1972,
        "lon" : 20.1833,
        "elevation" : 2627,
        "region" : "Tatry Wysokie",
        "country" : "sk"
    },
    "Durny szczyt" : {
        "name" : "Durny szcyt",
        "lat" : 49.1889,
        "lon" : 20.1667,
        "elevation" : 2623,
        "region" : "Tatry Wysokie",
        "country" : "sk"
    },
    "Kieżmarski szczyt" : {
        "name" : "Kieżmarski szczyt",
        "lat" : 49.2167,
        "lon" : 20.2167,
        "elevation" : 2558,
        "region" : "Tatry Wysokie",
        "country" : "sk"
    },
    "Wysoka" : {
        "name" : "Wysoka",
        "lat" : 49.1833,
        "lon" : 20.1000,
        "elevation" : 2547,
        "region" : "Tatry Wysokie",
        "country" : "sk"
    },
    "Krywań" : {
        "name" : "Krywań",
        "lat" : 49.1625,
        "lon" : 19.9997,
        "elevation" : 2495,
        "region" : "Tatry Wysokie",
        "country" : "sk"
    },
    "Mięguszowiecki Szczyt Wielki" : {
        "name" : "Mięguszowiecki Szczyt Wielki",
        "lat" : 49.1869,
        "lon" : 20.0711,
        "elevation" : 2438,
        "region" : "Tatry Wysokie",
        "country" : "both"
    },
    "Świnica" : {
        "name" : "Świnica",
        "lat" : 49.2194,
        "lon" : 20.0097,
        "elevation" : 2301,
        "region" : "Tatry Wysokie",
        "country" : "pl" # pl-Polska
    },
    "Kozi Wierch" : {
        "name" : "Kozi Wierch",
        "lat" : 49.2167,
        "lon" : 20.0333,
        "elevation" : 2291,
        "region" : "Tatry Wysokie",
        "country" : "pl"
    },
    "Mnich" : {
        "name" : "Mnich",
        "lat" : 49.1933,
        "lon" : 20.0556,
        "elevation" : 2068,
        "region" : "Tatry Wysokie",
        "country" : "pl"
    },
    "Kasprowy Wierch" : {
        "name" : "Kasprowy Wierch",
        "lat" : 49.2511,
        "lon" : 19.9350,
        "elevation" : 1894,
        "region" : "Tatry Zachodnie",
        "country" : "pl"
    },
    "Giewont" : {
        "name" : "Giewont",
        "lat" : 49.2511,
        "lon" : 19.9350,
        "elevation" : 1894,
        "region" : "Tatry Zachodnie",
        "country" : "pl"
    },
    "Szpiglasowy Wierch" : {
        "name" : "Szpiglasowy Wierch",
        "lat" : 49.2000,
        "lon" : 20.0417,
        "elevation" : 2171,
        "region" : "Tatry Wysokie",
        "country" : "both"
    }
}


def get_peak_info(peak_name):
    # Funkcja zwraca informacje o szczycie po  nazwie

    if peak_name in szczyty_tatr:
        return szczyty_tatr[peak_name]
    else:
        print(f"Błąd: Szczyt '{peak_name}' nie istnieje w bazie!")
        return None

def  get_all_peaks(szczyty_tatr):
    # Funkcja zwraca listę wszystkich dostępnych szczytów

    peaks = list(szczyty_tatr.keys())
    peaks.sort()
    return peaks

def get_peaks_by_region(region_name):
    # Funkcja zwraca listę szczytów w danym retgionie Tatr
    result = []

    for peak_name, peak_data in szczyty_tatr.items():
        if peak_data["region"] == region_name:
            result.append(peak_name)
    return result



# Testy funkcjii
if __name__ == "__main__":
    print("=== TESTY peaks_database.py ===")

    # Test 1: get_peak_info
    print("\n1. Test get_peak_info('Rysy'):")
    rysy_info = get_peak_info("Rysy")
    print(f"   {rysy_info}")

    # Test 2: get_all_peaks
    print("\n2. Test get_all_peaks():")
    all_peaks = get_all_peaks(szczyty_tatr)
    print(f"   Liczba szczytów: {len(all_peaks)}")
    print(f"   Szczyty: {all_peaks}")

    # Test 3: get_peaks_by_region
    print("\n3. Test get_peaks_by_region('Tatry Wysokie'):")
    wysokie = get_peaks_by_region("Tatry Wysokie")
    print(f"   Tatry Wysokie ({len(wysokie)} szczytów): {wysokie}")

    print("\n4. Test get_peaks_by_region('Tatry Zachodnie'):")
    zachodnie = get_peaks_by_region("Tatry Zachodnie")
    print(f"   Tatry Zachodnie ({len(zachodnie)} szczytów): {zachodnie}")

    print("\n✅ Wszystkie testy zakończone!")
