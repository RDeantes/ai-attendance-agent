import subprocess

# 🐻 Personalidad Baloo
def personalidad_baloo(respuesta):
    return f"🐻 Baloo dice:\n{respuesta}\n\nRecuerda: busca lo más vital 😎🎶"


# 🎯 FUNCIÓN PRINCIPAL
def procesar(texto):
    texto_lower = texto.lower()

    if "acta" in texto_lower:
        return personalidad_baloo(generar_acta(texto))

    elif "hola" in texto_lower:
        return personalidad_baloo("Hola pequeño amigo 😎 ¿Qué necesitas hoy?")

    else:
        return personalidad_baloo(
            "No entendí 🤔 intenta así:\nacta Juan Pérez 10/04/2026 mesero"
        )


# 📄 FUNCIÓN QUE GENERA ACTA
def generar_acta(texto):
    try:
        partes = texto.split()

        # 🔍 Buscar la fecha
        fecha = None
        for p in partes:
            if "/" in p:
                fecha = p
                break

        if not fecha:
            return "No encontré la fecha ❌ usa formato dd/mm/yyyy"

        fecha_index = partes.index(fecha)

        # 👤 Nombre completo
        nombre = " ".join(partes[1:fecha_index])

        # 💼 Puesto
        puesto = " ".join(partes[fecha_index + 1:])

        if not nombre or not puesto:
            return "Formato incorrecto ❌ usa:\nacta Juan Pérez 10/04/2026 mesero"

        # 🔥 LIMPIEZA DE DATOS (AQUÍ ESTÁ EL FIX)
        nombre_limpio = nombre.replace(" ", "_")
        fecha_limpia = fecha.replace("/", "-")

        template = "Acta_Administrativa_Falta_Injustificada_Membretada(1).docx"
        output = f"Acta_{nombre_limpio}_{fecha_limpia}.docx"

        resultado = subprocess.run(
            [
                "python",
                "llena actas.py",
                "--template", template,
                "--output", output,
                "--empleado", nombre,
                "--puesto", puesto,
                "--fecha", fecha
            ],
            capture_output=True,
            text=True
        )

        # Debug (puedes borrar luego)
        print("STDOUT:", resultado.stdout)
        print("STDERR:", resultado.stderr)

        if resultado.returncode == 0:
            return f"🎉 ¡Listo, pequeño amigo!\nTu acta ya quedó lista 🐻📄\nArchivo: {output}"

        elif resultado.stderr:
            return f"❌ Error al generar acta:\n{resultado.stderr}"

        else:
            return "❌ No se generó el acta correctamente"

    except Exception as e:
        return f"Error al generar acta: {str(e)}"
    
    