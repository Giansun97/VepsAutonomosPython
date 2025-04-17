# src/enviar_email.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from utils import constants

def enviar_vep_por_email(filepath, contribuyente):
    """
    Envía el archivo VEP por correo electrónico al contribuyente.
    
    Args:
        filepath (str): Ruta completa al archivo PDF del VEP.
        contribuyente (Contribuyente): Objeto contribuyente con datos de contacto.
    
    Returns:
        bool: True si el correo se envió exitosamente, False en caso contrario.
    """
    # Obtener configuración del email remitente
    sender_email = getattr(constants, 'EMAIL_SENDER', None)
    sender_password = getattr(constants, 'EMAIL_PASSWORD', None)
    
    if not sender_email or not sender_password:
        print("Error: Configuración de correo no encontrada. Definir EMAIL_SENDER y EMAIL_PASSWORD en constants.py")
        return False
        
    # Comprobar que el archivo existe
    if not os.path.exists(filepath):
        print(f"Error: No se encontró el archivo {filepath}")
        return False
    
    # Comprobar que el contribuyente tiene email
    if not hasattr(contribuyente, 'mail') or not contribuyente.mail:
        print(f"Error: El contribuyente {contribuyente.cuit_contribuyente} no tiene dirección de email")
        return False
    
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = contribuyente.mail
    msg['Subject'] = f"VEP {contribuyente.cliente} - Período {contribuyente.datos_vep.periodo_fiscal}/{contribuyente.datos_vep.anio_fiscal}"
    
    # Cuerpo del mensaje
    body = f"""
    Estimado/a contribuyente,
    
    Adjunto encontrará el Volante Electrónico de Pago (VEP) generado para:
    - CUIT: {contribuyente.cuit_contribuyente}
    - Impuesto: {contribuyente.datos_vep.grupo_de_tipo_pago}
    - Período: {contribuyente.datos_vep.periodo_fiscal}/{contribuyente.datos_vep.anio_fiscal}
        
    Saludos.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    # Adjuntar el archivo PDF
    with open(filepath, 'rb') as file:
        attachment = MIMEApplication(file.read(), _subtype="pdf")
        attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(filepath))
        msg.attach(attachment)
    
    try:
        # Configurar el servidor SMTP para Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Activar el modo seguro
        server.login(sender_email, sender_password)
        
        # Enviar el correo
        text = msg.as_string()
        server.sendmail(sender_email, contribuyente.mail, text)
        server.quit()
        
        print(f"Correo enviado exitosamente a {contribuyente.mail}")
        return True
    
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return False