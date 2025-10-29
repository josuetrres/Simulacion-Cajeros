import random

PAY_CARD = 15
PAY_CASH = 30

def calcular_tiempo(productos, tipo_pago, tipo_cajero):
    escaneo = productos * (5 if tipo_cajero == "normal" else 9)
    cobro = PAY_CARD if tipo_pago == "tarjeta" else PAY_CASH
    return escaneo + cobro

def simular_caja_normal(num_personas):
    total = 0
    datos = []

    for i in range(num_personas):
        productos = random.randint(1, 50)
        pago = random.choice(["tarjeta", "efectivo"])
        tipo_cajero = random.choice(["normal", "inexperto"])
        tiempo = calcular_tiempo(productos, pago, tipo_cajero)
        total += tiempo
        datos.append({
            "persona": i+1,
            "productos": productos,
            "pago": pago,
            "cajero": tipo_cajero,
            "tiempo": tiempo
        })
    return total, datos
