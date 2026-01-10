export interface SurveyData {
  Attribute1: string;
  Attribute2: number;
  Attribute3: string;
  Attribute4: string;
  Attribute5: number;
  Attribute6: string;
  Attribute7: string;
  Attribute8: number;
  Attribute9: string;
  Attribute10: string;
  Attribute11: number;
  Attribute12: string;
  Attribute13: number;
  Attribute14: string;
  Attribute15: string;
  Attribute16: number;
  Attribute17: string;
  Attribute18: number;
  Attribute19: string;
  Attribute20: string;
}

export interface PredictionResult {
  prediction: number;
  probabilities: number[] | null;
  risk_level: string;
  decision: string;
  confidence: number;
}
