def read_template(path):
    with open(path) as template:
        return template.read()

def index():
    return read_template('templates/index.html')

def blog():
    return read_template('templates/blog.html')