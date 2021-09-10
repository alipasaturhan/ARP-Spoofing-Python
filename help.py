import interface

def run():
    print ("""    1) İlk olarak yerel ağ taranır.

    2) Tarama sonrasında seçilen hedefin numarası set edilir.

    3) Seçilen hedef için ARP Spoofing saldırısı başlatılır.

    4) Daha sonra network sniff edilir.

    5) ARP Spoofing saldırısını durdurmak için tekrar 3. modül seçilmelidir.
    'Running: False' durumuna getirilebilir. False olduğu takdirde sistem
    ayarları restore edilir ve arp tablosu otomatik bir şekilde önceki
    haline çevirilir.

    6)Programdan çıkmak için programın kendi 'exit' seçeneği kullanılabilir.

    7)Program modüllerini durdurmak için Ctrl + Z tuşları kullanılmalıdır.

    Proje Sahibi: Ali Paşa Turhan			81 İlde 81 Siber Kahraman\n""")
    input("(quit) Press ENTER")
    interface.show()
