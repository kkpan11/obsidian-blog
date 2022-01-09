import os
import dotenv

from lib.blog import get_posts, get_pages, get_layouts, render
from lib.helpers import make_dir, rm_dir, copy_dir

config = dotenv.dotenv_values('.env')

BLOG_TITLE = config['BLOG_TITLE']
DEST_DIR = config['DEST_DIR']
SOURCE_DIR = config['SOURCE_DIR']

LAYOUTS_DIR = os.path.join(SOURCE_DIR, '_layouts')
PAGES_DIR = os.path.join(SOURCE_DIR, '_pages')
ASSETS_DIR = os.path.join(SOURCE_DIR, '_assets')

# Clear prev build artefacts
rm_dir(DEST_DIR)
make_dir(DEST_DIR)
copy_dir(ASSETS_DIR, os.path.join(DEST_DIR, 'assets'))

print('Start a build')

# Parse layouts, pages, and posts
layouts = get_layouts(LAYOUTS_DIR)
posts = get_posts(SOURCE_DIR)
pages = get_pages(PAGES_DIR)

# Render pages
for page in pages:
    file = page['file']
    name = page['name']
    slug = page['slug']
    raw_content = page['raw_content']

    dest_file = os.path.join(DEST_DIR, slug)

    print('Render page:', file)
    print('  slug:', slug)

    content = render(raw_content, {
        'posts': posts,
        'title': BLOG_TITLE
    })

    layout = layouts['main']

    rendered_page = layout({
        'content': content,
        'title': BLOG_TITLE,
        'pages': pages,
    })

    with open(dest_file, 'a') as f:
        print(rendered_page, file=f)

# Render posts
for post in posts:
    file = post['file']
    meta = post['meta']
    html = post['html']
    slug = post['slug']

    print('Render post:', file)
    print('  slug:', slug)
    
    source_file = os.path.join(SOURCE_DIR, file)
    dest_file = os.path.join(DEST_DIR, slug)

    layout_name = meta['layout'][0]
    layout = layouts[layout_name] 

    rendered_post = layout({
        'title': meta['title'][0],
        'content': html,
        'pages': pages,
    })

    with open(dest_file, 'a') as f:
        print(rendered_post, file=f)

print('Done\n')