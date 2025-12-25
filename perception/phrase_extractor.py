"""
Phrase Extractor Module

Purpose: Extract phrases from text and create PEU (Perceptual Energy Unit)
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re
import hashlib
import math


@dataclass
class PEU:
    """Perceptual Energy Unit"""
    phrase: str
    I: float  # Intensity [0, 1]
    P: float  # Polarity [0, 1]
    S: float  # Stability [0, 1]
    H: float  # Entropy [0, 1]
    phase: float  # Phase [0, 2π]
    freq: float  # Frequency (Hz)
    role: str  # "goal" | "action" | "modifier" | "context"
    confidence: float  # Confidence [0, 1]
    energy: float  # Energy = I × |P| × S × (1 - H)


class PhraseExtractor:
    """
    Phrase extractor for text input.
    
    Extracts phrases and creates PEU (Perceptual Energy Unit) objects.
    """
    
    def __init__(self,
                 energy_threshold: float = 0.1,
                 max_phrase_length: int = 10,
                 language: str = "auto"):
        """
        Initialize phrase extractor.
        
        Args:
            energy_threshold: Minimum energy threshold for filtering
            max_phrase_length: Maximum tokens per phrase
            language: Language code ("auto", "th", "en", etc.)
        """
        self.energy_threshold = energy_threshold
        self.max_phrase_length = max_phrase_length
        self.language = language
        
        # Keyword dictionaries
        self.goal_markers = {
            "en": ["want", "need", "should", "must", "goal", "aim", "target", "objective"],
            "th": ["ต้องการ", "ต้อง", "ควร", "เป้าหมาย", "จุดมุ่งหมาย"]
        }
        
        self.action_markers = {
            "en": ["do", "make", "create", "build", "run", "execute", "perform", "action"],
            "th": ["ทำ", "สร้าง", "รัน", "ดำเนินการ", "ปฏิบัติ"]
        }
        
        self.modifier_markers = {
            "en": ["very", "quite", "really", "extremely", "slightly", "somewhat"],
            "th": ["มาก", "ค่อนข้าง", "จริงๆ", "มากๆ", "เล็กน้อย"]
        }
        
        self.positive_words = {
            "en": ["good", "great", "excellent", "positive", "happy", "nice", "wonderful"],
            "th": ["ดี", "เยี่ยม", "ดีมาก", "ยอดเยี่ยม", "ดีใจ", "สุข"]
        }
        
        self.negative_words = {
            "en": ["bad", "terrible", "negative", "sad", "awful", "horrible", "wrong"],
            "th": ["แย่", "ไม่ดี", "เลว", "เศร้า", "ผิด", "ร้าย"]
        }
        
        # Common words (for stability calculation)
        self.common_words = {
            "en": ["the", "a", "an", "is", "are", "was", "were", "be", "been", "have", "has", "had"],
            "th": ["ที่", "เป็น", "มี", "จะ", "ได้", "ใน", "ของ", "และ", "หรือ"]
        }
    
    def extract(self, text: str) -> List[PEU]:
        """
        Extract phrases from text and create PEU objects.
        
        Args:
            text: Input text string
        
        Returns:
            List of PEU objects sorted by energy (descending)
        """
        # 1. Tokenize
        tokens = self._tokenize(text)
        
        if not tokens:
            return []
        
        # 2. Detect phrase boundaries
        phrases = self._detect_phrase_boundaries(tokens)
        
        # 3. Create PEU for each phrase
        peu_list = []
        for phrase_tokens in phrases:
            phrase_text = " ".join(phrase_tokens)
            peu = self._create_peu(phrase_text, phrase_tokens)
            if peu:
                peu_list.append(peu)
        
        # 4. Filter by threshold
        filtered_peu = [
            peu for peu in peu_list
            if peu.energy >= self.energy_threshold
        ]
        
        # 5. Sort by energy (descending)
        filtered_peu.sort(key=lambda x: x.energy, reverse=True)
        
        return filtered_peu
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text.
        
        Supports English and Thai (basic).
        """
        if self.language == "th" or self._is_thai(text):
            return self._tokenize_thai(text)
        else:
            return self._tokenize_english(text)
    
    def _tokenize_english(self, text: str) -> List[str]:
        """Tokenize English text."""
        # Split by whitespace and punctuation
        tokens = re.findall(r'\b\w+\b', text.lower())
        return tokens
    
    def _tokenize_thai(self, text: str) -> List[str]:
        """
        Tokenize Thai text (basic implementation).
        
        Uses greedy word matching with common words.
        """
        # Basic implementation: split by spaces and common delimiters
        # In production, use proper Thai word segmentation
        tokens = re.findall(r'[\u0E00-\u0E7F]+|[a-zA-Z]+', text)
        return tokens
    
    def _is_thai(self, text: str) -> bool:
        """Check if text contains Thai characters."""
        return bool(re.search(r'[\u0E00-\u0E7F]', text))
    
    def _detect_phrase_boundaries(self, tokens: List[str]) -> List[List[str]]:
        """
        Detect phrase boundaries.
        
        Uses energy accumulation, continuity, boundary markers, and max length.
        """
        phrases = []
        current_phrase = []
        
        # Boundary markers
        boundary_markers = {
            "en": [",", ".", "!", "?", "and", "or", "but"],
            "th": ["และ", "หรือ", "แต่", "แล้ว", "ก็"]
        }
        
        lang = "th" if any(self._is_thai(token) for token in tokens) else "en"
        markers = boundary_markers.get(lang, [])
        
        for token in tokens:
            current_phrase.append(token)
            
            # Check for boundary
            is_boundary = (
                token in markers or
                len(current_phrase) >= self.max_phrase_length
            )
            
            if is_boundary and current_phrase:
                phrases.append(current_phrase[:])
                current_phrase = []
        
        # Add remaining tokens as phrase
        if current_phrase:
            phrases.append(current_phrase)
        
        return phrases
    
    def _create_peu(self, phrase: str, tokens: List[str]) -> Optional[PEU]:
        """
        Create PEU from phrase.
        
        Args:
            phrase: Phrase text
            tokens: List of tokens in phrase
        
        Returns:
            PEU object or None if invalid
        """
        if not tokens:
            return None
        
        lang = "th" if self._is_thai(phrase) else "en"
        
        # a. Compute Intensity
        I = self._compute_intensity(tokens, lang)
        
        # b. Compute Polarity
        P = self._compute_polarity(tokens, lang)
        
        # c. Compute Stability
        S = self._compute_stability(tokens, lang)
        
        # d. Compute Entropy
        H = self._compute_entropy(tokens)
        
        # e. Compute Phase
        phase = self._compute_phase(phrase)
        
        # f. Compute Frequency
        freq = self._compute_frequency(tokens, lang)
        
        # g. Classify Role
        role = self._classify_role(tokens, lang)
        
        # Compute Confidence
        confidence = S * (1.0 - H)
        
        # Compute Energy
        energy = I * abs(P) * S * (1.0 - H)
        
        return PEU(
            phrase=phrase,
            I=I,
            P=P,
            S=S,
            H=H,
            phase=phase,
            freq=freq,
            role=role,
            confidence=confidence,
            energy=energy
        )
    
    def _compute_intensity(self, tokens: List[str], lang: str) -> float:
        """
        Compute Intensity: I = min(len(tokens)/5.0 × emphasis, 1.0)
        """
        base_intensity = min(len(tokens) / 5.0, 1.0)
        
        # Check for emphasis markers
        emphasis = 1.0
        goal_markers = self.goal_markers.get(lang, [])
        action_markers = self.action_markers.get(lang, [])
        
        if any(token in goal_markers for token in tokens):
            emphasis = 1.3
        elif any(token in action_markers for token in tokens):
            emphasis = 1.2
        
        I = base_intensity * emphasis
        return min(1.0, I)
    
    def _compute_polarity(self, tokens: List[str], lang: str) -> float:
        """
        Compute Polarity: P = (pos_count - neg_count) / (pos_count + neg_count + 1)
        """
        pos_words = self.positive_words.get(lang, [])
        neg_words = self.negative_words.get(lang, [])
        
        pos_count = sum(1 for token in tokens if token in pos_words)
        neg_count = sum(1 for token in tokens if token in neg_words)
        
        total = pos_count + neg_count + 1
        P = (pos_count - neg_count) / total
        
        # Normalize to [0, 1] (original spec says [-1, 1], but we normalize)
        P_normalized = (P + 1.0) / 2.0
        
        return P_normalized
    
    def _compute_stability(self, tokens: List[str], lang: str) -> float:
        """
        Compute Stability: S = 0.5 + (common_words / total_words) × 0.3
        S -= 0.1 if len > 5 tokens
        """
        common_words = self.common_words.get(lang, [])
        common_count = sum(1 for token in tokens if token in common_words)
        total_words = len(tokens)
        
        if total_words == 0:
            return 0.5
        
        S = 0.5 + (common_count / total_words) * 0.3
        
        # Reduce stability for long phrases
        if len(tokens) > 5:
            S -= 0.1
        
        return max(0.0, min(1.0, S))
    
    def _compute_entropy(self, tokens: List[str]) -> float:
        """
        Compute Entropy: H = unique_ratio × 0.7 + 0.1
        """
        if not tokens:
            return 0.0
        
        unique_tokens = len(set(tokens))
        total_tokens = len(tokens)
        
        unique_ratio = unique_tokens / total_tokens if total_tokens > 0 else 0.0
        
        H = unique_ratio * 0.7 + 0.1
        
        return min(1.0, H)
    
    def _compute_phase(self, phrase: str) -> float:
        """
        Compute Phase: phase = (hash(phrase) % 1000) / 1000.0 × 2π
        """
        # Compute hash
        hash_obj = hashlib.md5(phrase.encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        
        # Normalize to [0, 1] then scale to [0, 2π]
        phase_normalized = (hash_int % 1000) / 1000.0
        phase = phase_normalized * 2.0 * math.pi
        
        return phase
    
    def _compute_frequency(self, tokens: List[str], lang: str) -> float:
        """
        Compute Frequency: freq = 40.0 (base) + adjustments
        """
        freq = 40.0
        
        goal_markers = self.goal_markers.get(lang, [])
        action_markers = self.action_markers.get(lang, [])
        
        if any(token in goal_markers for token in tokens):
            freq += 10.0
        elif any(token in action_markers for token in tokens):
            freq += 5.0
        
        return freq
    
    def _classify_role(self, tokens: List[str], lang: str) -> str:
        """
        Classify Role: goal | action | modifier | context
        """
        goal_markers = self.goal_markers.get(lang, [])
        action_markers = self.action_markers.get(lang, [])
        modifier_markers = self.modifier_markers.get(lang, [])
        
        if any(token in goal_markers for token in tokens):
            return "goal"
        elif any(token in action_markers for token in tokens):
            return "action"
        elif any(token in modifier_markers for token in tokens):
            return "modifier"
        else:
            return "context"

