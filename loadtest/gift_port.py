# -*- coding: utf-8 -*-
import os
from gift_press import GiftPress,User
from flask import Flask, request
from gevent import pywsgi
from flask_cors import CORS
import json
from threading import Thread

Gift = GiftPress
user = User
user.tasks = [Gift]
app=Flask(__name__)

@app.route("/livetool/createTask", methods=["GET"])
def check():

    return_data= {'errno': '0', 'errmsg': '处理成功'}
    if not request.args.to_dict():
        return_data['errno'] = '5004'
        return_data['errmsg'] = '请求参数为空'
        return json.dumps(return_data, ensure_ascii=False)
    try:
        recieve_data=request.args.to_dict()
        # http://0.0.0.0:8080/livetool/createTask?room_id=4051407545&uid=687275812&gids=11103&client_num=1&hatch_rate=1&expire=10
        room_id = recieve_data.get('room_id').strip()
        uid = recieve_data.get('uid').strip()
        gift_id = recieve_data.get('gids').strip()
        urs = recieve_data.get('client_num').strip()
        fqe = recieve_data.get('hatch_rate').strip()
        tm = recieve_data.get('expire').strip()
        gift_name = recieve_data.get('gift_name').strip()
        if room_id and uid and gift_id and urs and fqe and tm and gift_name:
            # do somethings
            print(f'http://x.x.x.x:8080/livetool/createTask?room_id={room_id}&uid={uid}&gids={gift_id}&client_num={urs}&hatch_rate={fqe}&expire={tm}&gift_name={gift_name}')
            t1 = Thread(target=main, args=(room_id, uid, gift_id, urs, fqe, tm, gift_name))
            t1.start()

            get_pid = 'ps -ef | grep locust'
            pid_data = os.popen(get_pid).read()
            # 不同操作系统解析数据方式不同
            pid_list = pid_data.split('\n')[-4].split(' ')
            print(pid_list)
            pid = [i for i in pid_list if i][1]
            return_data['result'] = True
            return_data['pid'] = pid
            return json.dumps(return_data, ensure_ascii=False)
        else:
            return_data['errno'] = 10001
            return_data['errmsg'] = '输入参数不全或输入参数错误'
            return_data['result'] = False
            return json.dumps(return_data, ensure_ascii=False)
    except Exception as e:
        return_data['errno'] = 10002
        return_data['errmsg'] = '程序处理发生异常'
        return_data['result'] = False
        print(e)
        return json.dumps(return_data, ensure_ascii=False)

@app.route("/livetool/stopTask", methods=["GET"])
def stop():
    return_data= {'errno': '0', 'errmsg': '处理成功'}
    if not request.args.to_dict():
        return_data['errno'] = '5004'
        return_data['errmsg'] = '请求参数为空'
        return json.dumps(return_data, ensure_ascii=False)
    try:
        recieve_data=request.args.to_dict()
        pid = recieve_data.get('pid')
        if pid:
            # do somethings
            cmd = f'kill -9 {int(pid)}'
            os.popen(cmd).read()
            return_data['result'] = True
            return json.dumps(return_data, ensure_ascii=False)
        else:
            return_data['errno'] = 10003
            return_data['errmsg'] = '空进程号'
            return_data['result'] = False
            return json.dumps(return_data, ensure_ascii=False)
    except Exception as e:
        return_data['errno'] = 10004
        return_data['errmsg'] = '无法结束此进程'
        return_data['result'] = False
        print(e)
        return json.dumps(return_data, ensure_ascii=False)

def main(room_id, uid, gift_id, urs, fqe, tm, gift_name):
    room_id = room_id
    uid = uid
    gid = gift_id
    gift_name = gift_name
    with open('data.txt','w') as f:
        f.write(room_id + ' ' + uid + ' ' + gid + ' ' + gift_name)

    cmd = f'locust -f gift_port.py --host=http://0.0.0.0:80 --headless -u {int(urs)} -r {int(fqe)} -t {int(tm)} &'
    os.system(cmd)

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 8080), app)
    CORS(app, supports_credentials=True)
    server.serve_forever()