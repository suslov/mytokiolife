from flask import (render_template,
                   redirect,url_for,
                   request)
from app import app
from ..models import * 

@app.route('/')
@app.route('/index')
def index():
    contents = Content.get_newest()
    popular_post = Content.get_popular()
    return render_template("index.html",
                           contents=contents,
                           popular_post=popular_post)

@app.route('/archive/<int:blog_id>')
def archive(blog_id=None):
    blog_id = blog_id
    if blog_id is None:
        return redirect(url_for('/'))
    blog_content = Content.get_by_id(blog_id)
    relevant_content= blog_content.get_relevant()
    return render_template("archive.html",
                           blog_content=blog_content,
                           relevant_content=relevant_content)

@app.route('/ex_admin')
def exadmin_index():
    return render_template("admin.html")

@app.route('/ex_admin/post',methods=['POST'])
def post():
    title = request.form["title"]
    text = request.form["text"]
    Content.create(title,text,[])
    return redirect(url_for('/'))
