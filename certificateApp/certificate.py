from PIL import Image,ImageDraw,ImageFont
from datetime import datetime
from .models import CertificateConfig


def generate_certificate(filespath,name,interntype,profile,startdate,enddate,logoname,registration,*args, **kwargs):
    """
    Function to generate a certificate take parameters path to file,name of intern, type of work, profile,
    start date, end date, logoname to be used, registration number, path where file to be saved.
    """
    # print(filespath,name,type,profile,startdate,enddate,logoname,registration,savepath)
    c = CertificateConfig.objects.all().last()
    imagepath = c.certificate_img.path
    logopath = c.logo_img.path
    signpath = c.sign_img.path

    # # Size of certificate to be generated
    cktsize = (round(float(c.cktw)),round(float(c.cktl)))
    logosize=(round(float(c.logow)),round(float(c.logol)))
    signsize=(round(float(c.signw)),round(float(c.signl)))

    # # font size
    namesize = round(float(c.namesize)) #px
    typesize = round(float(c.typesize))
    profilesize = round(float(c.profilesize))
    dsize = round(float(c.dsize))
    datesize = round(float(c.datesize))

    # # content coordinates
    namecdt = (round(float(c.namex)),round(float(c.namey)))
    typecdt = (round(float(c.typex)),round(float(c.typey)))
    profilecdt = (round(float(c.profilex)),round(float(c.profiley)))
    d1cdt = (round(float(c.d1x)),round(float(c.d1y)))
    d2cdt = (round(float(c.d2x)),round(float(c.d2y)))
    datecdt = (round(float(c.datex)),round(float(c.datey)))
    renocdt = (round(float(c.renox)),round(float(c.renoy)))
    logocdt = (round(float(c.logox)),round(float(c.logoy)))
    signcdt = (round(float(c.signx)),round(float(c.signy)))

    # # font faimily to be used 
    defaultfamily = f"{filespath}/fonts/Viga-Regular.ttf"
    namefamily = defaultfamily if c.namefont.name == 'default.ttf' else c.namefont.path
    otherfamily = defaultfamily if c.otherfont.name == 'default.ttf' else c.otherfont.path
    # defaultfamily = "arial.ttf"

    text_color = (0,0,0)

    name = str(name)
    interntype = str(interntype)
    profile = str(profile)
    d1 = startdate.strftime('%m-%d-%Y')
    d2 = enddate.strftime('%m-%d-%Y')
    date = datetime.now().strftime('%m-%d-%Y')
    registration_no = str(registration)
    # # cerficate_no = 'certificate No. - c57f9298-d2c2-4b1a-a456-fd1b90668072'
    # # url = 'url - https://exmaple.com/certificate/c57f9298-d2c2-4b1a-a456-fd1b90668072'

    # print(imagepath,logopath,signpath,name,interntype,d1,d2,date,namefamily,savepath)
    # # opening images and making them proper
    cktim = Image.open(imagepath,'r').resize(cktsize).convert("RGBA")
    logoim = Image.open(logopath,'r').resize(logosize).convert("RGBA")
    signim = Image.open(signpath,'r').resize(signsize).convert("RGBA")

    # make the image drawable
    d = ImageDraw.Draw(cktim)

    namefont = ImageFont.truetype(namefamily,namesize)
    typefont = ImageFont.truetype(otherfamily,typesize)
    profilefont = ImageFont.truetype(otherfamily,profilesize)
    dfont = ImageFont.truetype(otherfamily,dsize)
    datefont = ImageFont.truetype(otherfamily,datesize)
    refont = ImageFont.truetype(otherfamily,datesize)

    d.text(namecdt,name,fill=text_color,font=namefont)
    d.text(typecdt,interntype,fill=text_color,font=typefont)
    d.text(profilecdt,profile,fill=text_color,font=profilefont)
    d.text(d1cdt,d1,fill=text_color,font=dfont)
    d.text(d2cdt,d2,fill=text_color,font=dfont)
    d.text(datecdt,date,fill=text_color,font=datefont)
    d.text(renocdt,registration_no,fill=text_color,font=refont)

    transparent = Image.new('RGBA', cktsize, (0,0,0,0))
    transparent.paste(cktim,(0,0))
    transparent.paste(logoim,logocdt,logoim)
    transparent.paste(signim,signcdt,signim)

    # # print(cktim.size)
    # # print(logoim.size)
    # # print(signim.size)

    # transparent = Image.new("RGBA", cktsize)
    # transparent = Image.alpha_composite(transparent,cktim)
    # transparent = Image.alpha_composite(transparent, logoim)

    # registration_no = registration_no.split('/')[1]
    # saving as png
    png = f'{filespath}/temp/certificate_{registration_no}.png'
    transparent.save(png)

    # converting to RGB mode to save as pdf
    transparent = transparent.convert("RGB")
    pdf = f'{filespath}/temp/certificate_{registration_no}.pdf'
    transparent.save(pdf)
    return [png,pdf]