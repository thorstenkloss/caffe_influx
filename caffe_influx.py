import telnetlib
import time
from influxdb import InfluxDBClient

influxServer = 'ServerIP or hostname'
influxPort = 8086
influxUser = 'Username'
influxPassword = 'Password'
influxDB = 'DBname'
ito = 'IP or hostname of ito module'


columns = {0: 'PID1: control type',
 1: 'PID1: temperature',
 2: 'PID1: setpoint',
 3: 'PID1: output',
 4: 'PID1: output, P term',
 5: 'PID1: output, I term',
 6: 'PID1: output, D term',
 7: 'PID1: output, feed forwards',
 8: 'PID1: dPV/dt',
 9: 'PID1: Kc setting',
 10: 'PID1: TI setting',
 11: 'PID1: TD setting',
 12: 'PID1: WG setting',
 13: 'PID1: average output',
 14: 'PID2: control type',
 15: 'PID2: temperature',
 16: 'PID2: setpoint',
 17: 'PID2: output',
 18: 'PID2: output, P term',
 19: 'PID2: output, I term',
 20: 'PID2: output, D term',
 21: 'PID2: output, feed forwards',
 22: 'PID2: dPV/dt',
 23: 'PID2: Kc setting',
 24: 'PID2: TI setting',
 25: 'PID2: TD setting',
 26: 'PID2: WG setting',
 27: 'PID2: average output',
 28: 'increment',
 29: 'volume',
 30: 'flow rate',
 31: 'flowmeter ticks',
 32: 'PCB sensor',
 33: 'aux 1 sensor',
 34: 'aux 2 sensor',
 35: 'aux 3 sensor',
 36: 'pressure',
 37: 'pressure setpoint',
 38: 'pressure band (minimum)',
 39: 'pressure band (maximum)',
 40: 'phase',
 41: 'phase (bias term)',
 42: 'phase (P term)',
 43: 'phase (I term)'}



 def setDB(res):
    meastime = int(time.time()*1000)
    for n in [1, 2, 3, 15, 16, 17, 29, 30, 36, 37]:
        if res[n] != '??.??':
            if ':' in columns[n]:
                s = columns[n].split(': ')
                tag = s[0]
                measurement = s[1]
            else:
                measurement = columns[n]
                tag = columns[n].split(' ')[0]

            json_body = [
                {
                    "measurement": measurement,
                    "tags": {
                        "type": tag
                    },
                    "time": meastime,
                    "fields": {
                        "value": float(res[n])
                    }
                }
            ]
            client.write_points(json_body, time_precision='ms')
            

main():
	while True:
		try:

			client = InfluxDBClient(influxServer, influxPort, influxUser, influxPassword, influxDB)
			tn = telnetlib.Telnet(ito, timeout=2)
			tn.write('MCr\r\n'.encode('utf-8'))
			count = 0
			tn.read_very_eager()
			while True:
				try:
					res = str(tn.read_until('\n'.encode('utf-8'), 2)).split(' ')[3:]
					if len(res) == 46:
						if res[36] != '??.??' or count%10 == 0:
							meastime = int(time.time()*1000)
							for n in [1, 2, 3, 15, 16, 17, 29, 30, 36, 37]:
								if res[n] != '??.??':
									if ':' in columns[n]:
										s = columns[n].split(': ')
										tag = s[0]
										measurement = s[1]
									else:
										measurement = columns[n]
										tag = columns[n].split(' ')[0]

									json_body = [
										{
											"measurement": measurement,
											"tags": {
												"type": tag
											},
											"time": meastime,
											"fields": {
												"value": float(res[n])
											}
										}
									]
									client.write_points(json_body, time_precision='ms')
						count += 1
					else:
						try:
							tn = telnetlib.Telnet(ito, timeout=2)
							tn.write('MCr\r\n'.encode('utf-8'))
						except:
							pass
				except:
					time.sleep(60)
		except:
			time.sleep(60)
			
if __name__ == '__main__':
	main()