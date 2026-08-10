import { api } from "@/lib/api";

export interface Citation {
  document_id: string;
  chunk_index: number;
}

export interface ChatRequest {
  question: string;
}

export interface ChatResponse {
  answer: string;
  citations: Citation[];
}

export const chatApi = {
  chatWithProject: async (projectId: string, question: string): Promise<ChatResponse> => {
    const res = await api.post(`/projects/${projectId}/chat`, { question });
    return res.data;
  },
};
