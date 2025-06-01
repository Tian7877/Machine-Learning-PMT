export interface Email {
  subject: string;
  preview: string;
  body: string;
  label: "SPAM" | "HAM";
  confidence: number;
}
