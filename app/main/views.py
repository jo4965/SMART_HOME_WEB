import time
import sys
from threading import Thread
from flask import stream_with_context, request, Response, redirect, url_for,\
render_template

from . import main_blueprint
from app.models import *
import datetime
import socket
import select


def connect_to_iot(ip, led_control_info):
	host = ip # Local host address
	port = 9009 # Medium port number
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		s.connect((host, port))
		s.send( led_control_info.encode('utf-8') )
		recv_buf = s.recv(1024)
	except:
		print('Unable to connect')
		sys.exit()

	return recv_buf
	print('Connected.')

@main_blueprint.route('/')
def index():
	dev_info = Device.query.filter_by(name="Smart Light").order_by(Device.timestamp.desc()).first()
	is_light_on = 0
	print(dev_info)
	if dev_info is not None :
		if dev_info.content == "Light On":
			is_light_on = 1
		else:
			is_light_on = 0

	dev_count = list()
	for i in range(4): # count the number of alarm types
		dev_count.append(Device.query.filter_by(alarm_type = i+1).count())

	return render_template("main/index.html", is_light_on = is_light_on, dev_count = dev_count)


@main_blueprint.route('/iot1', methods=['GET', 'POST'])
def data_upload():
	if request.method == 'POST':
	 dev_name = request.form['name']
	 print(dev_name)
	 dev_content = request.form['content']
	 dev_type = request.form['alarm_type']
	 dev_ip = request.form['IP_address']
	 timestamp = datetime.datetime.now().replace(microsecond=0)

	 dev_info = Device(dev_name, dev_content, dev_type, dev_ip, timestamp)
	 add_and_commit(db.session, dev_info)
	 return redirect(url_for("main.index"))

@main_blueprint.route("/led_on_off", methods=['POST'])
def led_on_off():
	if request.method == 'POST':
		led_switch = int(request.form['led_switch'])
		tmp_thr = Thread(target=connect_to_iot, args=(led_switch,))
		tmp_thr.start()
		return redirect(url_for("main.index"))


@main_blueprint.route("/smart_light_view")
def smart_light_view():
	return render_template("main/smart_light.html")

@main_blueprint.route("/smart_bar_view")
def smart_bar_view():
	return render_template("main/smart_bar.html")

@main_blueprint.route("/smart_door_view")
def smart_door_view():
	return render_template("main/smart_door.html")


@main_blueprint.route("/smart_feeder_view")
def smart_feeder_view():
	return render_template("main/smart_feeder.html")


@main_blueprint.route("/smart_plug_view")
def smart_plug_view():
	return render_template("main/smart_plug.html")


@main_blueprint.route("/smart_shield_view")
def smart_shield_view():
	return render_template("main/smart_shield.html")


@main_blueprint.route("/control_smart_light", methods=['POST'])
def control_smart_light():
	if request.method == 'POST':
		red = request.form['red_value']
		green = request.form['green_value']
		blue = request.form['blue_value']
		power = request.form['power']
		led_control_info = ['[', '8', 'mood', 'lighton', '4']
		led_control_info += [red, green, blue, power]
		led_control_info = '_'.join(led_control_info)

		tmp_thr = Thread(target=connect_to_iot, args=("192.168.43.44", led_control_info))
		tmp_thr.start()
		return redirect(url_for("main.smart_light_view"))


@main_blueprint.route("/control_smart_door", methods=['POST'])
def control_smart_door():
	if request.method == 'POST':

		do_open = request.form["do_open"]
		password = request.form["password"]
		door_ip = "128.199.244.247"
		
		door_control_info = [do_open, password]
		door_control_info = '_'.join(door_control_info)
		print(door_control_info)
		buf = connect_to_iot(door_ip, door_control_info)
		#tmp_thr = Thread(target=connect_to_iot, args=(door_ip, door_control_info))
		#tmp_thr.start()
		print(buf)
		return "0"

@main_blueprint.route("/control_smart_bar", methods=['POST'])
def control_smart_bar():
	if request.method == 'POST':
		
		bar_ip = "192.168.123.148"

		beverage = request.form["beverage"]
		position = request.form["position"]
		
		bar_control_info = ['[', '1', 'SmartBar', 'ORDER', '2', str(position), str(beverage), ']']
		bar_control_info = '_'.join(bar_control_info)
		print(bar_control_info)
		connect_to_iot(bar_ip, bar_control_info, recv_buf)
		#tmp_thr = Thread(target=connect_to_iot, args=(bar_ip, bar_control_info))
		#tmp_thr.start()
		print(recv_buf)
		return "0"

@main_blueprint.route("/control_smart_feeder", methods=['POST'])
def control_smart_feeder():
	if request.method == 'POST':
		time = request.form.getlist("time")
		print(time)
		feeder_ip = "127.0.0.1"
		feeder_control_info = time
		#feeder_control_info = '_'.join(feeder_control_info)
		#print(feeder_control_info)
		tmp_thr = Thread(target=connect_to_iot, args=(feeder_ip, feeder_control_info))
		tmp_thr.start()
		return "0"

@main_blueprint.route("/control_smart_alarm", methods=['POST'])
def control_smart_alarm():
	if request.method == 'POST':

		alarm_ip = "192.168.123.114"
		alarm_command = request.form["alarm_command"]
		
		if alarm_command == '1':
			alarm_text = request.form["alarm_text"]
		else:
			alarm_text = '0'

		alarm_control_info = '_'.join([alarm_command, alarm_text])
		tmp_thr = Thread(target=connect_to_iot, args= (alarm_ip, alarm_control_info ) )
		tmp_thr.start()

		# na jale also need to send to led
		if alarm_command =='3':
			led_control_info = "5\n"
			led_ip = "192.168.123.118"
			tmp_thr = Thread(target=connect_to_iot, args = (led_ip, led_control_info ) )
			tmp_thr.start()

		return "5"


from .static_view import *
