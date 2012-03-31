KOMENTÁŘE K SEMESTRÁLNÍ PRÁCI
    verze 2012



Konstruktor brainfucku má následující potřebné parametry:
    BrainFuck(DATA)
        ~ jednoduchá inicializace s daty programu (jako řetězec)
    BrainFuck(DATA).run()
        ~ vykonání zavedeného programu
    BrainFuck(DATA).output
        ~ řetězec výstupu, který vyprodukuje běžící program voláním brainfuckovského příkazu '.'
    BrainFuck(DATA).memory_pointer
        ~ ukazatel do paměti/pásky
    BrainFuck(DATA).get_memory()
        ~ vrací paměť/pásku jako binární řetězec

Jeho plné volání je následující:
    BrainFuck(DATA, memory=b'\x00', output='', instruction_pointer=0, memory_pointer=0, show_output=True)
přičemž navíc:
    ~ show_output : ukaž/potlač výstup brainfuckovského programu generovaný příkazem '.'
                    (hodnota atributu 'output' se ale nastavuje nezávisle na tomto)
    ~ instruction_pointer : ukazuje pozici v instrukcích programu
                            (v testech se nevyskytuje)



Třída BrainLoller (a též BrainCopter pro ty, co ho budou implementovat) musí obsahovat metodu 'load()', která způsobí načtení dat brainfuckovského programu z dat PNG-obrázku.
    ~ To znamená, že load() na pozadí zavolá PngReader.load() a jím vygenerovaný seznam (R,G,B)-trojic převede podle převodních pravidel daného jazyka do příkazů brainfucku.
    ~ Konkrétní implementace (zvláště načítání PNG) je na vás, v (letošních :-) testech se netestuje.



Třída PngReader slouží k oddělení zpracování PNG-obrázků od zpracování samotných jazyků.
    ~ Konkrétní implementace je na vás, v (letošních :-) testech se netestuje.



Program se bude k uživateli chovat přívětivě, tzn. bude umět vyhodnotit špatné vstupy a poskytne nápovědu, přibližně něco jako následující dvě ukázky:

$> python3.2 __main__.py
usage: __main__.py [-h] [--version] [-l] [-c] file
__main__.py: error: too few arguments

$> python3.2 __main__.py --help
usage: __main__.py [-h] [--version] [-l] [-c] file

positional arguments:
  file               Soubor ke zpracování.

optional arguments:
  -h, --help         show this help message and exit
  --version          show program's version number and exit
  -l, --brainloller  Jde o program v jazyce brainloller.
  -c, --braincopter  Jde o program v jazyce braincopter.
