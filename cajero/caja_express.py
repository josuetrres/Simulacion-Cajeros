import random
from caja_normal import calcular_tiempo

def simular_caja_express(num_personas):
    """Simula la caja express (máximo 10 productos)."""
    total = 0
    datos = []

    for i in range(num_personas):
        productos = random.randint(1, 10)
        pago = random.choice(["tarjeta", "efectivo"])
        tipo_cajero = random.choice(["normal", "inexperto"])
        tiempo = calcular_tiempo(productos, pago, tipo_cajero)
        total += tiempo
        datos.append({
            "caja": "Express",
            "persona": i+1,
            "productos": productos,
            "pago": pago,
            "cajero": tipo_cajero,
            "tiempo": tiempo
        })
    return total, datos
