export interface QuestionRes {
  question: string;
  sentence: string;
  answer: string;
  source: string;
  source_documents: SourceDocument[];
}

export interface SourceDocument {
  page_content: string;
  lookup_str: string;
  metadata: Metadata;
  lookup_index: number;
}

export interface Metadata {
  audio_file: string;
  date: string;
  description: string;
  folder: string;
  guest: string;
  link: string;
  source: string;
  start: number;
  title: string;
  audio_url: string;
}
