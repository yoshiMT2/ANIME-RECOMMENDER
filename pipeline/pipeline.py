from config.config import get_settings
from src.recommender import AnimeRecommender
from src.vector_store import VectorStoreBuilder
from utils.exception import CustomException
from utils.logger import get_logger

logger = get_logger(__name__)


class AnimeRecommendationPipeline:
    def __init__(
        self,
        *,
        retriever=None,
        persist_dir: str = 'chroma_db',
        csv_path: str | None = None,
        k: int = 10,
    ):
        settings = get_settings()

        try:
            logger.info('Initializing Recommendation Pipeline')

            if retriever is None:
                if not csv_path and not persist_dir:
                    raise ValueError('Either csv_path or persist_dir must be provided')

                vetor_builder = VectorStoreBuilder(csv_path=csv_path, persist_dir=persist_dir)
                retriever = vetor_builder.load_vector_store().as_retriever(search_kwargs={'k': k})

            self.recommender = AnimeRecommender(
                retriever=retriever, api_key=settings.openai_api_key, model_name=settings.model_name
            )

            logger.info('Pipeline initialized successfully...')
        except Exception as e:
            logger.exception(f'Failed to initalize pipeline {str(e)}')
            raise CustomException('Error during pipeline initialization', e) from e

    def recommend(self, query: str) -> str:
        try:
            logger.info(f'Recieved a query {query}')
            recommendation = self.recommender.get_recommendation(query)
            logger.info('Recommendation generated succesfully...')
            return recommendation
        except Exception as e:
            logger.error(f'Failed to get recommendation {str(e)}')
            raise CustomException('Error during getting recommendation', e) from e
