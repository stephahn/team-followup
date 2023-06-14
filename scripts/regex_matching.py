import re
import re
from typing import Type


class TextDetector:
    def __init__(self, regex_pattern: str, preceding_level: Type["TextDetector"]= None):
        """
        Initialize the TextDetector instance with a regex pattern.

        Args:
            regex_pattern (str): The regular expression pattern to detect.
        """
        self.regex_pattern = regex_pattern
        self.property = {}
        self.preceding_level = preceding_level
        self.html_balise = 'mark'
        self.color='red'

    def prepare_input_text(self, text: str) -> str:
        """
        Prepare the text for detection by clipping to the beginning of the previous detection if needed

        Args:
            text (str): The text to prepare.

        Returns:
            str: The prepared text.
        """
        if start_pos := self.property.get('start_pos', None):
            return text[start_pos:]
        if self.preceding_level:
            if start_pos := self.preceding_level.property.get('start_pos', None):
                return text[start_pos:]
        return text

    def prepare_output_text(self, original_text: str,text:str) -> str:
        """
        Output the full text
        :param text:
        :return: text
        """
        if start_pos := self.property.get('start_pos', None):
            return original_text[:start_pos] + text
        if self.preceding_level:
            if start_pos := self.preceding_level.property.get('start_pos', None):
                return original_text[:start_pos]+text
        return text
    def detect(self, text: str) -> list[str]:
        """
        Find all occurrences of the regex pattern in the given text.

        Args:
            text (str): The text to search for matches.

        Returns:
            list[str]: A list of matches found in the text.
        """
        text_to_proceed = self.prepare_input_text(text)
        return re.findall(self.regex_pattern, text_to_proceed, flags=re.IGNORECASE)
    def set_start_position(self, text):
        """
        Extract the text from the regex matches from the text.
        :return: str: The extracted text
        """
        if matches := re.finditer(self.regex_pattern, text, re.IGNORECASE):
            for match in matches:
                start_pos = match.start()
                self.property['start_pos'] = start_pos

    def highlight_html(self, text: str, ) -> str:
        """
        Highlight the regex matches in the text using HTML span elements.

        Args:
            text (str): The text to highlight.
            css_class (str, optional): The CSS class to apply to the highlighted matches. Defaults to 'highlight'.

        Returns:
            str: The text with the regex matches highlighted using HTML span elements.
        """
        css_class = 'highlight'
        text_to_proceed = self.prepare_input_text(text)

        highlithed = re.sub(self.regex_pattern, fr'<span class="{css_class}" style="color: {self.color}">\1</span>', text_to_proceed,
                            flags=re.IGNORECASE)
        return self.prepare_output_text(text, highlithed)


class RecommendationDetector(TextDetector):
    def __init__(self,preceding_level=None):
        """
        Initialize the RecommendationDetector instance.
        """
        super().__init__(r'\b(recommend|consider|recommendations)\b', preceding_level=preceding_level)
        self.html_balise = 'mark'
    def detect(self, text: str) -> list[str]:
        """
        Find all occurrences of the regex pattern in the given text.

        Args:
            text (str): The text to search for matches.

        Returns:
            list[str]: A list of matches found in the text.
        """
        matches = super().detect(text)
        if matches:
            self.set_start_position(text)
        return matches
    def highlight_html(self, text: str, ) -> str:
        """
        Highlight the regex matches in the text using HTML span elements.

        Args:
            text (str): The text to highlight.
            css_class (str, optional): The CSS class to apply to the highlighted matches. Defaults to 'highlight'.

        Returns:
            str: The text with the regex matches highlighted using HTML span elements.
        """
        text_to_proceed = self.prepare_input_text(text)
        highlithed = fr"<{self.html_balise} style='background-color: green; color: black;'>{text_to_proceed}</{self.html_balise}>"
        return self.prepare_output_text(text,highlithed)

class TimeFrameDetector(TextDetector):
    def __init__(self, preceding_level=None):
        """
        Initialize the ConclusionDetector instance.
        """
        super().__init__(r'(in\s+\d+-\d+\s+(?:weeks|months))',preceding_level=preceding_level)
        self.color = "blue"

class ModalityDetector(TextDetector):
    def __init__(self, preceding_level=None):
        """
        Initialize the ModalityDetector instance.
        """
        super().__init__(r'(CT|MRI|PET|X-ray)', preceding_level=preceding_level)
        self.color = "red"

class DetectorPipeline:
    def __init__(self):
        """
        Initialize the DetectorPipeline instance.
        """
        self.recommendation = RecommendationDetector()
        self.detectors = {}

    def add_detector(self, regex_pattern: str, name: str, color:str='red'):
        """
        Add a new detector to the pipeline.

        Args:
            regex_pattern (str): The regex pattern to use for the detector.
            name (str): The name of the detector.
        """
        detector = TextDetector(regex_pattern, preceding_level=self.recommendation)
        detector.color = color
        self.detectors[name] = detector
    def remove_detector(self, name: str):
        """
        Remove a detector from the pipeline.

        Args:
            name (str): The name of the detector to remove.
        """
        del self.detectors[name]
    def detect(self, text: str) -> dict[str, list[str]]:
        recommendation_matches = self.recommendation.detect(text)
        print(recommendation_matches)
        highlithed_text = self.recommendation.highlight_html(text)
        if recommendation_matches:
            for name, detector in self.detectors.items():
                if detector.detect(text):
                    highlithed_text = detector.highlight_html(highlithed_text)
        return highlithed_text




