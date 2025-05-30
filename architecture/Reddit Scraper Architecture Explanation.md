# Reddit Scraper Architecture Explanation

This document provides an explanation of the Reddit Scraper architecture for non-technical audiences.

## Overview

The Reddit Scraper is a sophisticated tool designed to automatically find potential marketing leads on Reddit. It works by:

1. Collecting relevant posts and comments from Reddit
2. Using AI (GPT models) to filter and analyze the content
3. Identifying high-value opportunities for a cron job scheduling service
4. Storing results in a database for review

## Key Components

### Core Components

- **Main Pipeline**: The central coordinator that manages the entire workflow
- **Reddit Scraper**: Collects posts and comments from Reddit based on configured criteria
- **GPT Filter**: Uses AI to determine which posts are relevant (first-pass filtering)
- **GPT Insight Extractor**: Uses more advanced AI to deeply analyze relevant posts and extract business insights
- **Batch API**: Efficiently processes multiple AI requests in batches to save costs
- **Database**: Stores all collected and processed data

### External Services

- **Reddit API**: The external service used to collect posts and comments
- **OpenAI API**: The external service that provides AI capabilities for filtering and analysis

### Supporting Modules

- **Configuration**: Manages settings and API keys
- **Logging System**: Records all activity for troubleshooting and monitoring
- **Cost Tracker**: Monitors and limits API spending to stay within budget
- **Rate Limiter**: Prevents overloading the Reddit API with too many requests
- **Subreddit Discovery**: Automatically finds new relevant communities to monitor
- **Helper Utilities**: Various support functions used throughout the system

### Data Storage

- **SQLite Database**: The main storage for all processed data
- **Batch Request Files**: Temporary storage for AI processing requests
- **Exploratory Subreddits**: List of newly discovered Reddit communities to monitor
- **Log Files**: Records of system activity and errors

## Data Flow

1. The system is triggered either manually by a user or automatically by the scheduler (daily at 8:00 UTC)
2. The main pipeline initializes the environment and loads configuration
3. The Reddit scraper collects posts from configured subreddits:
   - Checks history to avoid reprocessing
   - Uses rate limiting to avoid API restrictions
   - Discovers new subreddits to explore
   - Stores raw posts in the database
4. The GPT filter processes posts in batches:
   - Determines relevance scores
   - Updates the database with scores
5. The GPT insight extractor analyzes relevant posts:
   - Extracts business insights, tags, and ROI potential
   - Updates the database with detailed analysis

## Database Schema

The system uses four main database tables:

- **Posts**: Stores all collected posts and comments with their analysis results
- **History**: Tracks which posts have been processed to avoid duplication
- **Offers**: Stores marketing offers (appears to be for future functionality)
- **Content**: Stores generated content related to offers (appears to be for future functionality)

## Key Features

- **Automatic scheduling**: Runs daily without manual intervention
- **Cost control**: Monitors and limits API spending
- **Exploratory learning**: Automatically discovers new relevant communities
- **Efficient batch processing**: Processes multiple items at once for cost savings
- **Detailed insights**: Provides rich analysis of potential leads

This architecture enables the system to efficiently discover and analyze potential marketing leads on Reddit with minimal human intervention while maintaining cost controls.
