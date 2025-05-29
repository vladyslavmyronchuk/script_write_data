import serial
import serial.tools.list_ports
import json
import time

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description or "CH340" in port.description:
            return port.device
    return None

def main():
    port = find_arduino_port()
    if not port:
        print(" Arduino не знайдено.")
        return

    print(f" Знайдено Arduino  Mega на порту: {port}")
    ser = serial.Serial(port, 115200, timeout=2)
    time.sleep(2)  
    with open("data_filt.txt", "a") as logfile:
        while True:
            try:
                line = ser.readline().decode("utf-8").strip()
                if not line:
                    continue
                print("Отримано:", line)

              
                if line.startswith("{") and line.endswith("}"):
                    data = json.loads(line)
                    if data.get("errorFlags") == 0:
                        print("✅ Дані валідні, запис у файл.")
                        logfile.write(line + "\n")
                        logfile.flush()
                    else:
                        print("⚠️ Помилка в даних, не записуємо.")
            except Exception as e:
                print(" Помилка:", e)

if __name__ == "__main__":
    main()