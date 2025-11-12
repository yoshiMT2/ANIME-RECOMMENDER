from src.data_loader import CSVDataLoader
from src.vector_store import VectorStoreBuilder
from utils.exception import CustomException
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    try:
        logger.info('Starting to build pipeline...')
        loader = CSVDataLoader('data/anime_with_synopsis.csv', 'data/anime_updated.csv')
        processed_csv = loader.load_and_process(['Name', 'Genres', 'Overview'])

        logger.info('Data loaded and processed...')

        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vectorstore()

        logger.info('Vector store built successfully...')

        logger.info('Pipeline built successfully...')
    except Exception as e:
        logger.error(f'Failed to execute pipeline {str(e)}')
        raise CustomException('Error during pipeline initialization', e) from e


if __name__ == '__main__':
    main()
