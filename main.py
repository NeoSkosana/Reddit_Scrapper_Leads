# main.py

import os
import sys
from src.scrapers.offer_scraper import OfferScraper
from src.generators.content_generator import ContentGenerator
from config.config_loader import get_config
from db.writer import DatabaseWriter
from utils.logger import setup_logger
from db.schema import create_tables
from scheduler.cost_tracker import initialize_cost_tracking
from utils.helpers import ensure_directory_exists

def main():
    # Load config
    config = get_config()
    
    # Initialize components
    offer_scraper = OfferScraper()
    content_gen = ContentGenerator(config['api_keys']['deepseek'])
    db_writer = DatabaseWriter()
    
    # Get top offers
    top_offers = offer_scraper.get_top_offers(limit=10)
    
    for offer in top_offers:
        # Generate content
        article = content_gen.generate_linkedin_article(offer)
        reddit_post = content_gen.generate_reddit_post({
            'tool_name': offer['name'],
            'article_link': article['url']
        })
        
        # Store in database
        db_writer.save_content({
            'offer': offer,
            'article': article,
            'reddit_post': reddit_post
        })


def setup_environment():
    """Initialize the environment for the application."""
    log = setup_logger()
    log.info("Setting up environment...")

    ensure_directory_exists("data")
    ensure_directory_exists("data/batch_responses")
    ensure_directory_exists("logs")

    try:
        create_tables()
        log.info("Database initialized.")
    except Exception as e:
        log.error(f"Failed to initialize database: {str(e)}")
        return False

    try:
        initialize_cost_tracking()
        log.info("Cost tracking initialized.")
    except Exception as e:
        log.error(f"Failed to initialize cost tracking: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    log = setup_logger()
    log.info("\U0001F680 Starting Cronlytic Reddit scraping pipeline...")

    if not setup_environment():
        log.error("Failed to set up environment. Exiting.")
        sys.exit(1)

    try:
        run_daily_pipeline()
        log.info("\u2705 Pipeline completed successfully.")
    except KeyboardInterrupt:
        log.info("Pipeline interrupted by user.")
    except Exception as e:
        log.error(f"Pipeline failed: {str(e)}")
        sys.exit(1)
