# car-scraper

Web scraper for collecting JDM vehicle images 
Part of the AI Vehicle Identification project.

## Setup
pip install -r requirements.txt

## Usage
# Scrape images
scrapy crawl <spider_name>

# Clean dataset
python clean_images.py

# Augment
python augment_images.py

# Generate bounding boxes
python generate_bboxes.py

# Test
python test.py
python test_spider.py
python test_list.py

## Notes
- Images are saved to dataset/Make_Model/*.jpg
- Requires ~500MB RAM for Scrapy + CLIP pipeline
- CLIP phase requires GPU for reasonable speed