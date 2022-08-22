#!/usr/bin/env python3

from __future__ import print_function

import argparse
import logging
import re
import sys
import string
import traceback
import unicodedata

# These are:
# - Names of Ubuntu versions
# - Words that occur 100x as often in a message as they do as a user name
reserved = {
    'ubuntu', 'help', 'linux'
"topic", "signoff", "signon", "total", "#ubuntu", "window", "server:",
"screen:", "geometry", "co,", "current", "query", "prompt:", "second", "split",
"logging", "logfile", "notification", "hold", "window", "lastlog", "notify",
'netjoined:',
"artful", "aardvark", "bionic", "beaver", "breezy", "badger", "cosmic",
"cuttlefish", "dapper", "drake", "disco", "dingo", "edgy", "eft", "feisty",
"fawn", "gutsy", "gibbon", "hardy", "heron", "hoary", "hedgehog", "intrepid",
"ibex", "jaunty", "jackalope", "karmic", "koala", "lucid", "lynx", "maverick",
"meerkat", "natty", "narwhal", "oneiric", "ocelot", "precise", "pangolin",
"quantal", "quetzal", "raring", "ringtail", "saucy", "salamander", "trusty",
"tahr", "utopic", "unicorn", "vivid", "vervet", "warty", "warthog", "wily",
"werewolf", "xenial", "xerus", "yakkety", "yak", "zesty", "zapus",
"`", "^^", "^_^", "^", "||", "|", "_", "[", "[[", "]]", "{", "\\", "\\\\", "^5", "a",
"aaah", "aaahhh", "aao", "aargh", "abandoned", "abit", "able", "abot", "about",
"above", "absolute", "accent", "accept", "acceptance", "acces", "access",
"accident", "account", "accused", "acpi", "acronym", "across", "act", "action",
"active", "activex", "acts", "adapter", "adb", "add", "addict", "adding",
"additional", "addon", "adds", "adduser", "adept", "administer",
"administration", "administrators", "adn", "adobe", "adsl", "advanced",
"adventure", "advertise", "advertising", "advise", "af", "afk", "african",
"after", "again", "against", "aggravating", "aggressive", "ago", "agp",
"agree", "ah", "aha", "ahead", "ahh", "ahhh", "ahhhh", "ahs", "ai", "air",
"airflow", "airsnort", "ait", "aix", "album", "alert", "algorithm", "alguien",
"algun", "alias", "aliases", "all", "alla", "allegro", "alli", "alliance",
"allow", "allright", "almost", "alo", "alone", "along", "alors", "already",
"alsa", "alsaconf", "alse", "also", "alt", "alter", "alternate", "alternative",
"always", "am", "amarok", "amazed", "amazing", "amazon", "amd", "amd64",
"among", "ampache", "an", "analog", "analysis", "analyzer", "and", "angles",
"animals", "anime", "anjuta", "anotehr", "another", "ansible", "antenna",
"anthy", "any", "anybody", "anyone", "anything", "anyway", "anywhere", "aol",
"apache", "apache2", "apci", "apis", "apm", "apology", "app", "appears",
"apple", "applet", "application", "applied", "apply", "appreciated",
"appropriate", "apps", "apr", "april", "aprox", "apt", "apt-get", "aptitude",
"archaic", "architecture", "archive", "archiver", "archives", "archlinux",
"are", "area", "arena", "arg", "argh", "arise", "arista", "ark", "arm", "arms",
"array", "arrgh", "artist", "arts", "as", "asap", "ascii", "aside", "ask",
"asking", "asla", "ass", "assertion", "assist", "assistance", "association",
"at", "ath0", "athlonxp", "ati", "atm", "atsc", "attack", "attackers",
"attempt", "attractive", "audacity", "audigy", "audio", "audition", "aug",
"aus", "auth", "author", "authority", "authorized", "auto", "automated",
"automatic", "automatix", "autostart", "aux", "av", "avail", "available",
"avant", "avconv", "aw", "aware", "away", "awe", "awesome", "awry", "awww",
"awwww", "aye", "ayone", "ayuda", "azalia", "b4", "back", "backdoor",
"backintime", "backlight", "backport", "backspace", "backup", "bad", "bahasa",
"bakc", "balloon", "ban", "band", "banned", "banning", "banshee", "bar",
"barrel", "bars", "base", "basement", "bash", "bashing", "bashrc", "basic",
"bastard", "battery", "bay", "bbl", "bcm4318", "bcm43xx", "bcm43xx-fwcutter",
"bcz", "be", "beagle", "beautiful", "beauty", "becase", "because", "bed",
"been", "beep", "beers", "beg", "begin", "begs", "being", "bell", "bells",
"bench", "berly", "bery", "beryl", "best", "bet", "beta", "better", "beyond",
"bg", "bi", "bias", "bible", "bie", "big", "biger", "bigger", "biggy", "bin",
"binary", "bios", "bit", "bitch", "bitches", "bitchx", "bitlbee", "bitrate",
"bitten", "bittorrent", "bizarre", "bizzare", "bla", "black", "blacklist",
"bleeding", "blew", "blinking", "block", "blocks", "blow", "blue", "bluefish",
"blueman", "bluetooth", "bluez", "blu-ray", "bmp", "bnc", "boat", "bochs",
"body", "bonding", "bonsoir", "book", "books", "boost", "boot", "booted",
"bootloader", "bootmgr", "boots", "boottime", "bootup", "border", "bose",
"both", "botnet", "bots", "botsnack", "bound", "bout", "box", "boxes", "boys",
"brackets", "brake", "branch", "branches", "brand", "brasero", "brave",
"brazil", "brb", "break", "breaks", "breezy", "bricks", "bridge", "brightness",
"brightside", "brilliant", "british", "broad", "broadband", "broke", "brother",
"brown", "browser", "browsing", "bsd", "btnx", "btrfs", "btw", "budget",
"buffer", "bug", "bugfixes", "bugger", "buggy", "bugs", "bugzilla", "build",
"bulk", "burn", "burned", "burning", "busca", "busted", "busy", "busybox",
"but", "button", "buttons", "buzz", "by", "bzip", "c", "c2", "ca", "cable",
"cache", "cacher", "caldera", "calendar", "california", "call", "called",
"caller", "came", "camera", "campus", "cams", "can", "canada", "cancel",
"canonical", "cant", "capital", "capitals", "caps", "capslock", "car", "card",
"cards", "care", "carry", "cases", "`cat", "cat5", "catalyst", "ccleaner",
"cd", "cd1", "cd-r", "cds", "ce", "celeron", "cellphone", "center", "centos",
"century", "certain", "certificate", "cfdisk", "challenged", "chance",
"chanell", "change", "changing", "charge", "charged", "charm", "chars",
"charset", "chat", "chatter", "cheat", "check", "checker", "checks", "cheers",
"chess", "chicago", "child", "chime", "china", "chinese", "chips", "chipset",
"chm", "chmod", "choice", "choices", "choppy", "chops", "chose", "chosen",
"chown", "chowned", "christ", "christmas", "chrome", "chromium", "chunk",
"chunks", "ci", "ciao", "cigarettes", "circuits", "claim", "class", "clean",
"cleaner", "clear", "cli", "click", "client", "clients", "clock", "clocking",
"clone", "clonezilla", "close", "closed", "closer", "clue", "clueless",
"clutter", "cmd", "cms", "cnt", "cobol", "coc", "code", "coded", "coders",
"coding", "color", "column", "com", "comand", "combine", "comcast", "come",
"comfort", "comics", "coming", "command", "command-line", "commandline",
"common", "community", "como", "comp", "compile", "compiler", "compiz",
"complete", "compliant", "comply", "component", "composite", "compressed",
"computer", "computers", "concentrate", "concepts", "concerned", "concrete",
"conf", "confident", "config", "conflict", "confuse", "confusion", "conky",
"connect", "connected", "connecting", "connection", "connections", "connector",
"console", "construct", "contact", "contents", "contract", "control",
"controller", "controls", "controversial", "convert", "converted", "converter",
"convinced", "coo", "cookies", "copies", "copy", "core2", "core2duo", "corner",
"correct", "corrupted", "cost", "couch", "coucou", "coul", "counter",
"country", "couple", "cousin", "cousins", "cover", "cpanel", "cpp", "cpu",
"cpufreqd", "crappy", "crash", "crashed", "crazy", "create", "creating",
"creation", "creative", "creator", "crippled", "critical", "cron", "cronjob",
"crontab", "cross", "crossover", "crt", "crud", "cry", "ctcp", "ctrl",
"ctrl-alt-del", "cuda", "culprit", "cup", "cure", "curious", "current",
"curses", "cursor", "curve", "cuss", "custom", "customize", "cuz", "cvs", "cz",
"czech", "czy", "daemons", "daily", "damn", "damnit", "dances", "dancing",
"dang", "danger", "dangerous", "danko", "dapper", "darn", "dashboard", "data",
"dates", "day", "daytime", "db", "dban", "dbus", "dcc", "dd", "de", "dead",
"deal", "deb", "debain", "debian", "debians", "debs", "debug", "dec", "decade",
"decent", "decode", "decoded", "decrypt", "decryption", "dedicated", "deeper",
"def", "defalt", "default", "defect", "defense", "deff", "define", "defined",
"defult", "deg", "degree", "delay", "delet", "delete", "deleted", "deluge",
"demonoid", "demuxer", "denied", "dependencies", "depth", "design", "designer",
"desktop", "destination", "destroy", "detached", "detail", "detected",
"detection", "determin", "deutsch", "deutsche", "dev", "devede", "develop",
"device", "devote", "devs", "df", "dhcp", "diag", "diagnostic", "dial",
"dial-up", "dictionary", "did", "died", "dif", "diff", "different",
"difficult", "dig", "dilemma", "dillo", "dinner", "dir", "dire", "directory",
"directx", "disabled", "disappear", "disappeared", "disc", "disconnect",
"disconnected", "discrete", "diskette", "disks", "display", "diss", "dist",
"distinct", "distorted", "distracted", "distribution", "distro", "distupgrade",
"disturb", "dit", "ditch", "dl", "dlink", "dmesg", "dns", "do", "doable",
"doc", "dock", "docker", "docky", "dod", "doe", "does", "doki", "domain",
"domu", "done", "dongle", "donno", "dont", "dos", "dose", "dots", "double",
"doubleclick", "doubt", "dove", "down", "downgrade", "downloader",
"downloading", "downtime", "doze", "dozen", "dpi", "dram", "draw", "drawn",
"dreamweaver", "dress", "dri", "drinks", "drive", "driver", "drm", "drop",
"dropbox", "dropped", "drops", "drug", "drums", "dsp", "du", "dual",
"dualboot", "dudes", "due", "duh", "dumb", "dummies", "dump", "dun", "dunno",
"duo", "duplex", "duplicated", "duplicity", "duron", "dvb", "dvd", "dvd-rw",
"dvdrw", "dvds", "dvr", "dynamic", "e", "e2fsck", "each", "ear", "early",
"earth", "ease", "east", "easter", "easy", "eat", "ebay", "edit", "edited",
"editor", "ee", "eed", "eeebuntu", "een", "effect", "effective", "effort",
"efi", "eg", "eh", "ehat", "eheh", "eide", "electronic", "elegant", "elements",
"elevate", "elevated", "elitist", "ello", "else", "emacs", "email", "embedded",
"embeded", "emerald", "emergency", "emmm", "empathy", "empty", "emulator",
"emulators", "en", "encode", "encoder", "encoding", "encrypted", "encryption",
"end", "enemy", "engine", "engineering", "english", "enjoy", "enlightened",
"enter", "entra", "entrance", "enuf", "enumerate", "enumeration", "env",
"envy", "enyone", "eol", "epiphany", "equipment", "equipped", "er", "erase",
"erh", "erlang", "erorr", "err", "errno", "erro", "erroneous", "error", "es",
"esd", "est", "este", "estimate", "et", "eta", "etc", "etch", "eth", "eth0",
"eth2", "ethernet", "etho", "european", "even", "evening", "ever", "everybody",
"everyday", "evidence", "evolution", "evolved", "ew", "ex", "exact", "exceed",
"excellent", "except", "excessive", "exe", "exec", "execute", "exfat", "exist",
"existed", "existence", "exit", "expect", "expecting", "experiment", "expert",
"explicit", "explicitly", "explode", "explorer", "export", "express",
"expression", "ext", "ext3", "ext4", "extended", "extra", "eye", "eyecandy",
"eyes", "f1", "f10", "f2", "f3", "f7", "facebook", "faced", "fact", "factoid",
"fail", "fair", "fait", "fake", "fala", "fallow", "falls", "familiar", "fan",
"fancy", "fantasy", "faptastic", "far", "fashion", "faster", "fastest",
"fat32", "fatal", "fatrat", "fault", "faulty", "favor", "favorite",
"favorites", "favourite", "fawn", "fb", "fd0", "fdd", "fdi", "feat", "feb",
"fedora", "fee", "feed", "feel", "feeling", "feisty", "fellas", "fellow",
"fetch", "few", "ff", "ff2", "fglrx", "fi", "fiddle", "field", "fighting",
"file", "files", "fileserver", "filesystem", "fill", "filling", "filter",
"filtered", "final", "finally", "find", "fine", "fing", "fingers", "fins",
"firebug", "firefox", "firefox3", "firestarter", "firewall", "firewalls",
"firewire", "firmware", "first", "firstly", "fishing", "fits", "fix", "fixed",
"flag", "flaky", "flamed", "flash", "flashed", "flashget", "flashplugin",
"flavor", "flavors", "flawed", "flickering", "flock", "flood", "floodbot",
"flooding", "floola", "floor", "floppy", "floss", "fluff", "flux", "fluxbox",
"fly", "fml", "fn", "focus", "folder", "folk", "folks", "follow", "font",
"fonts", "foobar2000", "fools", "foomatic", "football", "footprint", "fopen",
"for", "force", "forensic", "forget", "forgotten", "fork", "form", "format",
"formatted", "forme", "former", "formula", "forth", "fortress", "fortune",
"forum", "forward", "foss", "found", "founder", "fr", "francais", "free",
"freebsd", "freely", "freenode", "freevo", "freeware", "freezes", "freezing",
"french", "fresh", "freshly", "friend", "friendly", "friends", "friggin",
"frist", "fro", "from", "froze", "fs", "fsck", "fsf", "fspot", "ftp", "ftw",
"fucker", "fuhrer", "full", "fullscreen", "fully", "function", "funny", "fuss",
"future", "fvwm", "g3", "g5", "gaah", "gadmin", "gah", "gals", "game", "games",
"gaming", "garbage", "gates", "gateway", "gather", "gave", "gay", "gb", "gcc",
"gconf", "gconftool", "gd", "gdisk", "gear", "geeks", "geese", "gem",
"general", "generate", "gentoo", "get", "getty", "gf", "gftp", "gfx", "ghz",
"gib", "gibbon", "gift", "gig", "gigabit", "gimp", "girlfriend", "gist", "git",
"give", "gksudo", "glad", "glibc", "gmp", "gmt", "gnash", "gnewsense", "gnite",
"gnome", "gnomes", "gnome-shell", "gnome-terminal", "gnone", "gns3", "gnu",
"gnutella", "go", "goddamnit", "gods", "goes", "goin", "going", "golly",
"gone", "gonna", "good", "goodbye", "goodness", "goodnight", "google",
"googled", "google-fu", "googles", "googling", "goole", "goood", "goot", "got",
"goto", "gotten", "government", "gpart", "gparted", "gpg", "gpt", "gpu", "gq",
"grabbed", "gracias", "grade", "grain", "grammer", "grand", "grants", "graph",
"graphic", "graphical", "graphics", "graphix", "grasp", "grats", "gratz",
"grazie", "great", "grep", "greyed", "grid", "grief", "ground", "groundhog",
"growisofs", "grr", "grub", "grub2", "grubs", "gsm", "gstreamer", "gta", "gtg",
"gtk", "gues", "guess", "guessing", "gui", "guid", "guide", "guilty", "guis",
"gusty", "guts", "gutsy", "guy", "guys", "guyz", "gvim", "gw", "gxmame", "gym",
"gz", "ha", "haa", "hacked", "hackers", "hacking", "hacks", "had", "hadoop",
"haha", "hahaha", "hahahah", "hahahaha", "hahahahah", "half", "halflife",
"halfway", "halloween", "haloo", "hand", "handle", "hands", "handy", "hang",
"hanks", "happier", "happily", "hard", "harddrive", "harder", "hardly",
"hardware", "hardy", "has", "hate", "hav", "have", "haves", "hd", "hda",
"hda1", "hdb", "hdd", "hdtv", "he", "head", "header", "headless", "headphone",
"heads", "healthy", "hear", "heart", "heartbleed", "heat", "heavy", "heck",
"hee", "hefty", "heh", "hehe", "heheh", "heil", "held", "hell", "hella",
"helllo", "hello", "heloo", "help", "hence", "here", "heres", "heron",
"herring", "het", "heu", "heve", "hex", "hey", "heya", "heyyy", "hi", "hidden",
"hides", "hie", "hier", "high", "high-end", "hii", "hilfe", "him", "himself",
"hint", "his", "history", "hit", "hits", "hl2", "hm", "hmm", "hmmm", "hmmmmm",
"ho", "hoary", "hoe", "hokay", "holder", "homepage", "homeserver", "homework",
"honest", "honesty", "hoops", "hooray", "hope", "horny", "horrid", "hosed",
"host", "hosting", "hostname", "hotspot", "hours", "how", "howso", "howto",
"howtos", "hr", "hrhr", "hrm", "hrs", "hsf", "hsync", "htop", "http", "huawei",
"hug", "huge", "huh", "hum", "hung", "hw", "hwe", "hwy", "hy", "hypervisor",
"_i_", "i", "i3", "i386", "i7", "ia64", "ibook", "ican", "iceweasel", "ici",
"icon", "icons", "icq", "ics", "id", "id3", "ide", "idea", "ideas", "ident",
"idiocy", "idk", "idle", "idling", "idont", "ie", "ieee", "if", "iface",
"ifconfig", "iffy", "ifup", "ignorance", "ignorant", "ignore", "igp", "ihr",
"iii", "iin", "ill", "illiterate", "illustrator", "i`m", "im", "image",
"imagine", "img", "immediately", "immune", "imo", "impatient",
"implementation", "import", "improve", "improved", "in", "inbox", "inch",
"incident", "incomplete", "inconvenience", "indeed", "india", "indicates",
"individual", "indonesia", "inet", "inet6", "inetd", "infection", "infer",
"info", "inform", "infos", "ing", "in-game", "init", "initial", "initialize",
"initram", "injection", "inline", "insecure", "insert", "inserts", "inside",
"inspiron", "install", "installer", "installing", "instant", "instantly",
"insurance", "integrated", "intel", "intent", "interactive", "interested",
"interface", "interim", "internal", "internet", "internets", "interval",
"intrepid", "intro", "introduce", "invalid", "invert", "ioctl", "ios", "iot",
"ip", "ipad", "iphone", "ipod", "ips", "iptraf", "ir", "irc", "irs", "irssi",
"is", "isdn", "isee", "island", "isnt", "iso", "isp", "issue", "ist",
"istanbul", "it", "italiano", "itanium", "item", "ith", "itouch", "its", "itt",
"itunes", "iu", "iv", "ive", "iw", "iwl3945", "jackalope", "jaunty", "java",
"javascript", "jdk", "jeez", "jetzt", "jfs", "job", "jobs", "join", "joins",
"joke", "joomla", "jou", "journal", "joystick", "jre", "jump", "jumps", "junk",
"jus", "just", "justs", "k", "k6", "k7", "kaffeine", "kanji", "karmic",
"kazam", "kb", "kde", "kde4", "kdm", "keep", "keine", "kernal", "kernel",
"kewl", "key", "keyboard", "keygen", "keyring", "keys", "keystroke", "keyword",
"khz", "kick", "kicks", "kil", "kile", "kill", "killed", "killing", "kinda",
"kindly", "kino", "kiso", "kit", "kk", "kms", "knew", "knock", "know", "knows",
"knw", "koala", "kodi", "konquerer", "kontact", "kopete", "krusader", "ksirc",
"kthx", "kto", "kubuntu", "kvm", "l2", "la", "label", "lack", "lacking",
"ladies", "lagged", "lame", "lamp", "lan", "landlord", "landscape", "laptop",
"large", "laserjet", "last", "late", "latency", "later", "laugh", "laughing",
"launch", "launched", "launchpad", "law", "lay", "layer", "ldd", "le", "lead",
"leading", "leak", "lean", "lear", "learn", "learning", "leave", "leaves",
"left", "leg", "legacy", "legal", "lesbian", "less", "let", "letter", "level",
"lfe", "lib", "libc", "libet", "library", "libre", "license", "lid", "lie",
"life", "light", "lightning", "lights", "like", "liked", "likes", "limb",
"limewire", "limited", "line", "linear", "lines", "link", "linked", "links",
"links2", "linksys", "linux-", "linux", "linux-firmware", "linuxmce", "list",
"listen", "listening", "little", "live", "liveboot", "live-cd", "livecd",
"liveusb", "living", "lo", "load", "loaded", "loader", "loading", "lobby",
"local", "locales", "localhost", "locate", "locked", "lockup", "log",
"logging", "logical", "logically", "logins", "logo", "lol", "long", "longer",
"longterm", "look", "looking", "looks", "lookup", "loop", "loop0", "loopback",
"looping", "loose", "los", "lose", "losing", "loss", "lossless", "lossy",
"lost", "lot", "love", "lovely", "loving", "low", "lowest", "lpr", "ls",
"lsblk", "lsof", "lspci", "lts", "ltsp", "lubuntu", "lucid", "luck", "lug",
"luks", "lvm", "lxde", "lyx", "m", "m68k", "maas", "mabe", "mac", "macbookpro",
"machine", "machines", "macintosh", "macos", "macosx", "made", "mageia",
"mail", "mailserver", "main", "major", "majority", "make", "makefile", "makin",
"male", "malicious", "malone", "mam", "man", "manager", "mandatory",
"mandriva", "manger", "mangled", "manipulate", "many", "mapping", "marked",
"marketing", "massive", "mastering", "matchbox", "mate", "matter", "mature",
"maximum", "may", "maybe", "mb", "mbox", "mbr", "mce", "md5", "md5sum",
"mdadm", "me", "mean", "means", "mechanical", "media", "medicine", "medium",
"member", "men", "mention", "mentor", "menu", "mepis", "merci", "merge",
"merry", "mess", "metacity", "method", "me-tv", "mf1", "mga", "mhm", "mi",
"mic", "mice", "microsd", "microsoft", "midi", "might", "mikrotik", "mileage",
"min", "mind", "mine", "minecraft", "mines", "minimal", "minor", "mins",
"minute", "mirc", "mirror", "mirrored", "mirrors", "miserable", "misplaced",
"miss", "missed", "missing", "mistake", "mix", "mixer", "mixing", "mkay",
"mkdir", "mkv", "mldonkey", "mlr", "mmap", "mmh", "mmkay", "mobility",
"moblin", "mobo", "modding", "mode", "model", "modem", "modern", "modify",
"modinfo", "modprobe", "modular", "mol", "moment", "monde", "monitor",
"monitoring", "month", "moral", "more", "morning", "most", "mostly", "mother",
"motu", "mount", "mousepad", "mout", "move", "mozilla", "mp2", "mp3", "mpeg",
"mprime", "mpv", "mroe", "msdos", "msg", "msn", "mtp", "muck", "muh", "multi",
"multimedia", "munin", "music", "must", "muted", "mutt", "mv", "my", "mybe",
"mysql", "myuser", "\\n", "n", "na", "nah", "nahh", "name", "namely", "nar",
"narwhal", "nasty", "nat", "native", "natty", "navigator", "nay", "nbr", "nc",
"ncq", "ndiswrapper", "near", "nearby", "neat", "need", "neighbor", "neither",
"nerdy", "nervous", "nessus", "net", "netbios", "netbook", "netcat", "nethack",
"netmask", "netstat", "network", "networked", "networking", "networks",
"never", "new", "newbs", "newer", "newline", "news", "nexenta", "next",
"nexuiz", "nfs", "nfsv4", "nginx", "ni", "nice", "nicely", "nick", "nicks",
"nickspam", "nicotine", "nid", "nie", "nipple", "nmap", "no", "noapic",
"nobody", "nome", "non", "none", "nonsense", "noobs", "no-one", "nop", "nope",
"nor", "norm", "normal", "normally", "not", "note", "notes", "nothing",
"nouveau", "novell", "now", "np", "ns", "ntfs", "ntfs-3g", "ntp", "nuisance",
"number", "numbers", "nun", "nup", "nvidia", "nvm", "nx", "o", "obex",
"observing", "obv", "oct", "od", "odd", "odds", "oes", "of", "ofc", "ofcourse",
"off", "offense", "offensive", "offer", "offsets", "offtopic", "often", "ogl",
"ogle", "oh", "oi", "oic", "ok", "okay", "oki", "okies", "okk", "okkk", "oky",
"okz", "ola", "old", "omg", "on", "onboard", "once", "one", "ones", "online",
"only", "onto", "oof", "ook", "ooo", "oops", "op", "open", "openarena",
"openbox", "opend", "opened", "openerp", "opengl", "openoffice", "open-source",
"opensource", "opensuse", "openttd", "openvpn", "opinion", "ops", "option",
"or", "orange", "oranges", "order", "original", "originals", "oss", "osx",
"ot", "other", "others", "ouch", "oui", "out", "output", "outside", "ovaries",
"over", "overkill", "overloaded", "overlook", "override", "owa", "own",
"owned", "p2p", "p3", "p4", "pack", "package", "packets", "padding", "pae",
"pain", "painful", "paint", "pakage", "palm", "paman", "panasonic", "panic",
"para", "paragraph", "parallel", "parent", "parents", "park", "part",
"partition", "partitioner", "partner", "party", "pas", "pass", "passed",
"passwd", "password", "past", "paste", "pata", "patch", "patches", "patient",
"pattern", "patterns", "pavilion", "pay", "pc", "pcbsd", "pci", "pcm", "pcs",
"pctv", "pdf", "pearl", "peek", "peer", "pending", "pentium", "people",
"peoples", "per", "perfect", "performances", "perl", "permanent",
"persistence", "personal", "pesky", "peu", "pff", "pgp", "phd", "phew",
"philosophy", "phone", "phones", "photo", "photos", "php", "phpmyadmin",
"physical", "phyton", "pianobar", "pic", "picard", "pick", "pico", "pics",
"picture", "pictures", "pid", "pidgin", "pidof", "piece", "ping", "pingus",
"pink", "pint", "pipe", "pipes", "pity", "places", "plagued", "plain",
"plaintext", "plan", "play", "playback", "player", "playing", "please",
"plenty", "plex", "pls", "plug", "plugin", "plugins", "plugs", "plymouth",
"plz", "pm", "pocket", "pocketpc", "poff", "point", "pointer", "pointless",
"poke", "poking", "police", "polite", "poll", "pooched", "pool", "poor", "pop",
"pop3", "popup", "por", "porno", "port", "portable", "portage", "ports",
"portugues", "positive", "possible", "post", "postgres", "postgresql", "pour",
"pov", "power", "powered", "powerpc", "ppc", "ppl", "ppp0", "pppoe", "pptp",
"pra", "practical", "practice", "pre", "preferred", "prefixed", "preload",
"premiere", "preseed", "press", "pretty", "prety", "price", "primary", "print",
"printer", "prints", "prior", "priv", "privacy", "private", "privileged",
"prize", "prob", "probably", "probe", "problem", "problems", "proc", "proceed",
"process", "processor", "procs", "programer", "programming", "progress",
"progs", "prohibit", "project", "projects", "prolog", "prompt", "proper",
"props", "protect", "protection", "protocols", "prove", "proven", "provider",
"proxy", "prt", "pry", "ps", "ps2", "ps3", "psd", "psk", "psu", "ptp",
"public", "puel", "pulse", "pulseaudio", "pun", "purge", "purpose", "puta",
"putty", "puzzled", "pv", "pvt", "pwd", "pxe", "pxeboot", "q3", "qdisc",
"qemu", "qn", "qt", "quad", "quadro", "quake2", "quakenet", "qualcuno",
"quality", "quanta", "quantal", "que", "quel", "query", "question",
"questionable", "questioning", "questions", "questo", "quick", "quickly",
"quicksilver", "quit", "quotes", "r1", "r40", "r9", "raep", "ragazzi", "raid",
"raid0", "rails", "ramdisk", "ran", "random", "randomly", "rape", "rar",
"rare", "ratio", "rc", "re", "reach", "read", "reader", "reading", "readme",
"ready", "real", "realistic", "reality", "realize", "really", "realm",
"realplayer", "realtek", "realtime", "rear", "reason", "reasonable", "reasons",
"reboot", "reburn", "recall", "received", "recent", "reconnect", "record",
"recover", "recovery", "recreate", "recycle", "redhat", "redo", "reduce",
"refresh", "refund", "regard", "regenerate", "regenerating", "regexp",
"register", "regression", "regular", "reinstall", "reiserfs", "relate",
"relation", "relax", "relay", "release", "relevant", "reload", "reloaded",
"reloading", "rely", "remaster", "remastersys", "remember", "remembers",
"remix", "remote", "removed", "rename", "repair", "replaced", "replay", "repo",
"repro", "reproducing", "request", "required", "rerun", "rescue", "research",
"reservation", "reserved", "reset", "resolution", "resolve", "respectful",
"responce", "respond", "rest", "restart", "restricted", "results", "retards",
"return", "returning", "reverse", "revision", "rf", "rfc", "ribbon", "rid",
"ridiculous", "right", "ringtail", "ripoff", "ripping", "risk", "rite", "rl",
"rm", "rmdir", "road", "roaming", "rocks", "rolling", "roms", "room", "root",
"roulette", "routed", "router", "routing", "row", "rows", "rpi", "rpm",
"rsync", "rtf", "rtt", "ru", "rude", "ruin", "rule", "run", "runaway",
"runescape", "runlevel", "runs", "rushed", "rv8", "rvm", "rwx", "s3", "safe",
"safety", "said", "salut", "samba", "same", "samples", "sand", "sandbox",
"sandisk", "sans", "sansa", "sarcasm", "sasl", "sat", "sata", "saturday",
"saucy", "save", "saveas", "savvy", "saw", "sawfish", "say", "scaled", "scan",
"scandisk", "scheduler", "science", "scite", "scp", "scrambled", "scratch",
"screen", "screencast", "screening", "screensaver", "screenshot", "screw",
"screwed", "screwing", "script", "scripts", "scroll", "scrollbar", "scrolls",
"scsi", "sda3", "sda9", "sdc", "sdcard", "se", "seagate", "seahorse",
"seamonkey", "search", "searched", "searching", "seattle", "sec", "second",
"secondary", "secondlife", "security", "sed", "see", "seed", "seeking",
"segfaults", "select", "selection", "selective", "selinux", "selling", "sem",
"semicolon", "send", "sense", "sensible", "sent", "sentence", "senza",
"separate", "serial", "series", "serious", "seriously", "serpentine", "serve",
"server", "servers", "servlet", "session", "set", "seti", "setting", "setup",
"sever", "sex", "sfs", "sftp", "sh", "sha1", "shame", "sharing", "she",
"shell", "shells", "shellshock", "shift", "shipit", "shite", "sho", "shoes",
"shoot", "shoots", "shop", "short", "shortcut", "shortcuts", "shorter",
"shoutcast", "shouting", "shown", "shred", "shrink", "shrugs", "shuffle",
"shure", "shut", "shutdown", "shuttleworth", "si", "sick", "side", "sidebar",
"siema", "siemens", "sigh", "sign", "signal", "silence", "silently", "silly",
"sim", "similar", "simple", "simplicity", "simply", "simulate", "sing",
"single", "sips", "sir", "sis", "sistem", "sit0", "site", "situation",
"skills", "skin", "skype", "slang", "slaps", "slave", "sleep", "sleeping",
"sleeve", "slightly", "slow", "slower", "slowest", "slowing", "slowness",
"sm56", "small", "smarter", "smb", "sme", "smooth", "smp", "smth", "smtp",
"snaps", "snapshot", "snes", "snippets", "snmp", "so", "sobre", "socat",
"social", "socks", "soem", "soft", "software", "solar", "solution", "solving",
"som", "some", "some1", "somebody", "somehow", "someon", "someone",
"someplace", "somethin", "something", "somewhat", "somewhere", "somone",
"song", "songbird", "soo", "soon", "sooner", "soooo", "sorry", "sort", "sorta",
"sory", "soulseek", "sound", "soundblaster", "soundtrack", "source",
"sourcecode", "sourced", "sow", "sp2", "sp3", "space", "spam", "spanish",
"spe", "speak", "speaker", "speakers", "specs", "speed", "speeding",
"speedtouch", "spelling", "spin", "spinning", "spit", "splash", "split",
"splitter", "spoke", "spoofing", "spot", "spread", "sprint", "spurious",
"spyware", "sql", "squares", "squeeze", "srt", "ssb", "ssd", "ssh", "sshd",
"ssh-server", "ssl", "sta", "stack", "stacks", "stand", "standalone",
"standard", "standby", "starcraft", "start", "startkeylogger", "startx",
"stat", "state", "stated", "states", "static", "status", "stay", "stderr",
"stdout", "steady", "steam", "steep", "step", "steps", "stfu", "sthg",
"stickers", "sticks", "still", "stopped", "storage", "store", "strace",
"strain", "stream", "streamer", "street", "strength", "stress", "string",
"stripped", "stroke", "strong", "stronger", "stty", "stubborn", "stuck",
"study", "studying", "stuff", "stuffs", "stupid", "stupidity", "su", "subject",
"subnet", "subset", "substance", "subversion", "succeed", "sucker", "sucks",
"sucky", "suddenly", "sudo", "sudoers", "suffer", "suffering", "suffice",
"sugar", "sum", "sunday", "sup", "super-user", "supply", "suppor", "support",
"supybot", "sure", "surely", "surfing", "surprise", "survives", "suse",
"suspend", "sux", "svn", "swap", "swapon", "swedish", "sweeet", "sweet", "swf",
"swiftweasel", "switch", "switched", "switcher", "switches", "sym", "symbolic",
"symlinks", "synaptic", "synatic", "sync", "synoptic", "sys", "syscall",
"sysctl", "syslogd", "system", "system76", "systemd", "systems", "systray",
"sysv", "t", "t400", "t42", "t61", "ta", "tab", "tab-complete", "tablet",
"taboo", "tabs", "tails", "take", "taken", "taking", "talk", "talkin", "tanks",
"tap", "tape", "target", "tasks", "tcp", "tea", "teach", "teachers", "team",
"teams", "teamspeak", "technical", "techs", "tedious", "tee", "teh", "tel",
"television", "tell", "telling", "telnet", "temperature", "temporary", "tend",
"terminal", "terminate", "terminology", "terror", "terse", "tes", "tested",
"testing", "text", "tf2", "th", "tha", "thank", "thanks", "thankyou", "that",
"thats", "the", "theater", "them", "theme", "then", "theora", "there",
"therefore", "these", "they", "thier", "thik", "thing", "things", "think",
"thinking", "third", "this", "thng", "tho", "thos", "thought", "thoughts",
"thousands", "threads", "three", "threw", "throttled", "ths", "tht",
"thumbdrive", "thumbs", "thunar", "thunderbird", "thunk", "thus", "thx", "ti",
"tia", "ticking", "tie", "tiff", "tightvnc", "till", "time", "timeout",
"timers", "timestamp", "tip", "tips", "tired", "tis", "tit", "tivo", "tks",
"tlp", "tls", "tnx", "to", "toasted", "today", "together", "toilet",
"tomorrow", "tonight", "too", "took", "tool", "tools", "top", "topic", "tor",
"torrent", "toss", "total", "totem", "touch", "touched", "touchpad", "tough",
"tous", "tp", "tracert", "track", "tracker", "trackpoint", "tracks", "trafic",
"training", "transgaming", "transient", "transition", "translated",
"transparent", "trap", "trash", "travelmate", "tray", "trayer", "treat",
"tremulous", "trial", "trick", "tricky", "tried", "trigger", "triple",
"trivial", "trolling", "trolls", "trouble", "troubleshooter", "tru", "true",
"truly", "truncate", "trunk", "trusted", "trusty", "try", "trying", "tsc",
"ttf", "ttfn", "tthe", "tty", "tty1", "tue", "tune", "tuner", "tunes",
"tunnel", "turds", "tut", "tuto", "tutorial", "tutorials", "tutti", "tuxracer",
"tv", "tweaks", "twenty", "twin", "twitter", "twm", "two", "txt", "tym",
"type", "u", "uac", "uae", "ubnutu", "ubunto", "ubuntu-cn", "ubuntu-dev",
"ubuntu-es", "ubuntu-fr", "ubuntuguide", "ubuntu-server", "ubunutu", "ubutto",
"ues", "ufw", "ug", "ugh", "ughh", "ugly", "uh", "uhh", "uh-oh", "uhu", "uid",
"uk", "ulimit", "um", "uma", "umm", "ummm", "una", "unable", "unallocated",
"uname", "unbanned", "unbelievable", "unbound", "unbuntu", "unclean", "und",
"undefined", "under", "undo", "undone", "une", "unetbootin", "unfriendly",
"unhappy", "uni", "unicorn", "unified", "unit", "univ", "universe", "unix",
"unix-like", "unless", "unlike", "unlimited", "unlock", "unmanaged", "unplug",
"unplugged", "unregged", "unto", "untouched", "untrusted", "unused", "up",
"update", "updated", "updater", "updates", "upgrade", "upgrading", "uploaded",
"upon", "upside", "upstairs", "upstart", "uptime", "ur", "urban", "urgh",
"url", "urs", "us", "usa", "usb", "use", "user", "userb", "userid", "userland",
"users", "using", "usre", "ut", "ut2004", "utf-8", "util", "utils", "utopic",
"utorrent", "uxa", "v4l", "v8", "v9", "vagina", "vagrant", "vai", "vain",
"value", "values", "valve", "various", "vary", "vault", "vbox", "venezuela",
"vent", "ventrilo", "verbosity", "versatile", "version", "vertical", "very",
"vga", "vi", "via", "victory", "vid", "viet", "view", "vim", "virgin",
"virtual", "virtualbox", "virtualized", "virtualmachine", "visit", "vista",
"visual", "visually", "vlc", "vmlinuz", "vms", "vmstat", "vmware", "vnc",
"voip", "volume", "volunteer", "vorbis", "vpc", "vpn", "vps", "vram", "vs",
"vsftpd", "vt", "vulnerable", "w7", "w8", "wa", "wack", "wah", "waht", "wait",
"waiting", "walking", "wall", "wan", "wana", "wanna", "wanted", "warcraft",
"warning", "wary", "was", "washed", "wast", "waste", "watch", "watchdog",
"wav", "way", "wayland", "ways", "wbar", "we", "wear", "weather", "web",
"webadmin", "webhosting", "webmin", "webserver", "website", "wed", "weechat",
"weird", "welcom", "welcome", "well", "welll", "wep", "wer", "were", "werk",
"wget", "whacky", "what", "whatever", "whatis", "whee", "when", "where",
"wherever", "which", "while", "whim", "whit", "white", "whitespace", "who",
"whoa", "whole", "whomever", "whoops", "whore", "whose", "wht", "why", "wid",
"widescreen", "width", "wie", "wife", "wi-fi", "wifi", "wiki", "wikipedia",
"wildcards", "will", "willl", "win", "win2k", "win7", "winblows", "winbox",
"window", "windows", "windows7", "windoze", "wine", "winehq", "wink", "wins",
"winxp", "wipe", "wire", "wired", "wireless", "wiser", "wish", "wit", "witch",
"with", "without", "wl", "wlan", "wlan0", "wm", "wmware", "wo", "wobbly",
"wol", "woman", "wonder", "wondered", "wonderful", "wondering", "wont", "woof",
"woohoo", "woohooo", "woooo", "woops", "word", "work", "workbench", "worker",
"workgroup", "working", "works", "world", "worried", "worry", "wors", "worth",
"worx", "wow", "wrapper", "wrecked", "write", "writer", "writing", "written",
"wrong", "wtc", "wtf", "wubi", "wusb54g", "wxp", "x", "x11", "x64", "x86",
"x86_64", "xampp", "xandros", "xargs", "x-chat", "xchat", "xconfig", "xd",
"xdmcp", "xe1", "xenial", "xeyes", "xf86", "xfburn", "xfce", "xfire", "xfs",
"xfx", "xgl", "xine", "xls", "xmacro", "xml", "xmms", "xmonad", "xmpp", "xorg",
"xp", "xps", "xsane", "xscreen", "xt", "xterm", "xubuntu", "xv", "xvf", "ya",
"yakuake", "yawn", "yay", "yea", "yeah", "yeap", "yeh", "yell", "yelp", "yep",
"yer", "yes", "yess", "yessir", "yesterday", "yet", "yields", "yikes", "you",
"your", "yours", "yourself", "yourusername", "youtube", "youve", "yoy", "yp",
"yrs", "yummy", "yup", "yus", "yw", "zeros", "zesty", "zips", "znc", "zomg",
"zone",
}

def convert_word(word):
    nword = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode("ascii").strip().lower()
    nword = ''.join(nword.split())
    if len(nword) == 0:
        nword = "<unconvertable>"
    elif word.lower().startswith(nword) and len(nword) != len(word):
        nword += " <unconvertable>"
    elif word.lower().endswith(nword) and len(nword) != len(word):
        nword = "<unconvertable> " + nword
    return nword

def make_unk(word):
    has_digit = any(c in string.digits for c in word)
    has_letter = any(c in string.ascii_letters for c in word)
    marks = set()
    for c in word:
        if c in string.punctuation:
            marks.add(c)
    marks = list(marks)
    marks.sort()
    marks = ''.join(marks)

    ans = "<unk"
    if has_digit:
        ans += "#"
    if has_letter:
        ans += "a"
    ans += marks
    ans += ">"
    return ans

def apply_re(expression, done, todo, current, label=''):
    if len(current) == 0:
        return current
    else:
        # Split
        parts = []
        for v in re.split(expression, current):
            if v is not None and len(v) > 0:
                parts.append(label + v)

        # Push all but the start back on todo
        if len(parts) > 1:
            for part in parts[:0:-1]:
                if len(part) > 0:
                    todo.insert(0, part)

        return parts[0]

# Names two letters or less that occur more than 500 times in the data
common_short_names = {"ng", "_2", "x_", "rq", "\\9", "ww", "nn", "bc", "te",
"io", "v7", "dm", "m0", "d1", "mr", "x3", "nm", "nu", "jc", "wy", "pa", "mn",
"a_", "xz", "qr", "s1", "jo", "sw", "em", "jn", "cj", "j_"}

def tokenise(line, args, vocab, users, line_no):
    tokens = []

    parts = line.strip().split()
    # Handle timestamp and username
    if re.match(".*\[[0-9][0-9][:][0-9][0-9]\]$", parts[0]) is None:
        if args.edit_messages_only:
            return line.strip().split()
        timestamp = parts.pop(0)
        if not args.cut_timestamp:
            tokens.append(timestamp)
    else:
        timestamp = parts.pop(0)
        user = parts.pop(0)
        while user[-1] != '>' and len(parts) > 0:
            user +=" "+ parts.pop(0)
        if not args.cut_timestamp:
            tokens.append(timestamp)
        if not args.cut_username:
            tokens.append(user)

    # Handle message
    while len(parts) > 0:
        current = parts.pop(0)
        if not args.is_ascii:
            current = convert_word(current)
        else:
            current = current.lower()

        # Handle username mentions
        user = None
        if current in users and len(current) > 2:
            user = current
        else:
            core = [char for char in current]
            while len(core) > 0 and core[-1] in string.punctuation:
                core.pop()
                nword = ''.join(core)
                if nword in users and (len(core) > 2 or nword in common_short_names):
                    user = nword
                    break
            if user is None:
                while len(core) > 0 and core[0] in string.punctuation:
                    core.pop(0)
                    nword = ''.join(core)
                    if nword in users and (len(core) > 2 or nword in common_short_names):
                        user = nword
                        break
        if user is not None:
            cmin, cmax = users[user]
            if cmin - 1000 <= line_no <= cmax + 1000:
                subparts = current.split(user)
                if len(subparts[0]) > 0:
                    tokens.append(subparts[0])
                if args.replace_usernames:
                    tokens.append("<user>")
                else:
                    tokens.append(user)
                if len(subparts[-1]) > 0:
                    tokens.append(subparts[-1])
                current = ''
                continue

        #  - email (...@...) or prompt (...@...:...) make word shape (...@...) and split on ':'
        if "@" in current and (not current.startswith("@")) and (not current.endswith('@')):
            if len(current.split("@")) == 2:
                tokens.append("ADDRESS_" + current.split("@")[0])
                tokens.append("ADDRESS_@" + current.split("@")[1])
                current = ''
                continue

        #  - Permissions (only rwxd-), split into groups of three characters
        if len(current) == 10 and re.fullmatch("[-rwxd]+", current) is not None:
            tokens.append('PERMISSIONS_'+ current[:1])
            tokens.append('PERMISSIONS_'+ current[1:4])
            tokens.append('PERMISSIONS_'+ current[4:7])
            tokens.append('PERMISSIONS_'+ current[7:])
            current = ''
            continue

        #  - URLs (start with http, sftp, telnet) split on '/' and add it (http://) (...) (/.../) (/.../) ...
        if re.match("^((http)|(sftp)|(telnet)).*\/", current) is not None:
            chunks = [c for c in current.split("/") if len(c) != 0]
            tokens.append("URL/"+ chunks[0] +"/")
            if len(chunks) > 1:
                tokens.append("URL/"+ chunks[1] +"/")
                if len(chunks) > 2:
                    tokens.append("URL/"+ '/'.join(chunks[2:]) +"/")
            current = ''
            continue
        if current.startswith("www."):
            current = "URL/"+ current

        #  - ...[:;*,.?!)] and group repeats (... or ... or !?!!??!?!)
        current = apply_re("""([":;?!.,)}\]]+$)""", tokens, parts, current)

        #  - Directories (start with / or ~) split into pieces (/.../) (/.../)
        if re.match("^[~/]", current) is not None:
            chunks = current.split("/")
            for chunk in chunks:
                if len(chunk) > 0:
                    tokens.append("DIR/"+ chunk +"/")
            current = ''
            continue

        #  - [!({[]...
        current = apply_re("""(^["!({[]+)""", tokens, parts, current)

        #  - ...'s  ...n't  ...'ll  ...'m ...'ve (and in all cases allow ' or ")
        current = apply_re("""(['"]s)$""", tokens, parts, current)
        current = apply_re("""(n['"]t)$""", tokens, parts, current)
        current = apply_re("""(['"]ll)$""", tokens, parts, current)
        current = apply_re("""(['"]m)$""", tokens, parts, current)
        current = apply_re("""(['"]ve)$""", tokens, parts, current)

        #  - mid-word ellipses (e.g. know...But)
        current = apply_re("""([.][.]+)""", tokens, parts, current)

        #  - Instructions like "System->Admin->Shared" split on "[-]?>"
        current = apply_re("""([-]?[>])""", tokens, parts, current)

        #  - "s/.../..." to "substitution / ... / ... /"
        if re.match("s/.*/", current) is not None:
            for chunk in current.split("/"):
                if len(chunk) > 0:
                    tokens.append("SUB/"+ chunk +"/")
            current = ''
            continue

        #  - Numbers (do not convert all numbers to 0, as 32 != 64)
        # versions, etc, so not worth collapsing

        if len(current) > 0:
            tokens.append(current)

    if args.add_line_boundaries:
        tokens.insert(0, "<s>")
        tokens.append("</s>")

    # Add unks
    if len(vocab) > 0:
        for i, token in enumerate(tokens):
            if i == 0 and (not args.cut_timestamp):
                continue
            if i == 1 and (not args.cut_username):
                continue
            if token.lower() not in users and token not in vocab:
                tokens[i] = make_unk(token)

    return tokens

def update_user(users, user, line_no):
    if user in reserved:
        return
    all_digit = True
    for char in user:
        if char not in string.digits:
            all_digit = False
    if all_digit:
        return

    if user not in users:
        users[user] = (line_no, line_no)
    else:
        cmin, cmax = users[user]
        users[user] = (min(cmin, line_no), max(cmax, line_no))

def update_users(line, users, line_no):
    if len(line.split()) < 2:
        return
    user = line.split()[1]
    if user in ["Topic", "Signoff", "Signon", "Total", "#ubuntu",
            "Window", "Server:", "Screen:", "Geometry", "CO,",
            "Current", "Query", "Prompt:", "Second", "Split",
            "Logging", "Logfile", "Notification", "Hold", "Window",
            "Lastlog", "Notify", 'netjoined:']:
        # Ignore as these are channel commands
        pass
    else:
        if line.split()[0].endswith("==="):
            parts = line.split("is now known as")
            if len(parts) == 2 and line.split()[-1] == parts[-1].strip():
                user = line.split()[-1]
        elif line.split()[0][-1] == ']':
            if user[0] == '<':
                user = user[1:]
            if user[-1] == '>':
                user = user[:-1]

        user = user.lower()
        update_user(users, user, line_no)
        # This is for cases like a user named |blah| who is
        # refered to as simply blah
        core = [char for char in user]
        while len(core) > 0 and core[0] in string.punctuation:
            core.pop(0)
        while len(core) > 0 and core[-1] in string.punctuation:
            core.pop()
        core = ''.join(core)
        update_user(users, core, line_no)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tokenise content from IRC logs.')
    parser.add_argument('--cut_timestamp', help='Remove the timestamp.', action='store_true')
    parser.add_argument('--replace_usernames', help='Replace usernames in messages with a placeholder.', action='store_true')
    parser.add_argument('--cut_username', help='Remove the username of the author.', action='store_true')
    parser.add_argument('--add_line_boundaries', help='Add tokens to indicate the start and end of a line.', action='store_true')
    parser.add_argument('--edit_messages_only', help='Keep non-message content as is.', action='store_true')
    parser.add_argument('--use_vocab', help='Use a vocab file to limit what is generated.')
    parser.add_argument('--output_suffix', help='Save to files with the suffix added.')
    parser.add_argument('--is_ascii', help='No need to convert to ascii.', action='store_true')
    parser.add_argument('--users_from_future', help='Make the user name list with future users too.', action='store_true')
    parser.add_argument('raw_data', help='File containing the raw logs.', nargs="+")
    args = parser.parse_args()

    vocab = set()
    if args.use_vocab is not None:
        for line in open(args.use_vocab):
            vocab.add(line.strip().split()[-1])
    log_file = open("progress.txt", 'a', 1)
    print("running", file=log_file)
    for input_filename in args.raw_data:
        print("Doing", input_filename, file=log_file)
        try:
            out = sys.stdout
            if args.output_suffix is not None:
                out = open(input_filename + args.output_suffix, 'w')

            users = {}
            if args.users_from_future:
                line_no = 0
                for line in open(input_filename):
                    line_no += 1
                    update_users(line.strip(), users, line_no)

            line_no = 0
            for line in open(input_filename):
                line_no += 1
                line = line.strip()
                if not args.users_from_future:
                    update_users(line, users, line_no)
                tokens = tokenise(line, args, vocab, users, line_no)
                print(' '.join(tokens), file=out)
                if line_no % 1000 == 0:
                    out.flush()
        except Exception as e:
            print("failed", input_filename, file=log_file)
            traceback.print_exc()
        if args.output_suffix is not None:
            out.close()
        log_file.flush()

