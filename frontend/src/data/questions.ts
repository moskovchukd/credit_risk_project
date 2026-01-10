export interface QuestionOption {
  code: string;
  label: string;
}

export interface Question {
  attribute: string;
  question: string;
  type: 'select' | 'number';
  options?: QuestionOption[];
  unit?: string;
}

export const surveyQuestions: Question[] = [
  {
    attribute: 'Attribute1',
    question: 'Status istniejącego konta czekowego:',
    type: 'select',
    options: [
      { code: 'A11', label: 'mniej niż 0 DM' },
      { code: 'A12', label: 'od 0 do 200 DM' },
      { code: 'A13', label: '200 DM lub więcej / wypłaty przez co najmniej 1 rok' },
      { code: 'A14', label: 'brak konta czekowego' },
    ],
  },
  {
    attribute: 'Attribute2',
    question: 'Czas trwania kredytu (w miesiącach):',
    type: 'number',
    unit: 'miesiące',
  },
  {
    attribute: 'Attribute3',
    question: 'Historia kredytowa:',
    type: 'select',
    options: [
      { code: 'A30', label: 'brak kredytów / wszystkie kredyty spłacone prawidłowo' },
      { code: 'A31', label: 'wszystkie kredyty w tym banku spłacone prawidłowo' },
      { code: 'A32', label: 'istniejące kredyty spłacane prawidłowo do tej pory' },
      { code: 'A33', label: 'opóźnienia w spłatach w przeszłości' },
      { code: 'A34', label: 'konto krytyczne / inne istniejące kredyty (nie w tym banku)' },
    ],
  },
  {
    attribute: 'Attribute4',
    question: 'Cel kredytu:',
    type: 'select',
    options: [
      { code: 'A40', label: 'samochód (nowy)' },
      { code: 'A41', label: 'samochód (używany)' },
      { code: 'A42', label: 'meble/wyposażenie' },
      { code: 'A43', label: 'radio/telewizja' },
      { code: 'A44', label: 'sprzęt AGD' },
      { code: 'A45', label: 'naprawy' },
      { code: 'A46', label: 'edukacja' },
      { code: 'A48', label: 'przekwalifikowanie' },
      { code: 'A49', label: 'biznes' },
      { code: 'A410', label: 'inne' },
    ],
  },
  {
    attribute: 'Attribute5',
    question: 'Kwota kredytu (w DM):',
    type: 'number',
    unit: 'DM',
  },
  {
    attribute: 'Attribute6',
    question: 'Konto oszczędnościowe/obligacje:',
    type: 'select',
    options: [
      { code: 'A61', label: 'mniej niż 100 DM' },
      { code: 'A62', label: 'od 100 do 500 DM' },
      { code: 'A63', label: 'od 500 do 1000 DM' },
      { code: 'A64', label: '1000 DM lub więcej' },
      { code: 'A65', label: 'nieznane / brak konta oszczędnościowego' },
    ],
  },
  {
    attribute: 'Attribute7',
    question: 'Obecne zatrudnienie od:',
    type: 'select',
    options: [
      { code: 'A71', label: 'bezrobotny' },
      { code: 'A72', label: 'mniej niż 1 rok' },
      { code: 'A73', label: 'od 1 do 4 lat' },
      { code: 'A74', label: 'od 4 do 7 lat' },
      { code: 'A75', label: '7 lat lub więcej' },
    ],
  },
  {
    attribute: 'Attribute8',
    question: 'Rata w procentach dochodu rozporządzalnego:',
    type: 'number',
    unit: '%',
  },
  {
    attribute: 'Attribute9',
    question: 'Status osobisty i płeć:',
    type: 'select',
    options: [
      { code: 'A91', label: 'mężczyzna : rozwiedziony/w separacji' },
      { code: 'A92', label: 'kobieta : rozwiedziona/w separacji/zamężna' },
      { code: 'A93', label: 'mężczyzna : kawaler' },
      { code: 'A94', label: 'mężczyzna : żonaty/wdowiec' },
      { code: 'A95', label: 'kobieta : panna' },
    ],
  },
  {
    attribute: 'Attribute10',
    question: 'Inni dłużnicy / poręczyciele:',
    type: 'select',
    options: [
      { code: 'A101', label: 'brak' },
      { code: 'A102', label: 'współwnioskodawca' },
      { code: 'A103', label: 'poręczyciel' },
    ],
  },
  {
    attribute: 'Attribute11',
    question: 'Obecne miejsce zamieszkania od (w latach):',
    type: 'number',
    unit: 'lata',
  },
  {
    attribute: 'Attribute12',
    question: 'Własność:',
    type: 'select',
    options: [
      { code: 'A121', label: 'nieruchomość' },
      { code: 'A122', label: 'umowa oszczędnościowo-budowlana / ubezpieczenie na życie' },
      { code: 'A123', label: 'samochód lub inne (nie w atrybucie 6)' },
      { code: 'A124', label: 'nieznane / brak własności' },
    ],
  },
  {
    attribute: 'Attribute13',
    question: 'Wiek (w latach):',
    type: 'number',
    unit: 'lata',
  },
  {
    attribute: 'Attribute14',
    question: 'Inne plany ratalne:',
    type: 'select',
    options: [
      { code: 'A141', label: 'bank' },
      { code: 'A142', label: 'sklepy' },
      { code: 'A143', label: 'brak' },
    ],
  },
  {
    attribute: 'Attribute15',
    question: 'Mieszkanie:',
    type: 'select',
    options: [
      { code: 'A151', label: 'wynajem' },
      { code: 'A152', label: 'własne' },
      { code: 'A153', label: 'za darmo' },
    ],
  },
  {
    attribute: 'Attribute16',
    question: 'Liczba istniejących kredytów w tym banku:',
    type: 'number',
  },
  {
    attribute: 'Attribute17',
    question: 'Praca:',
    type: 'select',
    options: [
      { code: 'A171', label: 'bezrobotny / niewykwalifikowany - nierezydent' },
      { code: 'A172', label: 'niewykwalifikowany - rezydent' },
      { code: 'A173', label: 'wykwalifikowany pracownik / urzędnik' },
      { code: 'A174', label: 'menedżer / samozatrudniony / wysoko wykwalifikowany / oficer' },
    ],
  },
  {
    attribute: 'Attribute18',
    question: 'Liczba osób na utrzymaniu:',
    type: 'number',
  },
  {
    attribute: 'Attribute19',
    question: 'Telefon:',
    type: 'select',
    options: [
      { code: 'A191', label: 'brak' },
      { code: 'A192', label: 'tak, zarejestrowany na nazwisko klienta' },
    ],
  },
  {
    attribute: 'Attribute20',
    question: 'Pracownik zagraniczny:',
    type: 'select',
    options: [
      { code: 'A201', label: 'tak' },
      { code: 'A202', label: 'nie' },
    ],
  },
];
