# KeyboardProfile-LoginSystem
This is the git repository for my BSC Thesis. The project is about a website/programme that uses keyboard patterns and profile creation as a means for a login system instead of a password. 

# Webprogramozás anyagok
Ide összeszedtem az összes infót nagyon röviden összetömörítve a webprogramozásról, illetve amit csak tudtam hasznos resource-okat, belinkeltem.

## Kliensoldal
A JavaScript a böngészőben fut, tehát a felhasználó gépén (ezért is hívjuk kliensoldalinak). Bármit is csinálunk benne, ahhoz a felhasználó hozzáfér.

### Első JavaScript kód
Bármilyen böngéészőben meg tudjuk nyitni a konzolt (általában az F12 gombbal). Csináljunk egy `index.html` filet és nyissuk meg böngészővel.

```HTML
<body>
    <h1>Állatok</h1>
    <div>Az állatok cukik.</div>
    <ul id="animals-list">
        <li class="animal">Boci</li>
        <li class="animal">Cica</li>
        <li class="animal">Maci</li>
    </ul>
</body>
```

Megnyomva az F12-t megjelennek a fejlesztői eszközök, ezek közül a konzol/console kell nekünk. Ide úgy tudunk írni, mint egy Python konzolba. Ha valamit beírunk, az rögtön lefut, és kiírja a visszatérési értékét. Például:
```
5+7
```

```
'alma'+'fa'
```

Persze nem szeretnénk örökre a konzolba írni. Hozzunk létre egy `script.js` filet, és jelezzük a HTML file-unkban, hogy ezt a scriptet szeretnénk futtatni:
```HTML
<body>
    ...
</body>
<script src="script.js"></script>
```
Amikor a böngésző elér a `script` taghez, lefuttatja a fileban lévő kódot (tehát ha módosítunk a kódban valamit, a file mentése után az oldalt újra kell tölteni F5-tel; vagy lehet live servert futtatni).

Írjuk bele a script fileba a következőt:
```JS
console.log(5+7)
console.log('alma'+'fa')
```
Ha elmentjük, és frissítjük az oldalt, meg is jelenik a konzolon.

### Típusok, változók
A JavaScript gyengén dinamikusan típusos, így hasonlít valamennyire a Pythonhoz. Változót a `let` vagy a `const` kulcsszóval hozhatunk létre. Stringeket létre tudunk hozni sima idézőjellel `'`, dupla idézőjellel `"` és backtickel is `` ` ``. Az első kettő közt nincs jelentős különbség, a backtick viszont behelyettesíthető (string template literálok).
```JS
const name = 'Brumi'
let age = 7

console.log(`${name} maci ${age} éves`)
```

A tömbök JavaScriptben olyasmik, mint a Python listák. Bármit bele lehet tenni, bármit kivenni. Persze célszerű hasonló dolgokat elhelyezni benne.
```JS
const randomArray = [1, true, 'valami', ['belső tömb', 7], null]
const animalNames = ['Peti', 'Geri']

animalNames.push('Brumi')

console.log(animalNames)
console.log(animalNames[0])
```

Az objektumok olyasmik, mint a Python dictionaryk. Bérmilyen attribútumot beléjük pakolhatunk, akár ad-hoc is.
```JS
const peti = {
    name: 'Peti',
    age: 8,
    species: 'boci'
}

console.log(peti)
```

A konstans tömb/objektum nem azt jelenti, hogy az attribútumokat nem változtathatjuk, csak azt, hogy nem változtathatjuk meg, mire "mutat" a változó.
```JS
const constTxt = 'valami'
const constArr = [1,2,3]
const constObj = {attr: 'valami'}

constTxt = 'valami más' // ez hibát dob
constArr = [4,5,6] // ez hibát dob
constObj = {attr: 'valami'} // ez hibát dob

constArr.push(4) // ez nem dob hibát
constObj.attr = 'valami más' // ez nem dob hibát
```

### Vezérlési szerkezetek
Az elágazások nem túl izgalmasak. Ciklusokból többféle van. A for-of az, ami pythonban a for-in, cpp-ben a for-: tehát iterál az elemeken. Viszont a for-in ciklus javascriptben az indexen iterál, nem az elemeken.
```JS
if(true){

}else if(false){

}else{

}

for(let i = 0; i < animalNames.length; i++){
    console.log(animalNames[i])
}
for(const i in animalNames){
    console.log(animalNames[i])
}
for(const name of animalNames){
    console.log(name)
}
```

### Függvények
A függvényeknek tetszőleges paraméterei, visszatérési értékei lehetnek.
```JS
function logThis(text){
    console.log(text)
    // nincs visszatérési érték
}
function isEven(number){
    return number % 2 == 0
}
function sum(num1, num2){
    return num1 + num2
}
```

Minden függvény egy objektum, így igazából változóként is létrehozhatjuk őket.
```JS
const isOdd = function (number){
    return number % 2 != 0
}
```

Ha pedig nagyon röviden akarjuk írni, használhatunk ú.n. arrow functiont, aminek ha egy paramétert adunk, akkor nem kell zárójel a paraméterek köré, ha pedig csak egy visszatérési értéke van, akkor még kapcsos zárójel se kell.
```JS
const multiply1 = (num1, num2) => {
    return num1 * num2
}
const multiply2 = (num1, num2) => num1*num2
const doubleThis = num => 2*num
```

### Tömbfüggvények
A tömböknek rengeteg beépített függvénye van, amik könnyítik a programozást. Ezek egy-egy függvényt várnak paraméterül, amit akár külön létre is hozhatunk, de egyszerűen arrowfunctionként is létre tudjuk hozni. (A console log tud több paramétert kapni, válasszuk el vesszővel). Ha egy tömbfüggvény tömböt ad vissza, azon tudunk további tömbfüggvényt futtatni. A forEach egy újabb ciklusiterációs módszer.
```JS
const numbers = [1, 4, 9, 2, 15]
console.log(
    numbers.some(num => num % 2 == 0),
    numbers.some(isEven),
    numbers.every(isEven),
    numbers.find(isEven),
    numbers.findIndex(isEven),
    numbers.filter(isEven),
    numbers.map(doubleThis)
)

console.log(
    numbers
        .map(doubleThis)
        .filter(num => num > 16)
        .some(num => num % 4 == 0)
) // megmondja, hogy a számok duplái közül azok közt, amik nagyobbak, mint 16, van-e 4-gyel osztható

numbers.forEach(num => console.log(num))
numbers.forEach((num, index) => console.log(index, num))
```

### Dokumentum és kimenet
A JavaScript nagy előnye, hogy be tudunk olvasni elemeket és ki tudunk írni infókat. A beolvasáshoz ismernünk kell az ú.n. CSS selectorokat.
- Ha egy konkrét `id`-jú elemet keresünk, azt `#` jellel lehet elérni.
- Ha egy bizonyos `class`-ba tartozó elemeket keresünk, azt a `.` jellel lehet elérni.
- Elemeket szóközzel láncolhatunk, ha egymásban vannak, szóköz nélkül, ha az adott attribútum az elemre vonatkozik.
    - `animals` ID-jú lista: `li#animals`
    - egy `div`-ben található `animals` ID-jú elem: `div #animals`
    - `animal` osztályú elemek egy `animals` ID-jú listában: `#animals .animal`
Ezeket JavaScriptben a `quareSelector` és a `querySelectorAll` függvényekke érhetjük el. Ezeket más elemeken hívhatjuk meg.

```JS
const animalUL = document.querySelector('#animals')
let animalLIs = document.querySelectorAll('#animals .animal') // később változtatjuk, azért let
// let animalLIs = animalUL.querySelectorAll('.animal') // ez ugyanazt csinálja, mint a felette lévő sor

console.log(animalUL.innerText)
console.log(animalUL.innerHTML)
animalLis.forEach(elem => console.log(elem.innerText))

const title = document.querySelector('h1')
title.innerText = 'Állatkák'
```

Így bonyolultabb dolgokat is generálhatunk.

```JS
const animals = [
    { name: 'Peti', age: 8, species: 'boci' },
    { name: 'Geri', age: 9, species: 'cica' },
    { name: 'Brumi', age: 7, species: 'maci' },
]

animalUL.innerHTML = ''
animals.forEach(animal => {
    animalUL.innerHTML += `<li>${animal.name} (${animal.species})</li>`
})
```

### Események
A JavaScript legfontosabb képessége az eseménykezelés. Megmondhatjuk, hogy milyen elemet szeretnénk figyelni, és milyen esemény hatására mi történjen vele.

Rakjunk egy plusz input mezőt és egy plusz gombot a HTML-be (nem csak gombokhoz rendelhetünk klikkelés eseményt, de logikus azt használni).
```HTML
<body>
    <h1>Állatok</h1>
    <div>Az állatok cukik.</div>
    <input id="animal-input"> <button id="add-btn">Hozzáad</button>
    <ul id="animals-list">
        <li class="animal">Boci</li>
        <li class="animal">Cica</li>
        <li class="animal">Maci</li>
    </ul>
</body>
```

Az `addEventListener` függvény egy elemet figyel. Első paramétere egy esemény neve. Második paramétere egy függvény, ami egy paramétert kap, a megtörténő eseményt.
```JS
const animalInput = document.querySelector('#animal-input')
const addButton = document.querySelector('#add-btn')

addButton.addEventListener('click', event => {
    console.log(event)

    animalUL.innerHTML += `<li>${animalInput.value}</li>`
})
```

Csináljunk egy stílust a HTML-be.
```HTML
<style>
    .fancy {
        color: red;
        text-decoration: underline;
    }
</style>
<body>
    ...
```

Ilyen stílusosztályt tudunk hozzáadni, elvenni és be/ki kapcsolni elemeken. (Ezeket külön külön add meg a kódnak konzolból, mert az kódbeli stílusváltozásokat egyszerre dolgozza fel).
```JS
animalUL.classList.add('fancy')
animalUL.classList.remove('fancy')
animalUL.classList.toggle('fancy')
```


Ha sok egyforma elemhez szeretnénk eseménykezelőket rendelni, használhatunk ciklust, de ez nem a szép megoldás, mert amikor új listaelemet adunk hozzá, nem lesz eseménykezelőnk.
```JS
animalLIs = animalUL.querySelectorAll('.animal')
animalLIs.forEach(li => {
    li.addEventListener('click', event => {
        li.classList.toggle('fancy')
    })
})
```

Ehelyett használhatjuk az okos delegáló függvényt (nem fontos, mi van benne, csak hogy hogyan használjuk). A delegáló függvény vár egy szülő elemet, amiben sok hasonló gyerek lesz, és hozzárendel egy-egy eseménykezelőt. Az eseménykezelő függvény két paraméteres, megkapja az eseményt, és a gyerek elemet amin az esemény megtörtént.
```JS
function delegate(parent, child, when, what){
    function eventHandlerFunction(event){
        let eventTarget  = event.target;
        let eventHandler = this;
        let closestChild = eventTarget.closest(child);

        if(eventHandler.contains(closestChild)){
            what(event, closestChild);
        }
    }

    parent.addEventListener(when, eventHandlerFunction);
}

delegate(animalUL, '.animal', 'click', (event, elem) => {
    elem.classList.toggle('fancy')
})
```

## További content
- [Thor GitHub](https://bit.ly/web-thor)
- [A böngésző mint alkalmazásfejlesztési platform](http://webprogramozas.inf.elte.hu/tananyag/kliens/)
- [Régebbi, kicsit elavult tananyag](http://webprogramozas.inf.elte.hu/tananyag/wf2/index.html)
- Gyakorló feladatok
    - [1. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/01)
    - [2. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/02)
    - [3. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/03)
    - [4. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/04)
    - [5. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/05)
    - [6. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/06)
    - [7. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/07)
- Előadások
    - [Bevezetés, követelmények, JavaScript nyelvi alapok](http://webprogramozas.inf.elte.hu/webprog/lectures/01/#/)
    - [Felületi elemek programozása: a DOM](http://webprogramozas.inf.elte.hu/webprog/lectures/02/#/)
    - [Interaktív programok készítése a böngészőben: eseménykezelés](http://webprogramozas.inf.elte.hu/webprog/lectures/03/#/)
    - [Alkalmazásfejlesztési alapelvek, kódszervezés](http://webprogramozas.inf.elte.hu/webprog/lectures/04/#/)
    -  [Időzítők. Adattárolás. Űrlapok, képek, táblázatok. További nyelvi elemek](http://webprogramozas.inf.elte.hu/webprog/lectures/05/#/)
    - [Canvas, animációk, API-k](http://webprogramozas.inf.elte.hu/webprog/lectures/06/#/)
    - [Aszinkron műveletek, AJAX, this, hibakezelés](http://webprogramozas.inf.elte.hu/webprog/lectures/07/#/)
- Gyakorlati videók
    - [VSCode ismertetése, vezérlési szerkezetek, tömbfüggvények](https://web.microsoftstream.com/video/0841844f-f8e3-4e46-8a8b-650d3f58b4a8)
    - [DOM alapok - kör kerülete](https://ikelte-my.sharepoint.com/:v:/g/personal/gyozke_inf_elte_hu/EXkjovxIQgFS2V7O6FA0IioB1VIbFOsjdo-zCwTxfp3LvA?e=f7QIxc&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)
    - [Eseménykezelés - todo lista](https://web.microsoftstream.com/video/98825c05-1e0c-47c3-8fc4-8e6e5b0e18f4)
    - [Eseménykezelés - hivatkozások letiltása](https://ikelte-my.sharepoint.com/:v:/g/personal/gyozke_inf_elte_hu/ET5OS-6REhhSZ4uKvUm8uOoBS30cFxE5OesOssfcISgkdA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=x5mFjb)
    - [Alkalmazásfejlesztés - számkitalálós játék](https://ikelte-my.sharepoint.com/:v:/g/personal/gyozke_inf_elte_hu/EZQgn6WL3AZXDnO-0IORih8BkuYyCcbwbIIFhiEa1lYV0A?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=xTOIea)
    - [Alkalmazásfejlesztés - aknakereső 1.](https://youtu.be/2TAvb2hjAw8)
    - [Alkalmazásfejlesztés - aknakereső 2.](https://youtu.be/wh6DXcSInlE)
    - [Alkalmazásfejlesztés - aszterodia 1.](https://ikelte-my.sharepoint.com/:v:/g/personal/gyozke_inf_elte_hu/EaY5wyvCzKFVOedFNkvy7-MB0DJqPA0VF-H14jJJ49waBA?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=mbt78U)
    - [Alkalmazásfejlesztés - aszteroida 2.](https://web.microsoftstream.com/video/037a50ff-7d69-44e9-a74f-105683ccc75f)

## Szerveroldal
A PHP egy szerveroldali programozási nyelv, ami dinamikus weboldalak készítésére alkalmas. A HTML-lel ellentétben a PHP kódot a szerver értelmezi, és a böngésző csak a végső eredményt kapja meg HTML-ként. A PHP-t telepíteni kell a gépünkre, nem tudja natívan értelmezni. Telepítés: [https://github.com/totadavid95/PhpComposerInstaller](https://github.com/totadavid95/PhpComposerInstaller)

### Első PHP kód
Hozzunk létre egy `index.php` filet. Ebbe bármilyen HTML kódot írhatunk.
```PHP
<body>
    <h1>Állatok</h1>
    <div>Az állatok cukik.</div>
    <ul id="animals-list">
        <li class="animal">Boci</li>
        <li class="animal">Cica</li>
        <li class="animal">Maci</li>
    </ul>
</body>
```
A PHP olyan, mintha egy új HTML taget nyitnánk. Ami ebben a tagben van, az PHP kód. (Lehet, hogy itt a syntax highlight nem olyan szép.)
```PHP
<body>
    <h1>Állatok</h1>
    <div>Az állatok cukik.</div>
    <?php
        // Ez itt php kód.
        // Pontosvessző a sor végén kötelező hosszúPHP tagben.
    ?>
    <ul id="animals-list">
        <li class="animal">Boci</li>
        <li class="animal">Cica</li>
        <li class="animal">Maci</li>
    </ul>
</body>
```
Mivel alapvetően kimenet generálására szolgál, tudjuk meg, milyen kimenetet lehet generálni.
```PHP
<ul id="animals-list">
    <li class="animal"><?php echo "Boci" ?></li>
    <li class="animal"><?php echo "Cica" ?></li>
    <li class="animal"><?php echo "Maci" ?></li>
</ul>
```
De ki akar ennyi mindent írni? Ha csak egy echo utasítást akarunk írni, arra van külön tag. (Nyilván itt most egy konkrét stringet ki-echozni nem annyira hasznos, de a példát jól mutatja).
```PHP
<ul id="animals-list">
    <li class="animal"><?="Boci"?></li>
    <li class="animal"><?="Cica"?></li>
    <li class="animal"><?="Maci"?></li>
</ul>
```

### Típusok, változók
A PHP-ban változókat `$` jellel jelölünk. A változók típusát nem kell deklarálni, a nyelv automatikusan felismeri.
```PHP
<?php
    $number1 = 10;
    $number2 = 20;

    $sum = $number1 + $number2;
    $difference = $number1 - $number2;
    $product = $number1 * $number2;
    $quotient = $number1 / $number2;
?>
<body>
    <?="Összeg: $sum, különbség: $difference, szorzat: $product, hányados: $quotient"?>

    vagy szebben

    Összeg: <?=$sum?>, különbség: <?=$difference?>, szorzat: <?=$product?>, hányados: <?=$quotient?>
</body>
```

A tömbök hasonlítanak a JS-hez.
```PHP
<?php
$animalNames = ["Peti", "Geri"];
$animalNames[] = ["Brumi"];
?>
<body>
    <?=$animalNames[0]>
</body>
```

Dictionary jellegű dolgot kétféle képpen tudunk létrehozni: asszociatív tömbként vagy objektumként.
```PHP
<?php
$assocArrayPeti = [
    "name" => "Peti",
    "species" => "boci",
    "age" => 8
];
$objectPeti = (object)[
    "name" => "Peti",
    "species" => "boci",
    "age" => 8
];
?>
<body>
    <?=$assocArrayPeti["name"]?> <br>
    <?=$objectPeti->name?> <br>
</body>
```

### Vezérlési szerkezetek
A ciklusok PHP-ban azért nagyon izgalmasak, mert kimenetgenerálásra tudjuk őket használni.
```PHP
<?php
    $animals = [
        (object)[ "name" => 'Peti',  "age" => 8, "species" => "boci" ],
        (object)[ "name" => 'Geri',  "age" => 9, "species" => "cica" ],
        (object)[ "name" => 'Brumi', "age" => 7, "species" => "maci" ],
    ]

    if(true){

    }else if(true){

    }else{

    }

    for($i = 0; $i < 10; $i++){
        var_dump($i); // a var dump függvény kidobja helyben az eredményt, mintha log lenne, hiszen a PHP nem fér hozzá a böngésző konzolhoz
    }
?>
<body>
    <ul>
        <?php
            foreach($animals as $animal){
                $name = $animal->name;
                $species = $animal->species;
                echo "$name ($species)";
            }
        ?>
    </ul>

    <ul>
        <?php foreach($animals as $animal): ?>
            <li><?=$animal->name?> (<?=$animal->species?>)</li>
        <?php endforeach; ?>
    </ul>
</body>
```

### JSON file feoldolgozása
A JSON a JavaScript Object Notation, egy standard file formátum. Hozzuk létre az `animals.json` filet.
```JSON
[
    {"name":"Peti","age":8,"species":"boci"},
    {"name":"Geri","age":9,"species":"cica"},
    {"name":"Brumi","age":7,"species":"maci"}
]
```
Ezt PHP-val be tudjuk olvasni.
```PHP
<?php
$json = file_get_contents("animals.json");
$data = json_decode($json);
?>
<body>
<ul>
    <?php foreach($data as $animal): ?>
        <li><?=$animal->name?> (<?=$animal->species?>)</li>
    <?php endforeach; ?>
</ul>
</body>
```
Vagy beleírni.
```PHP
$json = file_get_contents("animals.json");
$data = json_decode($json);

$data[] = (object)[ "name" => 'Arcsi', "age" => 8, "species" => "kutyus" ]; // a $tomb[] a push

$json = json_encode($data);
file_put_contents("animals.json", $json);
```

### Űrlapok
Az adatmozgatás oldalak közt kéréseken keresztül működik. A kettő legfontosabb a GET metódus és a POST metódus. A GET metódus az, amit gyakran látni böngészők címsávjában kérdőjelle és & jelekkel.  
Például: `google.com/search?client=firefox-b-d&q=alma`
- a `client` attribútum értéke `firefox-b-d`
- a `q` (query, keresőkifejezés) attribútum értéke `alma`

Egy űrlapon a `method` adja meg a metódust, az `action` pedig azt, hogy milyen oldalra irányítson az űrlap a kérés lefutásakor.

Ez az űrlap például helyben hagy az `index.php` oldalon, és egy `POST` kéréssel irányít ide vissza.
```HTML
<form action="index.php" method="post">
  <input type="text" name="name">
  <input type="submit">
</form>
```

Hozzunk létre egy `other.php` filet. Az `index.php`-ba írjuk bele a következőt.
```HTML
<body>
    <form action="other.php" method="get">
        <input name="name"> <br>
        <input name="age"> <br>
        <input name="species"> <br>
        <input type="submit">
    </form>
</body>
```

A `$_GET` és a `$_POST` változók minden oldalon jelen vannak, mindig hozzájuk férünk, de csak akkor van bennük bármi is, ha a megfelelő kéréssel érkeztünk az oldalra. Az `other.php`-ba pedig a következőt.
```PHP
<?php
$newElement = (object)[
    "name" => $_GET["name"],
    "age" => intval($_GET["age"]), // mindig szöveget küldönk kérésekben, át kell alakítani
    "species" => $_GET["species"]
];

$json = file_get_contents("animals.json");
$data = json_decode($json);

$data[] = $newElement;

$json = json_encode($data);
file_put_contents("animals.json", $json);

header('Location: index.php'); // ez visszairányít az index.php oldalra
die; // ezt a biztonság kedvéért rakjuk ide, mert a header függvény nem állítja meg a script futását, szóval ha lenne még utána 1000 sor, az lefutna, csak közben a felhasználó már másik oldalon lesz.
```

### Munkamenet
A munkamenet (session) lényege, hogy információt tároljunk, ami megmarad a böngészési folyamat során. Egy munkamenet egy kliens gépén egy böngészöben jön létre, és egyedien azonosítja azt.

Csináljunk egy `login.php` oldalt.
```PHP
<?php
session_start();
$_SESSION["user"] = $_POST["username"];

header('Location: index.php')
die;
```

Csináljunk egy `logout.php` oldalt.
```PHP
<?php
session_start();
session_unset();
session_destroy();

header('Location: index.php')
die;
```

És az `index.php` legyen a következő.
```PHP
<?php
    $logged_in = isset($_SESSION["user"]);
>
<body>
    <?php if($logged_in): ?>
        <h1>Szia <?=$_SESSION["user"]?>!</h1>
         <form action="logout.php" method="post">
            <input type="submit" value="Kijelentkezés">
        </form>
    <?php else: ?>
        <h1>Vendég</h1>
        <form action="login.php" method="post">
            <input name="username"> <br>
            <input type="submit" value="Bejelentkezés">
        </form>
    <?php endif ?>
</body>
```

## További content
- [Thor GitHub - ugyanaz a link mint a kliensoldal fejezetben](https://bit.ly/web-thor)
- [Dinamikus weboldalak előállítása szerveroldali technológiákkal](http://webprogramozas.inf.elte.hu/tananyag/szerver/)
- [Régebbi, kicsit elavult tananyag - ugyanaz a link mint a kliensoldal fejezetben](http://webprogramozas.inf.elte.hu/tananyag/wf2/index.html)
- Gyakorló feladatok
    - [8. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/08)
    - [9. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/09)
    - [10. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/10)
    - [11. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/11)
    - [12. gyak](http://webprogramozas.inf.elte.hu/#!/subjects/webprog-pti/gyak/12)
- Előadások
    - [Szerveroldali webprogramozás, HTTP, PHP, kimenet generálás](http://webprogramozas.inf.elte.hu/webprog/lectures/08/)
    - [Kliensoldali adatok mint bemenet, űrlapfeldolgozás](http://webprogramozas.inf.elte.hu/webprog/lectures/09/)
    - [Adattárolás](http://webprogramozas.inf.elte.hu/webprog/lectures/10/)
    - [Munkamenet, hitelesítés](http://webprogramozas.inf.elte.hu/webprog/lectures/11/)
    - [AJAX](http://webprogramozas.inf.elte.hu/webprog/lectures/12/)
    - [Kódszervezés, tervezési minták, kitekintés](http://webprogramozas.inf.elte.hu/webprog/lectures/13/)
- Gyakorlati videók
    - [Környezet beállítása, PHP nyelvi elemek, kimenet generálása](https://web.microsoftstream.com/video/799ffa49-953c-4b6b-a038-96944729cafc)
    - [Bemeneti adatok PHP-ban - háttérszín feladat](https://web.microsoftstream.com/video/0f6badbb-fbf3-4cd4-8b4b-07dfd40edf25)
    - [Űrlapfeldolgozás - elsőfokú egyenlet](https://ikelte-my.sharepoint.com/:v:/g/personal/gyozke_inf_elte_hu/ES4G5QWVtT9am_DOJJO5tssBClbVFVdOcXwWig2KLxHTDw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=Ymntqe)
    - [Adattárolás segédosztályokkal](https://web.microsoftstream.com/video/45a52674-05d3-4f10-9cd7-802413d17895)
    - [Mozifilmek - létrehozás, listázás, módosítás, törlés](https://web.microsoftstream.com/video/28786bb0-8998-4051-8c4a-7956bcc75343)
    - [Mozifilmek - kiegészítés](https://ikelte-my.sharepoint.com/:v:/g/personal/gyozke_inf_elte_hu/EdSP5VoNKv9QYo2mw2dZjnkBdLT4HmH_nnGR0rBDyZWmBw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=TRaSJK)
    - [Háttérszín tárolása munkamenetben](https://ikelte-my.sharepoint.com/:v:/g/personal/gyozke_inf_elte_hu/EYxdtpG6GsVfDeeGjq9sWhUBuRCpOeqbbkasYjLJKk5_Xg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=HiXt7j)
