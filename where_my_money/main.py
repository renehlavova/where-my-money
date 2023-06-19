"""Main entrypoint for the where-my-money package"""
import logging

logger = logging.getLogger(__name__)


def main():
    """Main entrypoint"""
    logging.basicConfig(level=logging.INFO)
    # Add your actual code here
    logger.info("This package does nothing")


if __name__ == "__main__":
    main()
