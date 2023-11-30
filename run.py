

from myappPackage import app










# @app.route('/insert',methods=['GET','POST'])
# def insert():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         mydata = Data(name,email,phone)
#         db.session.add(mydata)
#         db.session.commit()
#         return redirect(url_for('index'))
#     return render_template('insert.html')

# @app.route('/testing/<id>')
# def displayuser(id):
#     mydata = Data.query.get(id)
#     return render_template('display.html',mydata=mydata)
    


if __name__ == "__main__":
    app.run(debug=True)