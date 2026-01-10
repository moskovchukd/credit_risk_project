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
    question: 'What is the status of your existing checking account?',
    type: 'select',
    options: [
      { code: 'A11', label: 'Less than 0 DM' },
      { code: 'A12', label: '0 to 200 DM' },
      { code: 'A13', label: '200 DM or more / salary assignments for at least 1 year' },
      { code: 'A14', label: 'No checking account' },
    ],
  },
  {
    attribute: 'Attribute2',
    question: 'What is the duration of the credit in months?',
    type: 'number',
    unit: 'months',
  },
  {
    attribute: 'Attribute3',
    question: 'What is your credit history?',
    type: 'select',
    options: [
      { code: 'A30', label: 'No credits taken / all credits paid back duly' },
      { code: 'A31', label: 'All credits at this bank paid back duly' },
      { code: 'A32', label: 'Existing credits paid back duly till now' },
      { code: 'A33', label: 'Delay in paying off in the past' },
      { code: 'A34', label: 'Critical account / other credits existing (not at this bank)' },
    ],
  },
  {
    attribute: 'Attribute4',
    question: 'What is the purpose of the credit?',
    type: 'select',
    options: [
      { code: 'A40', label: 'Car (new)' },
      { code: 'A41', label: 'Car (used)' },
      { code: 'A42', label: 'Furniture/equipment' },
      { code: 'A43', label: 'Radio/television' },
      { code: 'A44', label: 'Domestic appliances' },
      { code: 'A45', label: 'Repairs' },
      { code: 'A46', label: 'Education' },
      { code: 'A48', label: 'Retraining' },
      { code: 'A49', label: 'Business' },
      { code: 'A410', label: 'Other' },
    ],
  },
  {
    attribute: 'Attribute5',
    question: 'What is the credit amount?',
    type: 'number',
    unit: 'DM',
  },
  {
    attribute: 'Attribute6',
    question: 'What is the status of your savings account/bonds?',
    type: 'select',
    options: [
      { code: 'A61', label: 'Less than 100 DM' },
      { code: 'A62', label: '100 to 500 DM' },
      { code: 'A63', label: '500 to 1000 DM' },
      { code: 'A64', label: '1000 DM or more' },
      { code: 'A65', label: 'Unknown / no savings account' },
    ],
  },
  {
    attribute: 'Attribute7',
    question: 'How long have you been employed at your current job?',
    type: 'select',
    options: [
      { code: 'A71', label: 'Unemployed' },
      { code: 'A72', label: 'Less than 1 year' },
      { code: 'A73', label: '1 to 4 years' },
      { code: 'A74', label: '4 to 7 years' },
      { code: 'A75', label: '7 years or more' },
    ],
  },
  {
    attribute: 'Attribute8',
    question: 'What is the installment rate as a percentage of disposable income?',
    type: 'number',
    unit: '%',
  },
  {
    attribute: 'Attribute9',
    question: 'What is your personal status and sex?',
    type: 'select',
    options: [
      { code: 'A91', label: 'Male : divorced/separated' },
      { code: 'A92', label: 'Female : divorced/separated/married' },
      { code: 'A93', label: 'Male : single' },
      { code: 'A94', label: 'Male : married/widowed' },
      { code: 'A95', label: 'Female : single' },
    ],
  },
  {
    attribute: 'Attribute10',
    question: 'Do you have other debtors or guarantors?',
    type: 'select',
    options: [
      { code: 'A101', label: 'None' },
      { code: 'A102', label: 'Co-applicant' },
      { code: 'A103', label: 'Guarantor' },
    ],
  },
  {
    attribute: 'Attribute11',
    question: 'How long have you been living at your current residence?',
    type: 'number',
    unit: 'years',
  },
  {
    attribute: 'Attribute12',
    question: 'What is your most valuable available asset?',
    type: 'select',
    options: [
      { code: 'A121', label: 'Real estate' },
      { code: 'A122', label: 'Building society savings agreement / life insurance' },
      { code: 'A123', label: 'Car or other' },
      { code: 'A124', label: 'Unknown / no property' },
    ],
  },
  {
    attribute: 'Attribute13',
    question: 'What is your age?',
    type: 'number',
    unit: 'years',
  },
  {
    attribute: 'Attribute14',
    question: 'Do you have other installment plans?',
    type: 'select',
    options: [
      { code: 'A141', label: 'Bank' },
      { code: 'A142', label: 'Stores' },
      { code: 'A143', label: 'None' },
    ],
  },
  {
    attribute: 'Attribute15',
    question: 'What is your housing situation?',
    type: 'select',
    options: [
      { code: 'A151', label: 'Rent' },
      { code: 'A152', label: 'Own' },
      { code: 'A153', label: 'For free' },
    ],
  },
  {
    attribute: 'Attribute16',
    question: 'How many existing credits do you have at this bank?',
    type: 'number',
  },
  {
    attribute: 'Attribute17',
    question: 'What is your job classification?',
    type: 'select',
    options: [
      { code: 'A171', label: 'Unemployed / unskilled - non-resident' },
      { code: 'A172', label: 'Unskilled - resident' },
      { code: 'A173', label: 'Skilled employee / official' },
      { code: 'A174', label: 'Management / self-employed / highly qualified / officer' },
    ],
  },
  {
    attribute: 'Attribute18',
    question: 'How many people are you liable to provide maintenance for?',
    type: 'number',
  },
  {
    attribute: 'Attribute19',
    question: 'Do you have a telephone registered under your name?',
    type: 'select',
    options: [
      { code: 'A191', label: 'No' },
      { code: 'A192', label: 'Yes' },
    ],
  },
  {
    attribute: 'Attribute20',
    question: 'Are you a foreign worker?',
    type: 'select',
    options: [
      { code: 'A201', label: 'Yes' },
      { code: 'A202', label: 'No' },
    ],
  },
];
