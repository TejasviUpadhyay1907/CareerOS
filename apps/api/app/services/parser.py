"""Resume parser service for text extraction."""
import io
import re
from typing import Optional

from app.core.logging import get_logger

logger = get_logger(__name__)


class ParserService:
    """Service for parsing resume files and extracting text."""

    async def extract_text_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF file.

        Args:
            file_content: PDF file content as bytes

        Returns:
            Extracted text
        """
        try:
            import PyPDF2

            pdf_file = io.BytesIO(file_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            logger.info(f"Extracted {len(text)} characters from PDF")
            return self.clean_text(text)

        except Exception as e:
            logger.error(f"Failed to extract text from PDF: {e}")
            raise

    async def extract_text_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX file.

        Args:
            file_content: DOCX file content as bytes

        Returns:
            Extracted text
        """
        try:
            import docx

            doc = docx.Document(io.BytesIO(file_content))
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])

            logger.info(f"Extracted {len(text)} characters from DOCX")
            return self.clean_text(text)

        except Exception as e:
            logger.error(f"Failed to extract text from DOCX: {e}")
            raise

    def clean_text(self, text: str) -> str:
        """Clean extracted text.

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove special characters that might interfere
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)

        # Normalize line breaks
        text = re.sub(r"\n\s*\n", "\n\n", text)

        return text.strip()

    def detect_sections(self, text: str) -> dict[str, str]:
        """Detect sections in resume text.

        Args:
            text: Resume text

        Returns:
            Dictionary of section names and their content
        """
        sections = {}
        current_section = "summary"
        current_content = []

        # Common section headers
        section_patterns = {
            "experience": r"(?i)^(experience|work experience|professional experience|employment history)",
            "education": r"(?i)^(education|academic background|academic)",
            "skills": r"(?i)^(skills|technical skills|core competencies|technologies)",
            "projects": r"(?i)^(projects|portfolio|personal projects)",
            "certifications": r"(?i)^(certifications|certificates|credentials)",
            "languages": r"(?i)^(languages|language proficiency)",
            "achievements": r"(?i)^(achievements|accomplishments|awards)",
            "links": r"(?i)^(links|social|contact|github|linkedin)",
        }

        lines = text.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if this line is a section header
            matched_section = None
            for section, pattern in section_patterns.items():
                if re.match(pattern, line):
                    matched_section = section
                    break

            if matched_section:
                # Save previous section
                if current_content:
                    sections[current_section] = "\n".join(current_content)
                current_section = matched_section
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = "\n".join(current_content)

        logger.info(f"Detected {len(sections)} sections")
        return sections


# Global instance
parser_service = ParserService()
