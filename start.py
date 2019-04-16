# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 20:23:34 2018

@author: ROSS
"""

import sqlite3
from flask import Flask, render_template, url_for, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
bootstrap = Bootstrap(app)

class NameForm(FlaskForm):
    name = StringField("你的名字", validators=[DataRequired()])
    tag = SelectField(
        label='想去的地方',
        validators=[DataRequired('请选择标签')],
        choices=[(1, '杭州'), (2, '湖州'), (3, '苏州'), (4, '北京'), (5, '香港')],
        coerce=int 
    )
    tag1 = SelectField(
        label='时间安排',
        validators=[DataRequired('请选择标签')],
        choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), \
                 (5, '星期五'), (6, '星期六'), (7, '星期日')],
        coerce=int 
    )
    suggesstions = StringField("其它建议?", validators=[])
    submit = SubmitField("Submit")
    
@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    time = None
    place= None
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['time'] = form.tag1.choices[form.tag1.data-1][1]
        session['place']= form.tag.choices[form.tag.data-1][1]
        form.name.data = ""

        conn = sqlite3.connect('travel_data.db')
        query = 'INSERT INTO travel VALUES (?,?,?)'
        value = [(session['name'], session['place'], session['time'])]
        conn.cursor().executemany(query, value)
        conn.commit()
        conn.close()
        #return redirect('')
        
        return redirect(url_for('my_echart'))#Post/重定向/Get请求,可是如果用session的话，刚进入网址就不会有Stranger了
    return render_template("tst_form.html", form=form, name=session.get('name'), place=session.get('place'), time=session.get('time'))

@app.route("/submissions", methods=["GET", "POST"])
def submissions():
    print('as')
    return render_template("sub.html")

@app.route('/charts')
def my_echart():
#在浏览器上渲染my_templaces.html模板
    time1=0;time2=0;time3=0;time4=0;time5=0;time6=0;time7=0;
    place1=0;place2=0;place3=0;place4=0;place5=0;
    conn = sqlite3.connect('travel_data.db')
    values = list(conn.cursor().execute('SELECT * FROM travel'))
    place1 = (conn.cursor().execute("SELECT count(place) FROM travel where place='杭州'").fetchall())[0][0]
    place2 = (conn.cursor().execute("SELECT count(place) FROM travel where place='湖州'").fetchall())[0][0]
    place3 = (conn.cursor().execute("SELECT count(place) FROM travel where place='苏州'").fetchall())[0][0]
    place4 = (conn.cursor().execute("SELECT count(place) FROM travel where place='北京'").fetchall())[0][0]
    place5 = (conn.cursor().execute("SELECT count(place) FROM travel where place='香港'").fetchall())[0][0]
    time1 = (conn.cursor().execute("SELECT count(time) FROM travel where time='星期一'").fetchall())[0][0]
    time2 = (conn.cursor().execute("SELECT count(time) FROM travel where time='星期二'").fetchall())[0][0]
    time3 = (conn.cursor().execute("SELECT count(time) FROM travel where time='星期三'").fetchall())[0][0]
    time4 = (conn.cursor().execute("SELECT count(time) FROM travel where time='星期四'").fetchall())[0][0]
    time5 = (conn.cursor().execute("SELECT count(time) FROM travel where time='星期五'").fetchall())[0][0]
    time6 = (conn.cursor().execute("SELECT count(time) FROM travel where time='星期六'").fetchall())[0][0]
    time7 = (conn.cursor().execute("SELECT count(time) FROM travel where time='星期日'").fetchall())[0][0]
    conn.close()

    return render_template('charts.html', place1=place1, place2=place2, place3=place3, place4=place4, place5=place5, \
        time1=time1, time2=time2, time3=time3, time4=time4, time5=time5, time6=time6, time7=time7)

if __name__ == "__main__":
	app.run(debug=True)



