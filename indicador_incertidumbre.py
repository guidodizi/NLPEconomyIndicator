def indicador_mensual_por_categoria(diario, fecha):
    """
    Función que calcula el índice para un diario y fecha dados. 
    
    Params: 
        diario: indica qué diario a procesar. 
        fecha: indica el mes y año en formato mm-aaaa. 

    Returns: 
        Devuelve una tupla (A,B)
        A: total de noticias del mes. 
        B: cantidad noticias EPU del mes. 
        C: diccionario con la cantidad de noticias EPU por categoría. 
    """
    total_noticias_mes = 100
    # total_noticias_mes = cantidad_articulos(diario)
    noticias_epu_mes = 0
    
    cantidad_por_categoria = {
        '3': 0,  # política impositiva
        '4': 0,  # política de gasto gubernamental
        '5': 0,  # política fiscal
        '6': 0,  # política monetaria
        '7': 0,  # política de salud
        '8': 0,  # política de seguridad nacional
        '9': 0,  # política de regulación financiera
        '10': 0,  # política de regulación
        '11': 0,  # política de deuda soberana y crisis monetaria
        '12': 0,  # política de programas de derechos
        '13': 0,  # política comercial
        '14': 0,  # otras políticas
        '15': 0  # autoridades
    }

    # PROCESAR NOTICIAS Y DEVOLVER RESULTADOS
    if (diario == "el pais"):
        noticias_epu_mes = procesar_noticias_el_pais(fecha, cantidad_por_categoria)
    elif (diario == "el observador"):
        noticias_epu_mes = procesar_noticias_el_observador(fecha, cantidad_por_categoria)
    elif (diario == "la diaria"):
        noticias_epu_mes = procesar_noticias_la_diaria(fecha, cantidad_por_categoria)
    elif (diario == "la republica"):
        noticias_epu_mes = procesar_noticias_la_republica(fecha, cantidad_por_categoria)

    return total_noticias_mes, noticias_epu_mes, cantidad_por_categoria