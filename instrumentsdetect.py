import pyvisa

def detect_and_log_instruments(filename='instruments.txt'):
    rm = pyvisa.ResourceManager()

    try:
        instruments = rm.list_resources()
    except Exception as e:
        print(f"Error listing resources: {e}")
        return

    with open(filename, 'w') as file:
        if not instruments:
            file.write("No instruments found.\n")
            print("No instruments found.")
            return

        for address in instruments:
            try:
                instrument = rm.open_resource(address)
                instrument.timeout = 2000  # 2 seconds
                idn = instrument.query("*IDN?").strip()
                file.write(f"{idn} : {address}\n")
                print(f"Detected: {idn} at {address}")
                instrument.close()
            except Exception as e:
                file.write(f"Error communicating with {address}: {e}\n")
                print(f"Error with {address}: {e}")

if __name__ == "__main__":
    detect_and_log_instruments()
