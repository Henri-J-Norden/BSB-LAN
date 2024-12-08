prompt = """
Create a list of all German abbreviations (written in CAPS, such as `TWW`,  `HK`, `ADA`, `BA-Umschaltung`, `DLH` etc.) used in the following Siemens Boiler-System-Bus parameters. Explain their meaning in the context, write out the full word/phrase deabbreviated, translate it to English and give the equivalent English abbreviation.

Output in the format:
```
("<German abbreviation>", "<explanation>", "<full German deabbreviated word/phrase>", "<English translation>", "<English abbreviation>"),
...
```


German parameters:
```
...
```
"""

# ("<German abbreviation>", "<explanation>", "<full German deabbreviated word/phrase>", "<English translation>", "<English abbreviation>"),
abbrev = [
    ("HK", "Heating circuit (Heizkreis)", "Heizkreis", "Heating circuit", "HC"),
    ("H1", "", "Heizkreis 1", "Heating circuit 1", "HC1"),
    ("H2", "", "Heizkreis 2", "Heating circuit 2", "HC2"),
    ("H3", "", "Heizkreis 3", "Heating circuit 3", "HC3"),
    ("HKW", "", "Heizkreis Wärme", "Heating Circuit Heat", "HC"),

    ("HKP", "Heating circuit pump (Heizkreispumpe)", "Heizkreispumpe", "Heating circuit pump", "HC pump"),

    #("TWW", "Domestic hot water (Trinkwasser)", "Trinkwasser", "Domestic hot water", "DHW"),
    ("TWW", "Domestic hot water", "Trinkwarmwasser", "Domestic hot water", "DHW"),
    ("TW", "", "Trinkwasser", "Domestic water", "DHW"),
    ("BW", "", "Brauchwasser", "Domestic water", "DHW"),
    # ^ [manual] usage duplicates TWW

    #("BA-Umschaltung", "Operating mode switching (Betriebsartumschaltung)", "Betriebsartumschaltung", "Operating mode switching", "OMS"),
    ("BA", "Operating mode switching (Betriebsartumschaltung)", "Betriebsart", "Operating mode", ""),

    #("DLH", "Instantaneous water heater (Durchlauferhitzer)", "Durchlauferhitzer", "Instantaneous water heater", "IWH"),
    ("DLH", "Instantaneous water heater (Durchlauferhitzer)", "Durchlauferhitzer", "Instantaneous water heater", ""),
    # ^ duplicate of TWW?
    ("Durchl'erhitzer", "", "Durchlauferhitzer", "Instantaneous water heater", ""),

    #("ADA", "Adaptive drift adjustment (Adaptive Driftanpassung)", "Adaptive Driftanpassung", "Adaptive drift adjustment", "ADA"),
    ("STB", "Safety temperature limiter (Sicherheitstemperaturbegrenzer)", "Sicherheitstemperaturbegrenzer", "Safety temperature limiter", ""),
    #("FA", "Combustion controller (Feuerungsautomat)", "Feuerungsautomat", "Combustion controller", ""),
    # ^ ?

    #("TR", "Temperature range (Temperaturhub)", "Temperaturhub", "Temperature range", "TR"),
    ("TR", "Thermostat regulator", "Temperatur-Regler", "Thermostat limiting", ""),
    # ^ STR2310_TEXT

    ##("PWM", "Pulse-width modulation", "Pulsweitenmodulation", "Pulse-width modulation", "PWM"),
    ("UV", "Diverter valve (Umlenkventil)", "Umlenkventil", "Diverter valve", ""),
    ("EW", "Electrical heater (Elektroeinsatz)", "Elektroeinsatz", "Electrical heater", ""),
    ("WP", "Heat pump (Wärmepumpe)", "Wärmepumpe", "Heat pump", ""),
    #("EVI", "External vapor injection", "Externe Dampfeinspritzung", "External vapor injection", "EVI"),
    ##("EVI", "Enhanced vapor injection", "?", "Enhanced Vapor Injection", "EVI"),
    ("RT", "Room thermostat (Raumthermostat)", "Raumthermostat", "Room thermostat", ""),
    ##("LPB", "Local Process Bus", "Lokaler Prozessbus", "Local Process Bus", "LPB"),
    ##("BSB", "Boiler System Bus", "Boiler-System-Bus", "Boiler System Bus", "BSB"),
    ##("PPS", "Plug and Play System", "Plug and Play System", "Plug and Play System", "PPS"),
    #("BMU", "Bus module (Busmodul)", "Busmodul", "Bus module", "BM"),
    # ^ maybe: ("BMU", "Burner Management Unit", "Brenner-Management-Unit", "Burner Management Unit", "BMU"),
    ("RU", "Room unit (Raumgerät)", "Raumgerät", "Room unit", ""),
    # ^ duplicate of RT?
    ##("HMI", "Human-machine interface", "Mensch-Maschine-Schnittstelle", "Human-machine interface", "HMI"),

    # https://www.remehatools.be/wp-content/uploads/documents/archive/BROETJE/Gas/BBS%20EVO/160802%20IM%20SM%20BBS%20EVO%2015_28%20H%20NL.pdf
    ("SSP", "Stratified storage tank (Schichtenspeicher)", "Schichtenspeicher", "Stratified storage tank", ""),
    #("KVF", "Cold water feed (Kaltwasserzufuhr)", "Kaltwasserzufuhr", "Cold water feed", "CWF"),
    ("KVF", "", "Kesselvorlauf-Fühler", "Boiler flow sensor", ""),
    #("KRF", "Cold water return (Kaltwasserrücklauf)", "Kaltwasserrücklauf", "Cold water return", "CWR"),
    ("KRF", "", "Kesselrücklauf-Fühler", "Boiler return sensor", ""),

    #("ISR", "Integral step response (Integral Sprungantwort)", "Integral Sprungantwort", "Integral step response", "ISR"),
    # ^ ?

    #("TVHw", "Minimum flow temperature setpoint (Minimale Vorlauftemperatur Sollwert)", "Minimale Vorlauftemperatur Sollwert", "Minimum flow temperature setpoint", "MFTS"),
    ("TVHw", "Minimum flow temperature setpoint (Minimale Vorlauftemperatur Sollwert)", "Minimale Vorlauftemperatur Sollwert", "Minimum flow temperature setpoint", ""),

    #("QAA", "Room control unit (Raumgerät)", "Raumgerät", "Room control unit", "RCU"),
    ("QAA", "designation used by Siemens for a type of room unit or controller", "", "A type of Siemens room thermostat or control unit", "QAA"),
    # ^ duplicate of RU

    #("OCI", "OpenTherm interface", "OpenTherm-Schnittstelle", "OpenTherm interface", "OTI"),
    ("OCI", "designation used by Siemens for a type of boiler communication interface", "", "A type of Siemens boiler communication interface", "OCI"),

    #("PC-Tool", "PC tool", "PC-Werkzeug", "PC tool", "PC tool"),
    #("HX", "Heat exchanger (Wärmetauscher)", "Wärmetauscher", "Heat exchanger", "HX"),
    ("VK", "Consumer circuit (Verbraucherkreis)", "Verbraucherkreis", "Consumer circuit", ""),
    ("Verbr'kreis", "", "Verbraucherkreis", "Consumer circuit", ""),
    ("Verbr'anforderung", "", "Verbraucheranforderung", "Load demand", ""),

    ("KK", "Cooling circuit (Kühlkreis)", "Kühlkreis", "Cooling circuit", "CC"),

    # only one use, written out elsewhere:
    ("NT", "Low tariff (Niedertarif)", "Niedertarif", "Low tariff", ""),
    ("HT", "", "Hochtarif", "High tariff", ""),

    # Manual:
    ("HD", "", "Hochdruck", "High pressure", ""),
    ("ND", "", "Niederdruck", "Low pressure", ""),
    ("MK", "", "Mischkreis", "Mixing circuit", ""),
    ("PK", "", "Pumpenkreis", "Pump circuit", ""),
    ("Zus'br", "", "Zusatzbrenner", "Auxiliary burner", ""),
    ("Schw'bad", "", "Schwimmbad", "Swimming pool", ""),
    ("FA", "", "Feuerungsautomat", "Burner control unit", ""),

]


def get_abbrev():
    return [((a[0], a[2]), (a[4], a[3])) for a in abbrev]


if __name__ == "__main__":
    print(get_abbrev())
