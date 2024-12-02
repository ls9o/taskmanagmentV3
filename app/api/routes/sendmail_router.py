# app/api/routes/sendmail_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

router = APIRouter()

# กำหนดค่า SMTP Server
SMTP_SERVER = 'smeinf054.smebank.local'
EMAIL_ADDRESS = 'coreportal@smebank.co.th'
EMAIL_PASSWORD = '12QWaszx'
EMAIL_NAME = 'coreportal@smebank.co.th'

class Email(BaseModel):
    from_email: EmailStr
    to: list[EmailStr]
    cc: list[EmailStr] = []  
    bcc: list[EmailStr] = []  
    subject: str
    body: str
    attach_name: str = None 
    attach_location: str = None
    is_urgent: bool = False

@router.post("/send-email/")
async def send_email(email: Email):
    msg = MIMEMultipart()
    msg['From'] = email.from_email
    msg['To'] = ', '.join(email.to)
    
    # ตรวจสอบว่า cc มีการระบุหรือไม่
    if email.cc:
        msg['Cc'] = ', '.join(email.cc)
    
    msg['Subject'] = email.subject

    # เพิ่มเนื้อหาของอีเมล
    msg.attach(MIMEText(email.body, 'html'))

    # แนบไฟล์ถ้ามี
    if email.attach_name and email.attach_location:
        try:
            with open(email.attach_location, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={email.attach_name}')
                msg.attach(part)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Attachment not found")

    try:
        with smtplib.SMTP(SMTP_SERVER, 587) as server:  # ใช้พอร์ต 587 สำหรับ TLS
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
