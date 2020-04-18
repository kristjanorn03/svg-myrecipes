import os
import codecs
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader
#Lesa inn gögn úr markdown skrá
POSTS = {}
for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])


    POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}
#skilgreina template sem á að nota
env = Environment(loader=PackageLoader('main', 'templates'))
index_template = env.get_template('index.html')
bread_template = env.get_template('bread.html')
post_template = env.get_template('post.html')

index_html = index_template.render()

#setjum md í færibreytur posts og tags
posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [post['tags'] for post in posts_metadata]
bread_html = bread_template.render(posts=posts_metadata, tags=tags)

#ekki output heldur upp úr vinnumöppunni og í recipes möppuna
with open('../seinnakvikun-myrecipes-output/index.html', 'w',encoding="utf-8") as file:
    file.write(index_html)

with open('../seinnakvikun-myrecipes-output/bread.html', 'w',encoding="utf-8") as file:
    file.write(bread_html)

for post in POSTS:
    post_metadata = POSTS[post].metadata

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        "thumbnail": post_metadata["thumbnail"]
    }

    post_html = post_template.render(post=post_data)

    post_file_path = '../seinnakvikun-myrecipes-output/posts/{slug}.html'.format(slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)