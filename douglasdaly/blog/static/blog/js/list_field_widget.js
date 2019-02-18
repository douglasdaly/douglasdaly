function lfwTextHelper(fieldName) {
    var listObj = document.getElementById("id_" + fieldName + "_list");

    var newText = "";
    for(var i=0; i<listObj.options.length; i++)
    {
        if(i > 0) {
            newText += ", ";
        }
        newText += listObj.options[i].text;
    }

    var textObj = document.getElementById("id_" + fieldName);
    textObj.value = newText;
}

function lfwAddValue(fieldName, tags) {
    if(tags == undefined) {
        tags = {};
    }

    var listObj = document.getElementById("id_" + fieldName + "_list");
    var addObj = document.getElementById("id_" + fieldName + "_add");

    var value = addObj.value;
    var newItem = document.createElement("option");
    newItem.text = value;
    for(var key in tags) {
        newItem.setAttribute(key, tags[key]);
    }

    listObj.add(newItem);
    addObj.value = "";

    lfwTextHelper(fieldName);
}

function lfwPickTextColorBasedOnBgColorSimple(bgColor) {
    var color = (bgColor.charAt(0) === '#') ? bgColor.substring(1, 7) : bgColor;
    var r = parseInt(color.substring(0, 2), 16); // hexToR
    var g = parseInt(color.substring(2, 4), 16); // hexToG
    var b = parseInt(color.substring(4, 6), 16); // hexToB
    return (((r * 0.299) + (g * 0.587) + (b * 0.114)) > 186) ? "#000000" : "#FFFFFF";
}

function lfwAddColorValue(fieldName, tags) {
    if(tags == undefined) {
        tags = {};
    }

    var value = document.getElementById("id_" + fieldName + "_add").value;
    tags["style"] = "background-color: " + value + "; color: " + lfwPickTextColorBasedOnBgColorSimple(value) + ";";

    lfwAddValue(fieldName, tags);
}

function lfwRemoveValue(fieldName) {
    var listObj = document.getElementById("id_" + fieldName + "_list");

    selectedArray = [];
    for(var i=0; i<listObj.options.length; i++) {
        selectedArray[i] = listObj.options[i].selected;
    }

    i = selectedArray.length;
    while(i--)
    {
        if(selectedArray[i])
        {
            listObj.remove(i);
        }
    }

    lfwTextHelper(fieldName);
}
