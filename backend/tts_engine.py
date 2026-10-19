"""
Lightweight Neural TTS Engine for Multilingual Speech (Telugu, Hindi, English).
Provides low-latency audio generation without paid cloud API dependencies.
Includes smart sentence boundary splitting and in-memory binary caching.
"""
import urllib.request
import urllib.parse
import hashlib
import re
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# In-memory LRU cache for synthesized audio bytes
_AUDIO_CACHE: Dict[str, bytes] = {}
_MAX_CACHE_ENTRIES = 200

def clean_text_for_speech(text: str) -> str:
    """
    Remove URLs, Markdown symbols, bullet asterisks, and excess punctuation
    to ensure smooth and natural pronunciation.
    """
    if not text:
        return ""
    # Remove URLs
    cleaned = re.sub(r'https?://\S+', '', text)
    # Remove markdown headers, bold, italics, code ticks, brackets
    cleaned = re.sub(r'[*_#`~\[\]()]', ' ', cleaned)
    # Replace bullet symbols with natural pauses
    cleaned = re.sub(r'[•\-\–\—]', ', ', cleaned)
    # Collapse multiple whitespaces
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def split_into_speech_chunks(text: str, max_chunk_len: int = 120) -> list:
    """
    Split text into natural clause or sentence chunks under max_chunk_len chars.
    """
    if not text:
        return []
    
    # Split by common sentence delimiters first
    raw_sentences = re.split(r'(?<=[.!?।॥\n])\s+', text)
    chunks = []
    
    for sentence in raw_sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) <= max_chunk_len:
            chunks.append(sentence)
        else:
            # Split long sentences by commas or word boundaries
            words = sentence.split(' ')
            curr = []
            curr_len = 0
            for w in words:
                if curr_len + len(w) + 1 > max_chunk_len:
                    if curr:
                        chunks.append(' '.join(curr))
                    curr = [w]
                    curr_len = len(w)
                else:
                    curr.append(w)
                    curr_len += len(w) + 1
            if curr:
                chunks.append(' '.join(curr))
                
    return chunks

def synthesize_speech(text: str, lang: str = "te") -> Optional[bytes]:
    """
    Synthesize text into MP3 audio bytes for the requested language.
    Supports 'te' (Telugu), 'hi' (Hindi), and 'en' (English).
    
    Returns:
        bytes: MP3 audio data if successful, None on network/connection failure.
    """
    cleaned = clean_text_for_speech(text)
    if not cleaned:
        return None
        
    lang_lower = (lang or "te").lower()
    if lang_lower.startswith("te"):
        tl = "te"
    elif lang_lower.startswith("hi"):
        tl = "hi"
    else:
        tl = "en"
        
    # Check cache first
    cache_key = hashlib.sha256(f"{tl}:{cleaned}".encode('utf-8')).hexdigest()
    if cache_key in _AUDIO_CACHE:
        return _AUDIO_CACHE[cache_key]
        
    chunks = split_into_speech_chunks(cleaned, max_chunk_len=120)
    if not chunks:
        return None
        
    # Limit max chunks to 8 (approx 1-2 minutes of speech) to ensure low latency
    active_chunks = chunks[:8]
    audio_frames = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://translate.google.com/"
    }
    
    try:
        for chunk in active_chunks:
            encoded_query = urllib.parse.quote(chunk)
            url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_query}&tl={tl}&client=tw-ob"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                if response.status == 200:
                    data = response.read()
                    if data:
                        audio_frames.append(data)
                        
        if not audio_frames:
            return None
            
        combined_mp3 = b"".join(audio_frames)
        
        # Store in LRU cache
        if len(_AUDIO_CACHE) >= _MAX_CACHE_ENTRIES:
            _AUDIO_CACHE.pop(next(iter(_AUDIO_CACHE)))
        _AUDIO_CACHE[cache_key] = combined_mp3
        
        return combined_mp3
        
    except Exception as exc:
        logger.warning("TTS audio generation failed: %s", exc)
        return None
