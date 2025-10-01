import snap7

def connect_to_plc(ip, rack, slot):
    client = snap7.client.Client()
    client.connect(ip, rack, slot)
    if client.get_connected():
        print("Povezava s Siemens PLC vzpostavljena.")
    return client

def test_read(client, db_number, start_address, size):
    try:
        data = client.db_read(db_number, start_address, size)
        print(f"Prebrani podatki: {list(data)}")
        return data
    except Exception as e:
        print(f"Napaka pri branju: {e}")

if __name__ == "__main__":
    PLC_IP = "192.168.0.1"  # IP naslov vašega PLC
    PLC_RACK = 0
    PLC_SLOT = 1

    client = connect_to_plc(PLC_IP, PLC_RACK, PLC_SLOT)

    try:
        # Test branja 10 bajtov iz DB1
        test_read(client, db_number=1, start_address=0, size=1)
    except Exception as e:
        print(f"Napaka: {e}")
    finally:
        client.disconnect()
        print("Povezava s Siemens PLC zaprta.")
