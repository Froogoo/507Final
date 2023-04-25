from flask import Flask, Response,request, render_template, session, redirect
from typing import Any, Dict, Optional
import pandas as pd

app = Flask(__name__, static_url_path='/resource')
app.config["JSON_AS_ASCII"] = False

#initialize the database df
class customer:
    def __init__(self, name, business, age, phone_number, queue_num=None):
        self.name = name
        self.business = business
        self.age = age
        self.phone_number = phone_number
        self.queue_number = queue_num

global personal_queue
global business_queue
global priority_queue

personal_queue=[]
business_queue=[]
priority_queue=[]

zwt=customer('zwt','personal',23,'88893251','A001')
jly = customer('jly', 'company', 22, '88193251','A002')
wsb = customer('wsb', 'company', 22, '66193251','A003')

personal_queue.append(zwt)
personal_queue.append(jly)
personal_queue.append(wsb)

#my student info
@app.route('/')
def index():
    return 'Group A, Index G2200626G, Zhu Wentao'

def get_queue_num(queue):
    l = len(queue)
    if l==0:
        lst_num=0
    else:
        lst_num=queue[l-1].queue_number
        lst_num=int(lst_num[1:])
    queuenum=str(lst_num+1)
    while len(queuenum) < 3:
        queuenum = '0' + queuenum
    return l, queuenum

@app.route('/a/customer/add',methods=['GET'])
def add_product():
    customer_name=str(request.args.get('name'))
    customer_operation=str(request.args.get('operation'))
    customer_age = int(request.args.get('age'))
    customer_phone = str(request.args.get('pn'))
    new_customer = customer(customer_name, customer_operation, customer_age, customer_phone)
    if new_customer.business=='personal':
        if new_customer.age<50:
            ppl_ahead, num=get_queue_num(personal_queue)
            que_num='A'+num
            new_customer.queue_number=que_num
            personal_queue.append(new_customer)
        else:
            ppl_ahead, num = get_queue_num(priority_queue)
            que_num = 'P' + num
            new_customer.queue_number = que_num
            priority_queue.append(new_customer)
    else:
        ppl_ahead, num = get_queue_num(business_queue)
        que_num = 'B' + num
        new_customer.queue_number = que_num
        business_queue.append(new_customer)
    return 'Your queue number is %s, there are %d people waiting in front of you.' % (que_num, ppl_ahead)


if __name__ == '__main__':
    app.run()