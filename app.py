import random
from flask import Flask, render_template, abort  
from faker import Faker  

fake = Faker()
app = Flask(__name__)
application = app

images_ids = [
    '7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
    '2d2ab7df-cdbc-48a8-a936-35bba702def5',
    '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
    'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
    'cab5b7f2-774e-4884-a200-0c0180fa777f'
]

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = {
            'author': fake.name(),
            'text': fake.text()
        }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': fake.sentence(),
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': images_ids[i] + '.jpg',  # Изменена f-строка на конкатенацию
        'comments': generate_comments()
    }

posts_list = sorted(
    [generate_post(i) for i in range(len(images_ids))],
    key=lambda p: p['date'],
    reverse=True
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list)

@app.route('/posts/<int:index>')
def post(index):
    if 0 <= index < len(posts_list):
        p = posts_list[index]
        return render_template('post.html', title=p['title'], post=p)
    else:
        abort(404)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='Страница не найдена'), 404

if __name__ == '__main__':
    app.run(debug=True)
