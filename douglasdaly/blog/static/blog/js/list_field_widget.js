function arsTextHelper(fieldName) {
    var listObj = document.getElementById("id_" + fieldName + "_list");

    var newText = "";
    for(i=0; i<listObj.options.length; i++)
    {
        if(i > 0) {
            newText += ", ";
        }
        newText += listObj.options[i].text;
    }

    var textObj = document.getElementById("id_" + fieldName);
    textObj.value = newText;
}

function arsAddValue(fieldName, tags) {
    if(tags == undefined) {
        tags = {};
    }

    var listObj = document.getElementById("id_" + fieldName + "_list");

    var value = document.getElementById("id_" + fieldName + "_add").value;
    var newItem = document.createElement("option");
    newItem.text = value;
    for(var key in tags) {
        newItem.setAttribute(key, tags[key]);
    }

    listObj.add(newItem);

    arsTextHelper(fieldName);
}

function pickTextColorBasedOnBgColorSimple(bgColor) {
    var color = (bgColor.charAt(0) === '#') ? bgColor.substring(1, 7) : bgColor;
    var r = parseInt(color.substring(0, 2), 16); // hexToR
    var g = parseInt(color.substring(2, 4), 16); // hexToG
    var b = parseInt(color.substring(4, 6), 16); // hexToB
    return (((r * 0.299) + (g * 0.587) + (b * 0.114)) > 186) ? "#000000" : "#FFFFFF";
}

function arsAddColorValue(fieldName, tags) {
    if(tags == undefined) {
        tags = {};
    }

    var value = document.getElementById("id_" + fieldName + "_add").value;
    tags["style"] = "background-color: " + value + "; color: " + pickTextColorBasedOnBgColorSimple(value) + ";";
    arsAddValue(fieldName, tags);
}

function arsRemoveValue(fieldName) {
    var listObj = document.getElementById("id_" + fieldName + "_list");
    listObj.remove(listObj.selectedIndex);

    arsTextHelper(fieldName);
}
