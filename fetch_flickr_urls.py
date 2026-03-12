import os
import sys
import flickrapi

# Set FLICKR_API_KEY and FLICKR_API_SECRET as environment variables before running
api_key = os.environ.get('FLICKR_API_KEY')
api_secret = os.environ.get('FLICKR_API_SECRET')

if not api_key or not api_secret:
    sys.exit(
        "Error: FLICKR_API_KEY and FLICKR_API_SECRET environment variables must be set.\n"
        "  export FLICKR_API_KEY=your_api_key\n"
        "  export FLICKR_API_SECRET=your_api_secret"
    )

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Function to fetch photo URLs
def fetch_photo_urls(tags, max_photos):
    urls = []
    page = 1
    per_page = 500  # Maximum allowed by Flickr

    while len(urls) < max_photos:
        photos = flickr.photos.search(tags=tags, per_page=per_page, page=page, extras='url_o')
        photos_page = photos['photos']['photo']
        
        if not photos_page:
            break
        
        for photo in photos_page:
            if 'url_o' in photo:
                urls.append(photo['url_o'])
        
        page += 1
        if len(urls) >= max_photos or page > photos['photos']['pages']:
            break

    return urls[:max_photos]

# Fetch photo URLs (e.g., with the tag 'nature')
photo_urls = fetch_photo_urls(tags='nature, city, landscape, sports, house', max_photos=6500)

# Save URLs to image_urls.txt
with open('image_urls.txt', 'w') as file:
    for url in photo_urls:
        file.write(url + '\n')

print(f'Saved {len(photo_urls)} URLs to image_urls.txt')
