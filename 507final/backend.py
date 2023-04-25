from flask import Flask, Response, request, render_template, session, redirect
from typing import Any, Dict, Optional


app = Flask(__name__) #, static_url_path='/resource')
app.config["JSON_AS_ASCII"] = False

#initialize the database df
class customer:
    def __init__(self, name, service, email, branch=None, queue_num=None, status='Waiting'):
        self.name = name
        self.service = service
        self.email = email
        self.branch = branch
        self.queue_number = queue_num
        self.status = status

id_lst = ['','','']
service_lst = ['','','']
queue_num_call_list = ['','','']

personal_queue=[[],[],[]]
business_queue=[[],[],[]]
priority_queue=[[],[],[]]

missing_queue = [[],[],[]]
completed_queue = [[],[],[]]

system_status = ['Continue','Continue','Continue']

zwt = customer('zwt', 'personal', 'zwt@gmail.com', branch='east', queue_num='A001', status='Waiting')
yly = customer('yly', 'personal', 'yly@outlook.com', branch='east', queue_num='A002', status='Waiting')
ldr = customer('ldr', 'personal', 'ldr@outlook.com', branch='east', queue_num='A003', status='Waiting')
lzl = customer('lzl', 'business', 'lzl@gmail.com', branch='east', queue_num='B001', status='Waiting')
zhq = customer('zhq', 'business', 'zhq@gmail.com', branch='east', queue_num='B002', status='Waiting')
lmk = customer('lmk', 'business', 'lmk@outlook.com', branch='east', queue_num='B003', status='Waiting')
hrj = customer('hrj', 'priority', 'hrj@outlook.com', branch='east', queue_num='P001', status='Waiting')
njm = customer('njm', 'priority', 'njm@gmail.com', branch='east', queue_num='P002', status='Waiting')
ldn = customer('ldn', 'priority', 'ldn@gmail.com', branch='east', queue_num='P003', status='Waiting')

# West
ldh = customer('ldh', 'personal', 'ldh@outlook.com', branch='west', queue_num='A004', status='Waiting')
pjs = customer('pjs', 'personal', 'pjs@gmail.com', branch='west', queue_num='A005', status='Waiting')
zcl = customer('zcl', 'personal', 'zcl@outlook.com', branch='west', queue_num='A006', status='Waiting')
ltr = customer('ltr', 'business', 'ltr@gmail.com', branch='west', queue_num='B007', status='Waiting')
lty = customer('lty', 'business', 'lty@outlook.com', branch='west', queue_num='B008', status='Waiting')
jhn = customer('jhn', 'business', 'jhn@gmail.com', branch='west', queue_num='B009', status='Waiting')
wtl = customer('wtl', 'priority', 'wtl@gmail.com', branch='west', queue_num='P001', status='Waiting')
nky = customer('nky', 'priority', 'nky@gmail.com', branch='west', queue_num='P002', status='Waiting')
kjw = customer('kjw', 'priority', 'kjw@outlook.com', branch='west', queue_num='P003', status='Waiting')

# North
lyy = customer('lyy', 'personal', 'lyy@gmail.com', branch='north', queue_num='A010', status='Waiting')
xdj = customer('xdj', 'personal', 'xdj@outlook.com', branch='north', queue_num='A011', status='Waiting')
hgh = customer('hgh', 'personal', 'hgh@outlook.com', branch='north', queue_num='A012', status='Waiting')
qk = customer('qk', 'business', 'qk@gmail.com', branch='north', queue_num='B007', status='Waiting')
ten = customer('ten', 'business', 'ten@outlook.com', branch='north', queue_num='B008', status='Waiting')
dsc = customer('dsc', 'business', 'dsc@outlook.com', branch='north', queue_num='B009', status='Waiting')
jcc = customer('jcc', 'priority', 'jcc@gmail.com', branch='north', queue_num='P004', status='Waiting')
sho = customer('sho', 'priority', 'sho@gmail.com', branch='north', queue_num='P005', status='Waiting')
han = customer('han', 'priority', 'han@outlook.com', branch='north', queue_num='P006', status='Waiting')

personal_queue[0].append(zwt)
personal_queue[0].append(yly)
personal_queue[0].append(ldr)
business_queue[0].append(lzl)
business_queue[0].append(zhq)
business_queue[0].append(lmk)
priority_queue[0].append(hrj)
priority_queue[0].append(njm)
priority_queue[0].append(ldn)

personal_queue[1].append(ldh)
personal_queue[1].append(pjs)
personal_queue[1].append(zcl)
business_queue[1].append(ltr)
business_queue[1].append(lty)
business_queue[1].append(jhn)
priority_queue[1].append(wtl)
priority_queue[1].append(nky)
priority_queue[1].append(kjw)

personal_queue[2].append(lyy)
personal_queue[2].append(xdj)
personal_queue[2].append(hgh)
business_queue[2].append(qk)
business_queue[2].append(ten)
business_queue[2].append(dsc)
priority_queue[2].append(jcc)
priority_queue[2].append(sho)
priority_queue[2].append(han)



@app.route('/mobile')
def index():
    return render_template("mobile_welcome.html")

def get_queue_num(queue, branch_num):
    l = len(queue[branch_num])
    if l==0:
        lst_num=0
        queuenum = "01"
    else:
        i=l-1
        queuenum='01'
        while i >= 0:
            temp_customer=queue[branch_num][i]
            if len(temp_customer.queue_number)==4:
                lst_num = temp_customer.queue_number
                lst_num = int(lst_num[1:])
                queuenum = str(lst_num + 1)
                break
            i=i-1
    while len(queuenum) < 3:
        queuenum = '0' + queuenum
    return l, queuenum


@app.route('/mobile', methods=['POST'])
def add_customer():
    if request.method == 'POST':
        Branch_choice = request.form['Branch']
        to_branch = int(Branch_choice)
        customer_name = str(request.form.get('lname'))
        option = request.form['service']
        customer_operation = str(option)
        customer_email = str(request.form.get('email'))
        new_customer = customer(customer_name, customer_operation, customer_email,to_branch)
        if system_status[to_branch] == 'Continue':
            if new_customer.service=='personal':
                ppl_ahead, num = get_queue_num(personal_queue,to_branch)
                que_num='A'+num
                new_customer.queue_number=que_num
                personal_queue[to_branch].append(new_customer)

            elif new_customer.service == 'priority':
                ppl_ahead, num = get_queue_num(priority_queue,to_branch)
                que_num = 'P' + num
                new_customer.queue_number = que_num
                priority_queue[to_branch].append(new_customer)
            else:
                ppl_ahead, num = get_queue_num(business_queue,to_branch)
                que_num = 'B' + num
                new_customer.queue_number = que_num
                business_queue[to_branch].append(new_customer)
            result= f"Hello {customer_name}, your queue number is {que_num}, and there are {str(ppl_ahead)} people waiting in front of you."
            return render_template("mobile_welcome.html",output_queue=result)
        else:
            if to_branch==0:
                branch_name='East'
            elif to_branch==1:
                branch_name='West'
            else:
                branch_name='North'
            result = 'Sorry, there are already too many people in ' + branch_name + 'Branch. You may wait and get a queue number later or try other branches.'
            return render_template("mobile_welcome.html", output_queue=result)

@app.route('/walkin/<branch>')
def index2(branch):
    return render_template("walkin_welcome.html", branch=branch)

@app.route('/walkin/<branch>', methods=['POST'])
def walkin_add(branch):
    if branch == 'east':
        to_branch = 0
    elif branch == 'west':
        to_branch = 1
    else:
        to_branch = 2
    if request.method == 'POST':
        customer_name = str(request.form.get('lname'))
        option = request.form['service']
        customer_operation = str(option)
        customer_email = str(request.form.get('email'))
        new_customer = customer(customer_name, customer_operation, customer_email,to_branch)
        if system_status[to_branch] == 'Continue':
            if new_customer.service=='personal':
                ppl_ahead, num = get_queue_num(personal_queue,to_branch)
                que_num='A'+num
                new_customer.queue_number=que_num
                personal_queue[to_branch].append(new_customer)

            elif new_customer.service == 'priority':
                ppl_ahead, num = get_queue_num(priority_queue,to_branch)
                que_num = 'P' + num
                new_customer.queue_number = que_num
                priority_queue[to_branch].append(new_customer)
            else:
                ppl_ahead, num = get_queue_num(business_queue,to_branch)
                que_num = 'B' + num
                new_customer.queue_number = que_num
                business_queue[to_branch].append(new_customer)
            result= f"Hello {customer_name}, your queue number is {que_num}, and there are {str(ppl_ahead)} people waiting in front of you."
            return render_template("walkin_welcome.html",output_queue=result, branch=branch)
        else:
            if to_branch==0:
                branch_name='East'
            elif to_branch==1:
                branch_name='West'
            else:
                branch_name='North'
            result = 'Sorry, there are already too many people in ' + branch_name + 'Branch. You may wait and get a queue number later or try other branches.'
            return render_template("walkin_welcome.html", output_queue=result, branch=branch)


@app.route('/<branch>/qcro/qsearch', methods=['GET', 'POST'])
def searchMissing(branch):
    if request.method == "GET":
        qnum = str(request.args.get("queue_num"))
        update_status = str(request.args.get("status"))

        if branch == 'east':
            to_branch = 0
        elif branch == 'west':
            to_branch = 1
        else:
            to_branch = 2

        if update_status == "None":
            update_status = system_status[to_branch]
        system_status[to_branch] = update_status

        for customer_data in missing_queue[to_branch]:
            if qnum == customer_data.queue_number:
                customer_data.queue_number = customer_data.queue_number + 'M'
                customer_data.status = 'Waiting'
                if qnum[0] == 'A':
                    personal_queue[to_branch].insert(2, customer_data)
                elif qnum[0] == 'B':
                    business_queue[to_branch].insert(2, customer_data)
                else:
                    priority_queue[to_branch].insert(2, customer_data)
                missing_queue[to_branch].remove(customer_data)
                result = f"Queue Number {qnum} has been added in as {customer_data.queue_number}."
                return_sys_status = 'System now: ' + system_status[to_branch]
                return render_template("cro.html", personal=personal_queue[to_branch], business=business_queue[to_branch],
                                       priority=priority_queue[to_branch], check=result, niu=return_sys_status,
                                       branch=branch, len=len, max=max)
        result = f"{qnum} not in Missing Status."
        return_sys_status = 'System now: ' + system_status[to_branch]
        print(return_sys_status)
        return render_template("cro.html", personal=personal_queue[to_branch], business=business_queue[to_branch],
                               priority=priority_queue[to_branch], check=result, niu=return_sys_status, branch=branch,
                               len=len, max=max)

@app.route("/<branch>/screen")
def screen(branch):
    if branch == 'east':
        to_branch = 0
    elif branch == 'west':
        to_branch = 1
    else:
        to_branch = 2
    if queue_num_call_list[to_branch]=='':
        queue_call=''
    else:
        queue_call = f'{queue_num_call_list[to_branch]}, please come to {service_lst[to_branch]} service counter {id_lst[to_branch]}'

    if branch == 'east':
        personal_queue_branch = personal_queue[0]
        business_queue_branch = business_queue[0]
        priority_queue_branch = priority_queue[0]
    elif branch == 'west':
        personal_queue_branch = personal_queue[1]
        business_queue_branch = business_queue[1]
        priority_queue_branch = priority_queue[1]
    elif branch == 'north':
        personal_queue_branch = personal_queue[2]
        business_queue_branch = business_queue[2]
        priority_queue_branch = priority_queue[2]

    return render_template("screen.html", personal=personal_queue_branch, business=business_queue_branch, priority=priority_queue_branch,
                           len=len, max=max, branch=branch, queue_call=queue_call)


@app.route("/<branch>/counter/<service>/<int:id>")
def counter(branch, service, id):
    if branch == 'east':
        personal_queue_branch = personal_queue[0]
        business_queue_branch = business_queue[0]
        priority_queue_branch = priority_queue[0]
    elif branch == 'west':
        personal_queue_branch = personal_queue[1]
        business_queue_branch = business_queue[1]
        priority_queue_branch = priority_queue[1]
    elif branch == 'north':
        personal_queue_branch = personal_queue[2]
        business_queue_branch = business_queue[2]
        priority_queue_branch = priority_queue[2]

    return render_template("counter.html", personal=personal_queue_branch, business=business_queue_branch, priority=priority_queue_branch,
                           len=len, max=max, branch=branch, service=service, id=id)


@app.route("/<branch>/counter/<service>/<int:id>/next", methods=["POST"])
def next(branch, id, service):
    if branch == 'east':
        to_branch = 0
    elif branch == 'west':
        to_branch = 1
    else:
        to_branch = 2

    service_lst[to_branch] = service
    id_lst[to_branch] = id

    if branch == 'east':
        personal_queue_branch = personal_queue[0]
        business_queue_branch = business_queue[0]
        priority_queue_branch = priority_queue[0]
    elif branch == 'west':
        personal_queue_branch = personal_queue[1]
        business_queue_branch = business_queue[1]
        priority_queue_branch = priority_queue[1]
    elif branch == 'north':
        personal_queue_branch = personal_queue[2]
        business_queue_branch = business_queue[2]
        priority_queue_branch = priority_queue[2]

    if service == 'personal':
        sign = True

        for elements in personal_queue_branch:
            if elements.status == "Waiting":
                elements.status = "Ongoing"
                queue_number = elements.queue_number
                queue_num_call_list[to_branch] = queue_number
                sign = False
                break

        if sign == True:
            for elements in priority_queue_branch:
                if elements.status == "Waiting":
                    elements.status = "Ongoing"
                    queue_number = elements.queue_number
                    queue_num_call_list[to_branch] = queue_number
                    personal_queue_branch.append(elements)
                    priority_queue_branch.remove(elements)
                    break

    elif service == 'business':
        for elements in business_queue_branch:
            if elements.status == "Waiting":
                elements.status = "Ongoing"
                queue_number = elements.queue_number
                queue_num_call_list[to_branch] = queue_number
                break

    elif service == 'priority':
        sign = True

        for elements in priority_queue_branch:
            if elements.status == "Waiting":
                elements.status = "Ongoing"
                queue_number = elements.queue_number
                queue_num_call_list[to_branch] = queue_number
                sign = False
                break

        if sign == True:
            for elements in personal_queue_branch:
                if elements.status == "Waiting":
                    elements.status = "Ongoing"
                    queue_number = elements.queue_number
                    queue_num_call_list[to_branch] = queue_number
                    priority_queue_branch.append(elements)
                    personal_queue_branch.remove(elements)
                    break
    return render_template("counter.html", personal=personal_queue_branch, business=business_queue_branch, priority=priority_queue_branch,
                           len=len, max=max, branch=branch, service=service, id=id , queue_number=queue_number)


@app.route("/<branch>/counter/<service>/<int:id>/miss/<queue_number>", methods=["POST"])
def miss(branch, id, service, queue_number):
    if branch == 'east':
        personal_queue_branch = personal_queue[0]
        business_queue_branch = business_queue[0]
        priority_queue_branch = priority_queue[0]
        to_branch = 0
    elif branch == 'west':
        personal_queue_branch = personal_queue[1]
        business_queue_branch = business_queue[1]
        priority_queue_branch = priority_queue[1]
        to_branch = 1
    elif branch == 'north':
        personal_queue_branch = personal_queue[2]
        business_queue_branch = business_queue[2]
        priority_queue_branch = priority_queue[2]
        to_branch = 2

    if service == 'personal':
        for elements in personal_queue_branch:
            if elements.queue_number == queue_number:
                elements.status = "missing"
                personal_queue_branch.remove(elements)
                missing_queue[to_branch].append(elements)
                break

    elif service == 'business':
        for elements in business_queue_branch:
            if elements.queue_number == queue_number:
                elements.status = "missing"
                business_queue_branch.remove(elements)
                missing_queue[to_branch].append(elements)
                break

    elif service == 'priority':
        for elements in priority_queue_branch:
            if elements.queue_number == queue_number:
                elements.status = "missing"
                priority_queue_branch.remove(elements)
                missing_queue[to_branch].append(elements)
                break

    return render_template("counter.html", personal=personal_queue_branch, business=business_queue_branch, priority=priority_queue_branch,
                           len=len, max=max, branch=branch, service=service, id=id, queue_number = queue_number)


@app.route("/<branch>/counter/<service>/<int:id>/complete/<queue_number>", methods=["POST"])
def complete(branch, id, service, queue_number):
    if branch == 'east':
        personal_queue_branch = personal_queue[0]
        business_queue_branch = business_queue[0]
        priority_queue_branch = priority_queue[0]
        to_branch = 0
    elif branch == 'west':
        personal_queue_branch = personal_queue[1]
        business_queue_branch = business_queue[1]
        priority_queue_branch = priority_queue[1]
        to_branch = 1
    elif branch == 'north':
        personal_queue_branch = personal_queue[2]
        business_queue_branch = business_queue[2]
        priority_queue_branch = priority_queue[2]
        to_branch = 2

    if service == 'personal':
        for elements in personal_queue_branch:
            if elements.queue_number == queue_number:
                elements.status = "missing"
                personal_queue_branch.remove(elements)
                completed_queue[to_branch].append(elements)
                break

    elif service == 'business':
        for elements in business_queue_branch:
            if elements.queue_number == queue_number:
                elements.status = "missing"
                business_queue_branch.remove(elements)
                completed_queue[to_branch].append(elements)
                break

    elif service == 'priority':
        for elements in priority_queue_branch:
            if elements.queue_number == queue_number:
                elements.status = "missing"
                priority_queue_branch.remove(elements)
                completed_queue[to_branch].append(elements)
                break

    return render_template("counter.html", personal=personal_queue_branch, business=business_queue_branch, priority=priority_queue_branch,
                           len=len, max=max, branch=branch, service=service, id=id, queue_number = queue_number)

if __name__ == '__main__':
    app.run()
