class customer:
    def __init__(self, name, service, email, branch=None, queue_num=None, status='Waiting'):
        self.name = name
        self.service = service
        self.email = email
        self.branch = branch
        self.queue_number = queue_num
        self.status = status

global personal_queue
global business_queue
global priority_queue

global branch_num

branch_num = 0

personal_queue=[[],[],[]]
business_queue=[[],[],[]]
priority_queue=[[],[],[]]

zwt = customer('zwt','personal','email',branch='1',queue_num='A001M')
jly = customer('jly', 'personal', 'email',branch='1',queue_num='A002M')
wsb = customer('wsb', 'personal', 'email',branch='1',queue_num='A003')

zwt.status='Ongoing'

personal_queue[0].append(zwt)
personal_queue[0].append(jly)
personal_queue[0].append(wsb)

print(personal_queue[0][0].status)

# def get_queue_num(queue, branch_num): #烦死了！！
#     l = len(queue[branch_num])
#     print(l)
#     if l==0:
#         lst_num=0
#         queuenum = "01" #如果前面没人01开始
#     else:
#         i=l-1
#         queuenum='01'
#         while i>=0:
#             temp_customer=queue[branch_num][i]
#             if len(temp_customer.queue_number)==4:
#                 lst_num = temp_customer.queue_number
#                 lst_num = int(lst_num[1:])
#                 queuenum = str(lst_num + 1)
#                 break
#             i=i-1
#     while len(queuenum) < 3:
#         queuenum = '0' + queuenum
#     return l, queuenum
#
# print(get_queue_num(personal_queue,0))