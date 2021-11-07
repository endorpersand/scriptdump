var owls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40].reverse();
var hours = 0;
var iterate = choice => {
    if (choice) { // trigger choice
        owls.push(0);
    } else {
        for (var i = 0; i < 5; i++) owls.splice(Math.floor(Math.random() * owls.length), 1);
    }
    owls = owls.filter(x => x < 100); // agitated owls leave
    owls = owls.map(x => x + Math.floor(owls.length ** .5)); // add agitation
    if (owls.length == 0) return false; // check if mailbox is empty

    console.log(owls, ++hours);
}
var reset = () => {
    owls = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40].reverse();
    hours = 0;
}

var trashInDanger = (multiplier) => {
    if (owls.length <= 5) return true;
    var filter = owls.filter(x => x + multiplier * Math.floor(owls.length ** .5) > 100);
    if (filter.length > 0) return false;
    return true;
}

reset();
for (var i = 0; i < 1000; i++) {
    if (iterate(trashInDanger(2)) === false) break;
}