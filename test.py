striped = "/Users/Loshkarev/Downloads/2022_MIUZ_Premium11576_1 1x1.jpg"
striped = "smb://192.168.10.105/Shares/Marketing/Photo/2023/MUIZ paper bg.psd"
striped = "smb:\\192.168.10.105\Shares\Marketing\External\Фото_и_видео_Магазинов\Фото_магазинов"
striped = "\\192.168.10.105\Shares\Marketing\External\Фото_и_видео_Магазинов"
# striped = "sbc01\Shares\Marketing\General\4. MONTHLY TO START\МАРТ\ADV& PR\ФОТО"
# striped = "/Users/evlosh/Downloads/AutopanoGiga3.5.dmg"
# striped = "Some text"
# striped = "Z:\Marketing\External\Фото_и_видео_Магазинов\Фото_магазинов_2023\Retouch"
# striped = "smb://sbc01/shares/Marketing/Design/WEB/2023/10_Oсt"
striped = "/Volumes/Shares/Marketing/Photo/2023/01 - Январь"







# striped = "smb://192.168.10.105/Shares/Marketing/Photo/2023/MUIZ paper bg.psd"
striped = "smb://sbc01/shares/Marketing/Design/WEB/2023/10_Oсt"
striped = "Volumes/Shares/Marketing/Photo/folder smb name/sbc01/hello"




import re

# striped = striped.replace("\\", "/")

# mac_reg = r'/?.{,100}/.{,100}/.{,100}'
# if not re.findall(mac_reg, striped):
#     print("not mac")

# win_reg = r"[a-zA-Z]://?marketing/"
# striped = re.sub(win_reg, "Shares/Marketing/", striped, flags=re.IGNORECASE)

smb_reg = r"(smb[^/]{,100}:?/?)(/sbc01)"
striped = re.sub(smb_reg, "", striped, flags=re.IGNORECASE)
print(striped)


# sbc_reg = r"(sbc[^/]{,50}:?/?/)"
# striped = re.sub(sbc_reg, "", striped, flags=re.IGNORECASE)

# ip_reg = r"(\d{,4}\.?){,4}(:?\d{,10})?"
# striped = re.sub(ip_reg, "", striped, flags=re.IGNORECASE)

# striped = "/" + striped.strip("/")

# print(striped)




# striped = "2023/01 - Январь"
# striped = "192.168.10.105"

# ip_reg = r"([0-9]{,4}\.){,3}([0-9]{,4})"
# striped = re.sub(ip_reg, "1",striped)

# print(striped)
