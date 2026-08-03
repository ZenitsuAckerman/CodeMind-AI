import re
from typing import List, Tuple
from transformers import AutoTokenizer

class ChunkingService:
    """
    Intelligent text chunker that preserves paragraph and sentence boundaries
    while respecting token limits (approx 500 tokens, 100 overlap).
    """
    
    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        # We load the tokenizer once when the service is instantiated
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_tokens = 500
        self.overlap_tokens = 100

    def count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text, add_special_tokens=False))

    def split_text(self, text: str) -> List[Tuple[str, int]]:
        """
        Splits text into chunks, returning a list of (chunk_text, token_count).
        """
        # Split by double newline to preserve paragraphs
        paragraphs = re.split(r'\n\s*\n', text)
        
        chunks = []
        current_chunk = ""
        current_token_count = 0
        
        # We will hold overlapping text here
        overlap_buffer = ""
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
                
            para_tokens = self.count_tokens(para)
            
            # If a single paragraph is too large, we must split it by sentences
            if para_tokens > self.max_tokens:
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                        
                    sentence_tokens = self.count_tokens(sentence)
                    
                    if current_token_count + sentence_tokens > self.max_tokens and current_chunk:
                        # Chunk is full, finalize it
                        chunks.append((current_chunk.strip(), current_token_count))
                        
                        # Start new chunk with overlap
                        current_chunk = overlap_buffer + " " + sentence if overlap_buffer else sentence
                        current_token_count = self.count_tokens(current_chunk)
                        
                        # Update overlap buffer
                        overlap_buffer = self._calculate_overlap(current_chunk)
                    else:
                        current_chunk = current_chunk + " " + sentence if current_chunk else sentence
                        current_token_count = self.count_tokens(current_chunk)
                        overlap_buffer = self._calculate_overlap(current_chunk)
                        
            else:
                # Fit the whole paragraph if possible
                if current_token_count + para_tokens > self.max_tokens and current_chunk:
                    # Finalize chunk
                    chunks.append((current_chunk.strip(), current_token_count))
                    
                    # Start new chunk with overlap
                    current_chunk = overlap_buffer + "\n\n" + para if overlap_buffer else para
                    current_token_count = self.count_tokens(current_chunk)
                    
                    overlap_buffer = self._calculate_overlap(current_chunk)
                else:
                    current_chunk = current_chunk + "\n\n" + para if current_chunk else para
                    current_token_count = self.count_tokens(current_chunk)
                    overlap_buffer = self._calculate_overlap(current_chunk)

        # Add the final chunk if it exists
        if current_chunk:
            chunks.append((current_chunk.strip(), current_token_count))

        return chunks

    def _calculate_overlap(self, text: str) -> str:
        """
        Extracts the last N tokens from the text to serve as the overlap buffer for the next chunk.
        Attempts to respect sentence boundaries by taking trailing sentences that fit within overlap_tokens.
        """
        sentences = re.split(r'(?<=[.!?])\s+', text)
        overlap_text = ""
        overlap_count = 0
        
        for sentence in reversed(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            sentence_tokens = self.count_tokens(sentence)
            if overlap_count + sentence_tokens > self.overlap_tokens:
                break
                
            overlap_text = sentence + " " + overlap_text
            overlap_count += sentence_tokens
            
        return overlap_text.strip()

# Singleton instance
chunking_service = ChunkingService()
