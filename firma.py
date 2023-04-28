from playwright.sync_api import sync_playwright
import time
import json

def json_fabric(user, password, usuario, telefono, firma):
    resultado = {   
                    "user": "{}".format(user),
                    "password": "{}".format(password),
                    "usuario": "{}".format(usuario),
                    "telefono": "{}".format(telefono),
                    "firma": "{}".format(firma),
                    "Usado": False
                }
    return resultado

def filtrar_arrays_falsos(array):
    array_filtrado = list(filter(lambda x: x['Usado'] == False, array))
    return array_filtrado

def run(playwright):

    with open("data.json") as archivo_json:
        datajson = json.load(archivo_json)

    lista_firmas = []

    for js in range(0, len(datajson)):
        user_json = datajson[js]["user"]
        password_json = datajson[js]["password"]
        usuario_json = datajson[js]["usuario"]
        telefono_json = datajson[js]["telefono"]
        firma_json= datajson[js]["firma"]
        resultado_json = json_fabric(user_json, password_json, usuario_json, telefono_json, firma_json)
        lista_firmas.append(resultado_json)

    with open("data.json", 'w') as f:
        json.dump(lista_firmas, f, indent=4, ensure_ascii=False)

    with open("data.json") as archivo_json:
        firma_consulta = json.load(archivo_json)

    consulta_firma = filtrar_arrays_falsos(firma_consulta)

    for i in range(0, len(consulta_firma)):
        try:
            chromium = playwright.chromium
            browser = chromium.launch(headless=False)
            page = browser.new_page()
            page.goto("https://accounts.google.com/v3/signin/identifier?dsh=S688669832%3A1681137851757623&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&emr=1&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AQMjQ7RnvP3VYs6iFeeVXau-oI-Op5NJ-S7_KnNilzLV3S_7RakezqN1uWYV8JU-FGcIXU3yEACgXQ&osid=1&passive=1209600&service=mail&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
            user = consulta_firma[i]["user"]
            password = consulta_firma[i]["password"]
            usuario = consulta_firma[i]["usuario"]
            firma = consulta_firma[i]["firma"]
            #Navegacion de login
            page.fill("#identifierId",user)
            page.click("#identifierNext > div > button")
            page.fill("#password > div > div > div > input",password)
            page.click("#passwordNext > div > button")
            time.sleep(10)  

            #Navegacion de configuracion
            page.click("div.FI > a")
            page.click("button.Tj") 
            page.click(".P5")
            page.fill(".xx.nr", firma)
            page.click('button.J-at1-auR')

            if consulta_firma[i]["telefono"] != "":
                telefono = "-  Anexo " + str(consulta_firma[i]["telefono"])
            else:
                telefono = str(consulta_firma[i]["telefono"])

            usuario = consulta_firma[i]["usuario"]
            # Establecer el contenido de la firma
            
            page.evaluate(f"document.querySelector('div[aria-label=\"Firma\"]').innerHTML = '<p>--</p> <b>Consulte el estado de su contrato</b> <span><a href=\"https://www.notariapaino.com.pe/consulta-de-contratos/consulta-en-linea/busqueda-por-numero-de-kardex/\" target=\"_blank\">aquí</a></span><br>        <img style=\"height: 56px; width: 200px;\" src=\"https://oficinavirtual-notariapaino.ceeur.es/pluginfile.php/137/course/summary/logos%20Notaria%202007%20015.jpg\" alt=\"logoPaino\"><br>   <b>{usuario}</b><br>     Av Angamos Este 1803 5to Piso Lima 15036 - CC Open Plaza<br>        Central IP: (511) 6185151 {telefono}<br>        Correo: <span><a href=\"\">{user}</a></span><br>        Web: <span><a href=\"www.notariapaino.com.pe\">www.notariapaino.com.pe</a></span><br>   Ponemos a su disposición nuestras cuentas para pagos Diversos.<br>    <span><a href=\"https://www.notariapaino.com.pe/wp-content/uploads/2020/05/PAGO-DE-ALCABALA.pdf\">Alcabala</a> / <a href=\"https://www.notariapaino.com.pe/wp-content/uploads/2020/05/DEPOSITO-EN-CUENTA.pdf\">Depósito en Cuenta</a> / <a href=\"https://www.notariapaino.com.pe/wp-content/uploads/2020/05/CUENTAS-RECAUDADORAS.pdf\">Cuentas Recaudadoras</a></span><br>    <b>Horario de atención de Lunes a Viernes</b><br>        Verano: 9:00 am a 6:00 pm<br>        Invierno: 9:00 am a 6:30 pm<br>        <img src=\"https://www.notariapaino.com.pe/logotipos/logo.jpg\" alt=\"smc_sgs\"><br>   Playa de Estacionamiento:<br>     Piso 5 - Estacionamiento Verde (CC Open Plaza):<br>       __________________________________________________________________<br>        AVISO: Si recibe este mensaje por error, por favor destrúyalo y notifique al remitente. El remitente no renuncia a sus derechos de confidencialidad o a sus privilegios, y el uso indebido de este correo y/o su contenido está            prohibido.<br><br>        NOTICE: If you received this message in error, please destroy it and notify sender. Sender does not waive any            confidentiality or privilege rights, and improper use of this e-mail and/or its content is prohibited.<br>        ____________________________________________________________________<br>';")
            page.click("text=--")
            time.sleep(5)
            page.keyboard.press("Delete")
            #page.locator("text=PARA RESPUESTAS/REENVÍOSSin firmaaeaFIRMA >> select").select_option("3962556054448321215")
            id=page.evaluate("document.querySelector('.Ps').lastElementChild.value")
            page.locator("text=PARA CORREOS NUEVOS").select_option(id)
            page.locator("text=PARA RESPUESTAS/REENVÍOS").select_option(id)
            page.click("text=Guardar cambios")
            print("Se realizó la actualización de la firma del usuario: ", user)
            time.sleep(5) 
            consulta_firma[i]["Usado"] = True

        except Exception as e:
            print("error al momento de realizar actualizacion de la firma del usuario: ", user)
            print(str(e))
        browser.close()

    consulta_firma = filtrar_arrays_falsos(consulta_firma)
    with open("data.json", 'w') as f:
            json.dump(consulta_firma, f, indent=4, ensure_ascii=False)

with sync_playwright() as playwright:
    run(playwright)