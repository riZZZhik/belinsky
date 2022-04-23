"""Belinsky TextAnalyzer nlp worker."""
from google.cloud import language_v1 as api
from google.oauth2.service_account import Credentials


class TextAnalyzer:
    """Belinsky TextAnalyzer nlp worker."""

    def __init__(self, google_service_credentials: dict):
        """Initialize the TextAnalyzer.

        Args:
            google_service_credentials (dict): Google Cloud credentials.
        """

        # Initialize Google Cloud NLP api client
        credentials = Credentials.from_service_account_info(google_service_credentials)
        self.client = api.LanguageServiceClient(credentials=credentials)

    @staticmethod
    def available_analyzis():
        """List of available analyzis."""
        return {"Classify text": "classify_text"}

    def classify_text(self, text: str) -> api.ClassifyTextResponse:
        """Classifies a document into categories."""
        document = self._create_document(text)

        return self.client.classify_text(document=document)

    @staticmethod
    def _create_document(text: str) -> api.Document:
        """Create a gRPC document from text.

        Args:
            text (str): Text to be converted to grpc Document.

        Returns:
            api.Document:
                Text converted to Google Cloud NLP request format.
        """

        return api.Document(content=text, type_=api.Document.Type.PLAIN_TEXT)
