# Mapowanie atrybutów - Szybki przewodnik

Ten dokument zawiera mapowanie wszystkich 20 atrybutów z formatu czytelnego dla człowieka (polski) na kody używane przez model.

## Atrybut 1: Status konta czekowego
| Kod | Opis polski |
|-----|-------------|
| A11 | mniej niż 0 DM |
| A12 | od 0 do 200 DM |
| A13 | 200 DM lub więcej / wypłaty przez co najmniej 1 rok |
| A14 | brak konta czekowego |

## Atrybut 2: Czas trwania kredytu
**Typ:** Numeryczny (w miesiącach)
**Przykład:** 24

## Atrybut 3: Historia kredytowa
| Kod | Opis polski |
|-----|-------------|
| A30 | brak kredytów / wszystkie kredyty spłacone prawidłowo |
| A31 | wszystkie kredyty w tym banku spłacone prawidłowo |
| A32 | istniejące kredyty spłacane prawidłowo do tej pory |
| A33 | opóźnienia w spłatach w przeszłości |
| A34 | konto krytyczne / inne istniejące kredyty (nie w tym banku) |

## Atrybut 4: Cel kredytu
| Kod | Opis polski |
|-----|-------------|
| A40 | samochód (nowy) |
| A41 | samochód (używany) |
| A42 | meble/wyposażenie |
| A43 | radio/telewizja |
| A44 | sprzęt AGD |
| A45 | naprawy |
| A46 | edukacja |
| A48 | przekwalifikowanie |
| A49 | biznes |
| A410 | inne |

## Atrybut 5: Kwota kredytu
**Typ:** Numeryczny (w DM)
**Przykład:** 5000

## Atrybut 6: Konto oszczędnościowe/obligacje
| Kod | Opis polski |
|-----|-------------|
| A61 | mniej niż 100 DM |
| A62 | od 100 do 500 DM |
| A63 | od 500 do 1000 DM |
| A64 | 1000 DM lub więcej |
| A65 | nieznane / brak konta oszczędnościowego |

## Atrybut 7: Obecne zatrudnienie od
| Kod | Opis polski |
|-----|-------------|
| A71 | bezrobotny |
| A72 | mniej niż 1 rok |
| A73 | od 1 do 4 lat |
| A74 | od 4 do 7 lat |
| A75 | 7 lat lub więcej |

## Atrybut 8: Rata jako procent dochodu
**Typ:** Numeryczny (procent)
**Przykład:** 3

## Atrybut 9: Status osobisty i płeć
| Kod | Opis polski |
|-----|-------------|
| A91 | mężczyzna : rozwiedziony/w separacji |
| A92 | kobieta : rozwiedziona/w separacji/zamężna |
| A93 | mężczyzna : kawaler |
| A94 | mężczyzna : żonaty/wdowiec |
| A95 | kobieta : panna |

## Atrybut 10: Inni dłużnicy / poręczyciele
| Kod | Opis polski |
|-----|-------------|
| A101 | brak |
| A102 | współwnioskodawca |
| A103 | poręczyciel |

## Atrybut 11: Obecne miejsce zamieszkania od
**Typ:** Numeryczny (w latach)
**Przykład:** 4

## Atrybut 12: Własność
| Kod | Opis polski |
|-----|-------------|
| A121 | nieruchomość |
| A122 | umowa oszczędnościowo-budowlana / ubezpieczenie na życie |
| A123 | samochód lub inne (nie w atrybucie 6) |
| A124 | nieznane / brak własności |

## Atrybut 13: Wiek
**Typ:** Numeryczny (w latach)
**Przykład:** 35

## Atrybut 14: Inne plany ratalne
| Kod | Opis polski |
|-----|-------------|
| A141 | bank |
| A142 | sklepy |
| A143 | brak |

## Atrybut 15: Mieszkanie
| Kod | Opis polski |
|-----|-------------|
| A151 | wynajem |
| A152 | własne |
| A153 | za darmo |

## Atrybut 16: Liczba istniejących kredytów w banku
**Typ:** Numeryczny
**Przykład:** 2

## Atrybut 17: Praca
| Kod | Opis polski |
|-----|-------------|
| A171 | bezrobotny / niewykwalifikowany - nierezydent |
| A172 | niewykwalifikowany - rezydent |
| A173 | wykwalifikowany pracownik / urzędnik |
| A174 | menedżer / samozatrudniony / wysoko wykwalifikowany / oficer |

## Atrybut 18: Liczba osób na utrzymaniu
**Typ:** Numeryczny
**Przykład:** 2

## Atrybut 19: Telefon
| Kod | Opis polski |
|-----|-------------|
| A191 | brak |
| A192 | tak, zarejestrowany na nazwisko klienta |

## Atrybut 20: Pracownik zagraniczny
| Kod | Opis polski |
|-----|-------------|
| A201 | tak |
| A202 | nie |

---

## Przykład kompletnego rekordu

### Format czytelny:
```
Status konta: 200 DM lub więcej
Czas trwania: 24 miesiące
Historia: istniejące kredyty spłacane prawidłowo
Cel: radio/telewizja
Kwota: 5000 DM
Oszczędności: 500-1000 DM
Zatrudnienie: 7+ lat
Rata: 2% dochodu
Status osobisty: mężczyzna kawaler
Poręczyciele: brak
Zamieszkanie: 4 lata
Własność: nieruchomość
Wiek: 35 lat
Inne raty: brak
Mieszkanie: własne
Kredyty w banku: 1
Praca: wykwalifikowany pracownik
Osoby na utrzymaniu: 1
Telefon: tak
Pracownik zagraniczny: nie
```

### Format modelu:
```python
{
    'Attribute1': 'A13',
    'Attribute2': 24,
    'Attribute3': 'A32',
    'Attribute4': 'A43',
    'Attribute5': 5000,
    'Attribute6': 'A63',
    'Attribute7': 'A75',
    'Attribute8': 2,
    'Attribute9': 'A93',
    'Attribute10': 'A101',
    'Attribute11': 4,
    'Attribute12': 'A121',
    'Attribute13': 35,
    'Attribute14': 'A143',
    'Attribute15': 'A152',
    'Attribute16': 1,
    'Attribute17': 'A173',
    'Attribute18': 1,
    'Attribute19': 'A192',
    'Attribute20': 'A202'
}
```

## Uwagi

- **Atrybuty numeryczne:** Wprowadzaj wartości bezpośrednio (np. 24, 5000)
- **Atrybuty kategoryczne:** System automatycznie konwertuje wybór użytkownika na odpowiedni kod
- **Waluta:** DM (Deutsche Mark) - niemiecka marka
- **Wszystkie atrybuty są wymagane** - brak wartości może prowadzić do błędów predykcji
