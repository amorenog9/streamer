from time import sleep
import pandas as pd
import socket


def generator(data):
    deltas = data.delta.values
    data_rows = data.drop(columns=["delta"])
    for i in range(len(data)):
        sleep(deltas[i])
        yield data_rows.iloc[i].to_json()+"\n"


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("localhost",9090))
socket.listen()
while True:
    conn, addr = socket.accept()
    with conn:
        print(f"Connected by {addr}")
        g = generator(pd.read_feather("../data/anubis.feather"))
        for line in g:
            conn.send(line.encode())
