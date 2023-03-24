#!/usr/bin/env python3

# program - polskie wordle
# Karolina Rybszleger


import wx
from random import choice


class Wordle(wx.Frame):

    ALFABET = [
        "A", "Ą", "B", "C", "Ć", "D", "E", "Ę", "F",
        "G", "H", "I", "J", "K", "L", "Ł", "M", "N",
        "Ń", "O", "Ó", "P", "Q", "R", "S", "Ś", "T",
        "U", "V", "W", "X", "Y", "Z", "Ź", "Ż"
    ]


    def __init__(self):
        super().__init__(None, title="Wordle", size=(800, 800))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        naglowek = wx.StaticText(self, label="Zagraj w wordle - spróbuj zgadnąć 5-literowe słowo!")
        self.sizer.Add(naglowek, flag=wx.CENTER|wx.TOP|wx.BOTTOM, border=10)
        self.Menu()
        self.alf_tablica() 
        self.ilosc_wyn = 0
        self.ilosc_box = 0
        self.wygrana= False
        self.juz_prop = []
        self.slowo = choice(self.Dane('5l_slowa.txt')).upper()
        #self.slowo = 'KICIA'
        self.ZbudujUI_Przyciski(self.sizer)
        self.SetSizer(self.sizer)
        self.Show()


    def Dane(self, plik):
        with open(plik) as x:
            dane = x.readlines() 

        lista = []
        for i in dane:
            dane = lista.append(i[:-1])
        return lista


    
    def alf_tablica(self):
        tablica = wx.FlexGridSizer(9, 5, 5)
        for x in self.ALFABET:
            a = wx.Button(self, label = x)
            tablica.Add(a, proportion = 1, flag = wx.EXPAND)
            a.Bind(wx.EVT_BUTTON, self.litera_wyswietl)
        self.sizer.Add(tablica, flag = wx.CENTER)

    def litera_wyswietl(self, event):
        if not self.wygrana:     # zeby nie mozna bylo wpisywac nic za pomoca przyciskow po wygranej
            litera = event.GetEventObject().GetLabel()
            self.entry.SetValue(str(self.entry.GetValue() + str(litera)))



    def Menu(self):

        def dodaj_menu(menubar, name):
            m = wx.Menu()
            menubar.Append(m, name)
            return m

        def menu_entry(frame, menu, name, shortcut = '', action = None, kind = wx.ITEM_NORMAL):
            ii = wx.NewIdRef()
            if shortcut:
                name += '\t' + shortcut
            mi = wx.MenuItem(menu, ii, name, kind = kind)
            if action:
                frame.Bind(wx.EVT_MENU, action, id=ii)
            menu.Append(mi)
            return mi

        mb = wx.MenuBar()
        self.SetMenuBar(mb)

        m = dodaj_menu(mb, '&Opcje')
        menu_entry(self, m, '&O programie',  '', self.o_programie)
        menu_entry(self, m, '&Reguły gry',  '', self.reguly)
        menu_entry(self, m, '&Koniec gry',  '', self.koniec)


    # funckje do menu

    def o_programie(self, env):
        wx.MessageBox('Program stworzony na potrzeby ćwiczeń z paradygmatów programowania.\nWersja: styczeń 2023 rok\nKarolina Rybszleger', self.GetTitle())

    def reguly(self, env):
        wx.MessageBox('Reguły gry\n\nGra polega na odgadywaniu 5-literowych słów. Użytkownik ma na to 6 prób, ale każda z nich niesie za sobą szanse otrzymania podpowiedzi.\n\nGdy dana litera zmieni kolor na zielony oznacza to, że znajduje się ona we właściwym miejscu. Kolor żółty - dana litera znajduje się w wyrazie, ale w niewłaściwym miejscu. Kolor czarny - litera w ogóle nie występuje w danym słowie. \n\nCelem gry jest odgadnięcie słowa w maksymalnie 6 podejściach (jednak im szybciej - tym lepiej).', self.GetTitle())

    def koniec(self, env):
        self.Close()
        print('Koniec gry')



    # przyciski i pole tekstowe

    def ZbudujUI_Przyciski(self, sizer):

        box = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(box, 0, wx.CENTER | wx.ALL, 10)

        # do wpisywania propozycji
        self.entry = wx.TextCtrl(self)
        box.Add(self.entry, 1, wx.ALIGN_CENTER, 10)
        self.entry.SetValue('')


        box2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(box2, 0, wx.CENTER | wx.ALL, 10)

        # 4 przyciski potrzebne dla gry 
        self.button0 = wx.Button(self, label = 'poddaj się')
        box2.Add(self.button0, 0, wx.ALIGN_CENTER, 10)
        self.button0.Bind(wx.EVT_BUTTON, self.poddanie)

        self.button1 = wx.Button(self, label = 'cofnij')
        box2.Add(self.button1, 0, wx.ALIGN_CENTER, 10)
        self.button1.Bind(wx.EVT_BUTTON, self.cofnij)

        self.button2 = wx.Button(self, label = 'wyczyść')
        box2.Add(self.button2, 0, wx.ALIGN_CENTER, 10)
        self.button2.Bind(wx.EVT_BUTTON, self.wyczysc)

        self.button3 = wx.Button(self, label = 'spróbuj')
        box2.Add(self.button3, 0, wx.ALIGN_CENTER, 10)
        self.button3.Bind(wx.EVT_BUTTON, self.sprobuj)


        # propozycje 
        box3 = wx.BoxSizer(wx.VERTICAL)
        self.wyn = [wx.TextCtrl(self) for i in range(6)]
        for wyn in self.wyn:
            box3.Add(wyn.Hide(), 1, wx.ALIGN_CENTER, 10)    # Hide() zeby ukryc (nie chce wyswietlac tych 6 TextCtrl) a nie mogę usunąc sizer.Add(box3 ...) - twedy tworza sie niechciane efekty uboczne
        sizer.Add(box3, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # miejsce gdzie beda dodawane komentarze (np niespelnianie jakiegos warunku, wygrana, przegrana, przekroczenie ilosci dostepnych prob)
        box4 = wx.BoxSizer(wx.HORIZONTAL)
        self.kom = wx.StaticText(self, label = str(self.entry.GetValue()))
        box4.Add(self.kom, 1, wx.ALIGN_CENTER, 10)
        sizer.Add(box4, 0, wx.ALIGN_CENTER | wx.ALL, 10)


        # miejsce gdzie bedzie wyswietlal sie wynik ( cos/6)
        box_wynik = wx.BoxSizer(wx.HORIZONTAL)
        self.wynik = wx.StaticText(self, label = "")
        box_wynik.Add(self.wynik, 1, wx.ALIGN_CENTER, 10)
        sizer.Add(box_wynik, 0, wx.CENTER | wx.ALL, 10)


    # tworzenie pudełek w zaleznosci od ilosci prob, niepotrzebne nie beda tworzone
    def pudelko_nr_proby(self, env):
        
        if self.ilosc_box == 0:
            self.box6 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(self.box6, 0, wx.CENTER | wx.ALL, 10)
        elif self.ilosc_box == 1:
            self.box7 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(self.box7, 0, wx.CENTER | wx.ALL, 10)
        elif self.ilosc_box == 2:
            self.box8 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(self.box8, 0, wx.CENTER | wx.ALL, 10)
        elif self.ilosc_box == 3:
            self.box9 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(self.box9, 0, wx.CENTER | wx.ALL, 10)
        elif self.ilosc_box == 4:
            self.box10 = wx.BoxSizer(wx.HORIZONTAL)
            self.sizer.Add(self.box10, 0, wx.CENTER | wx.ALL, 10)
        else:
            self.box11 = wx.BoxSizer(wx.HORIZONTAL)  
            self.sizer.Add(self.box11, 0, wx.CENTER | wx.ALL, 10)


    # poddanie się - wyświetlenie odpowiedzi
    def poddanie(self, env):
        self.kom.SetLabel(self.slowo)
        self.wygrana = True         # żeby zablokować mozliwość dalszego wpisywania za pomoca przyciskow (chociaz nie jest to 'wygrana')
        self.entry.Disable()        # żeby zablokować mozliwość dalszego wpisywania za pomoca klawiatury
        self.wynik.SetLabel("X/6")
        self.Layout()

    # usuwa ostatnią wprowadzoną literę
    def cofnij(self, env):
        self.entry.SetValue(str(self.entry.GetValue()[:-1]))

    # usuwa cały tekst wpisany przez użytkownika
    def wyczysc(self, env):
        self.entry.SetValue('')


    # gra - proba zostaje poddana sprawdzeniu
    def sprobuj(self, env):

        proba = str(self.entry.GetValue())
        self.kom.SetLabel('')

        # sprawdzanie czy slowo jest 5- literowe
        if len(proba) != 5:
            self.kom.SetLabel('to nie jest 5-literowe słowo!')
            self.Layout()
        
        # tylko polskie slowa
        elif proba.lower() not in self.Dane('5l_slowa.txt'):
            self.kom.SetLabel('to nie jest polskie słowo!')
            self.Layout()
            
        
        else:

            # jak uda sie zgadnac
            if proba == self.slowo:
                print("wygrana")
                self.kom.SetLabel('Wygrałeś! Gratulacje!')
                self.wyn[self.ilosc_wyn].SetForegroundColour('green')
                self.wyn[self.ilosc_wyn].SetLabel(str(self.entry.GetValue()))
                self.wygrana = True  
                self.entry.Disable()        # zeby nie mozna bylo wpisywac nic recznie po wygranej
                self.wynik.SetLabel("{}/6".format(self.ilosc_box +1))      # +1 poniewaz self.ilosc_box jest od zera a to jest wtedy nasza pierwsza propozycja 


            # sprawdzanie czy wczesniej uzytkownik nie wpisal tego samego slowa
            if proba in self.juz_prop:
                self.kom.SetLabel('to słowo już sprawdzałeś!')
                self.Layout()


            # nietrafione ale spelniajace warunki
            else:
                self.pudelko_nr_proby(self)

                a=[]
                b=[]
                length = len(proba)
                for p in range(length):
                    i = self.slowo[p]
                    litera = proba[p]
                    a.append(i)
                    b.append(litera)

                    box5 = wx.BoxSizer(wx.VERTICAL)
                    self.lit = wx.StaticText(self, label = litera)
                    #print(litera)
                    box5.Add(self.lit, 1, wx.ALIGN_CENTER, 10)
                    
                    if self.ilosc_box == 0:
                        self.box6.Add(box5, 0, wx.CENTER | wx.ALL, 10)
                    elif self.ilosc_box == 1:
                        self.box7.Add(box5, 0, wx.CENTER | wx.ALL, 10)
                    elif self.ilosc_box == 2:
                        self.box8.Add(box5, 0, wx.CENTER | wx.ALL, 10)
                    elif self.ilosc_box == 3:
                        self.box9.Add(box5, 0, wx.CENTER | wx.ALL, 10)
                    elif self.ilosc_box == 4:
                        self.box10.Add(box5, 0, wx.CENTER | wx.ALL, 10)
                    else:
                        self.box11.Add(box5, 0, wx.CENTER | wx.ALL, 10)


                    # oznaczanie kolorami poprawnosci kazdej litery
                    if litera in self.slowo and litera in i:
                        self.lit.SetForegroundColour('green')

                    elif litera in self.slowo:
                        if b.count(litera) <= self.slowo.count(litera):
                            self.lit.SetForegroundColour('yellow')

                        else:
                            self.lit.SetForegroundColour('black')

                    else:
                        self.lit.SetForegroundColour('black')
                    

                    self.Layout()


                self.wyn[self.ilosc_wyn].SetLabel(str(self.entry.GetValue()))
                
                
                self.ilosc_wyn +=1
                self.ilosc_box +=1

        
            self.juz_prop.append(proba)


            # warunkowanie ilosci prob, proby uzytkownika- max 6
            if self.ilosc_wyn > 5:
                self.kom.SetLabel('koniec prób')
                self.wygrana = True         # żeby zablokować mozliwość dalszego wpisywania za pomoca przyciskow (chociaz nie jest to 'wygrana')
                self.entry.Disable()        # żeby zablokować mozliwość dalszego wpisywania za pomoca klawiatury
                self.wynik.SetLabel("X/6")
                self.Layout()
                
                
        self.entry.SetValue('')
        


if __name__ == "__main__":
    print('START')
    app = wx.App()
    okno = Wordle()
    app.SetTopWindow(okno)
    app.MainLoop()
    print('KONIEC')
