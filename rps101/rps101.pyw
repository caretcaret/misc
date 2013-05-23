#!/usr/bin/python
#rps101.pyw
#Rock-Paper-Scissors 101

#modules
import wx

#define the app
app = wx.App()

#ids
ID_NEW_GAME = 1
ID_RULES_MENU = 2
ID_STATS = 3
ID_QUIT = 4
ID_HELP = 5
ID_ABOUT = 6
ID_NEW_GAME_BUTTON = 7
ID_RULES = [i for i in range(20,31)]

#constants
NAME = 'RPS-101'
VERSION = 0.1
VERSION_STRING = 'version 0.1'
DESCRIPTION = """Rock Paper Scissors 101 is the original Rock
Paper Scissors game, with a twist- there are
101 gestures that you can use! That means that
there are 5,050 non-tie outcomes and there is
only a 0.99% chance that you will get a tie!
"""
COPYRIGHT = 'Original concept ' + chr(169) + ' 2006 David C. Lovelace\n\
Images ' + chr(169) + ' 2006 David C. Lovelace\n\
Data ' + chr(169) + ' 2006 David C. Lovelace\n\
Program ' + chr(169) + ' 2008 Jeffrey Zhang'
WEBSITE = 'http://www.umop.com/rps101.htm'

#graphics/data
LOGO = wx.Bitmap('images/rps101_banner.jpg')
IMGS = [0 for i in range(101)]
GESTURES = ['DYNAMITE', 'TORNADO', 'QUICKSAND', 'PIT', 'CHAIN', 'GUN', 'LAW',\
            'WHIP', 'SWORD', 'ROCK', 'DEATH', 'WALL', 'SUN', 'CAMERA', 'FIRE',\
            'CHAINSAW', 'SCHOOL', 'SCISSORS', 'POISON', 'CAGE', 'AXE',\
            'PEACE', 'COMPUTER', 'CASTLE', 'SNAKE', 'BLOOD', 'PORCUPINE',\
            'VULTURE', 'MONKEY', 'KING', 'QUEEN', 'PRINCE', 'PRINCESS',\
            'POLICE', 'WOMAN', 'BABY', 'MAN', 'HOME', 'TRAIN', 'CAR', 'NOISE',\
            'BICYCLE', 'TREE', 'TURNIP', 'DUCK', 'WOLF', 'CAT', 'BIRD',\
            'FISH', 'SPIDER', 'COCKROACH', 'BRAIN', 'COMMUNITY', 'CROSS',\
            'MONEY', 'VAMPIRE', 'SPONGE', 'CHURCH', 'BUTTER', 'BOOK', 'PAPER',\
            'CLOUD', 'AIRPLANE', 'MOON', 'GRASS', 'FILM', 'TOILET', 'AIR',\
            'PLANET', 'GUITAR', 'BOWL', 'CUP', 'BEER', 'RAIN', 'WATER', 'TV',\
            'RAINBOW', 'UFO', 'ALIEN', 'PRAYER', 'MOUNTAIN', 'SATAN',\
            'DRAGON', 'DIAMOND', 'PLATINUM', 'GOLD', 'DEVIL', 'FENCE',\
            'VIDEO GAME', 'MATH', 'ROBOT', 'HEART', 'ELECTRICITY',\
            'LIGHTNING', 'MEDUSA', 'POWER', 'LASER', 'NUKE', 'SKY', 'TANK',\
            'HELICOPTER']

#variables (rules)
in_play = [True for i in range(101)]

#functions
def GetImage(number):
    if number in [19, 36, 40, 49, 55, 76, 85, 86, 89, 91]:
        if IMGS[number-1] == 0:
            IMGS[number-1] = wx.Animation('/images/' + str(number) + '.gif', \
                                        wx.ANIMATION_TYPE_GIF)
        return IMGS[number-1]
    elif number < 102:
        if IMGS[number-1] == 0:
            IMGS[number-1] = wx.Bitmap('/images/' + str(number) + '.png')
        return IMGS[number-1]
    else:
        return wx.NullBitmap

#application
class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(768, 576))

        #menubar
        menubar = wx.MenuBar()
        
        file_menu = wx.Menu()
        
        new_game = wx.MenuItem(file_menu, ID_NEW_GAME, '&New Game')
        #new_game.SetBitmap(wx.Bitmap('filename'))
        file_menu.AppendItem(new_game)
        
        file_menu.AppendSeparator()

        rules = wx.MenuItem(file_menu, ID_RULES_MENU, '&Rules')
        #set_rules.SetBitmap(wx.Bitmap('filename'))
        file_menu.AppendItem(rules)

        statistics = wx.MenuItem(file_menu, ID_STATS, '&Statistics')
        #records.SetBitmap(wx.Bitmap('filename'))
        file_menu.AppendItem(statistics)

        file_menu.AppendSeparator()

        quit_ = wx.MenuItem(file_menu, ID_QUIT, '&Quit')
        #quit.SetBitmap(wx.Bitmap('filename'))
        file_menu.AppendItem(quit_)

        help_menu = wx.Menu()
        
        help_ = wx.MenuItem(help_menu, ID_HELP, '&Help')
        #quit.SetBitmap(wx.Bitmap('filename'))
        help_menu.AppendItem(help_)

        help_menu.AppendSeparator()

        about = wx.MenuItem(help_menu, ID_ABOUT, '&About')
        #about.SetBitmap(wx.Bitmap('filename'))
        help_menu.AppendItem(about)

        menubar.Append(file_menu, '&File')
        menubar.Append(help_menu, '&Help')
        self.SetMenuBar(menubar)

        #bind events
        self.Bind(wx.EVT_MENU, self.NewGame, id=ID_NEW_GAME)
        self.Bind(wx.EVT_MENU, self.Rules, id=ID_RULES_MENU)
        self.Bind(wx.EVT_MENU, self.Stats, id=ID_STATS)
        self.Bind(wx.EVT_MENU, self.Quit, id=ID_QUIT)
        self.Bind(wx.EVT_MENU, self.Help, id=ID_HELP)
        self.Bind(wx.EVT_MENU, self.About, id=ID_ABOUT)

        #window body
        mainpanel = wx.Panel(self, -1)
        mainpanel.SetBackgroundColour('#FFF')
        vbox = wx.BoxSizer(wx.VERTICAL)

        logo = wx.StaticBitmap(mainpanel, -1, LOGO)
        button = wx.Button(mainpanel, ID_NEW_GAME_BUTTON, \
                           'New Game', style=wx.BU_EXACTFIT)
        
        vbox.Add(logo, flag=wx.ALIGN_CENTER)
        vbox.Add(button, flag=wx.ALIGN_CENTER)

        mainpanel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.NewGame, id=ID_NEW_GAME_BUTTON)

        #other events to be bound

        #show the window        
        self.Centre()
        self.Show(True)
        
    def NewGame(self, event):
        pass
    
    def Rules(self, event):
        RulesWindow(main_window, -1, 'RPS-101 Rules Configuration')
    
    def Stats(self, event):
        pass
    
    def Quit(self, event):
        self.Close()
    
    def Help(self, event):
        pass
    
    def About(self, event):
        about_dialog = wx.AboutDialogInfo()
        about_dialog.SetIcon(wx.Icon('images/rps101.png', wx.BITMAP_TYPE_PNG))
        about_dialog.SetName(NAME)
        about_dialog.SetVersion(VERSION_STRING)
        about_dialog.SetDescription(DESCRIPTION)
        about_dialog.SetCopyright(COPYRIGHT)
        about_dialog.SetWebSite(WEBSITE)
        wx.AboutBox(about_dialog)

class RulesWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(768, 576))
        
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour('#FFF')

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, -1, 'Game to play', style=wx.ALIGN_CENTRE))

        hbox1 = wx.BoxSizer()
        hbox1.Add(wx.ToggleButton(panel,ID_RULES[0],'RPS',style=wx.BU_EXACTFIT))
        hbox1.Add(wx.ToggleButton(panel,ID_RULES[1],'RPS-7',style=wx.BU_EXACTFIT))
        hbox1.Add(wx.ToggleButton(panel,ID_RULES[2],'RPS-9',style=wx.BU_EXACTFIT))
        hbox1.Add(wx.ToggleButton(panel,ID_RULES[3],'RPS-11',style=wx.BU_EXACTFIT))
        hbox1.Add(wx.ToggleButton(panel,ID_RULES[4],'RPS-15',style=wx.BU_EXACTFIT))
        hbox1.Add(wx.ToggleButton(panel,ID_RULES[5],'RPS-25',style=wx.BU_EXACTFIT))
        hbox1.Add(wx.ToggleButton(panel,ID_RULES[6],'RPS-101',style=wx.BU_EXACTFIT))

        vbox.Add(hbox1, 1, flag=wx.ALIGN_CENTER)
        panel.SetSizer(vbox)
        
        self.Show()

main_window = MainWindow(None, -1, NAME)
app.MainLoop()
