var fs = require('fs');
var Jimp = require("jimp");
var config = require('./config');

var imagesCount = 0;
var processedImages = 0;

console.log(config.imagesFile);

fs.readFile(config.imagesFile, 'utf8', function (err, data) {
    if (err) throw err;
    var imageDefs = JSON.parse(data);
    imagesCount = imageDefs.length;

    imageDefs.forEach(imageDef => {
        console.log('start processing image ' + imageDef.fileName);
        Jimp.read(config.filePrefix + imageDef.fileName + ".png", function (err, img) {
            if (err) throw err;
            // console.log(img);

            // identify lines
            var verticalLines = identifyLines(img, false)
            var horizontalLines = identifyLines(img, true)
            // console.log("horizontal --");
            // console.log(horizontalLines);
            // console.log("vertical ||");
            // console.log(verticalLines);

            // add red lines
            var imgRed = img.clone();
            imgRed = addRedLinesToImage(imgRed, horizontalLines, true);
            imgRed = addRedLinesToImage(imgRed, verticalLines, false);
            imgRed.write(imageDef.fileName + "_red.png");

            // generate composition
            addIcon2Image(imageDef, img, 0, verticalLines, horizontalLines);
        });
    });
});

function addIcon2Image(imageDef, img, iconIndex, verticalLines, horizontalLines) {
    if (iconIndex == imageDef.icons.length) {
        // vsetky pridane, uloz obrazok
        img.write(config.filePrefix + imageDef.fileName + "_i.png", function (err, img) {
            console.log((++processedImages) + '/' + imagesCount + "  DONE image " + imageDef.fileName);
            if (processedImages == imagesCount) {
                console.log("ALL IMAGES PROCESSED, DONE")
            }
        });
        return;
    };

    const iconDef = imageDef.icons[iconIndex];
    var x = 0;
    if (iconDef.coefx) {
        x = Math.floor((1 - iconDef.coefx) * verticalLines[iconDef.x1] + iconDef.coefx * verticalLines[iconDef.x2] - 0.5 * iconDef.size);
    } else {
        x = Math.floor(0.5 * verticalLines[iconDef.x1] + 0.5 * verticalLines[iconDef.x2] - 0.5 * iconDef.size);
    }
    var y = 0;
    if (iconDef.coefy) {
        y = Math.floor((1 - iconDef.coefy) * horizontalLines[iconDef.y1] + iconDef.coefy * horizontalLines[iconDef.y2] - 0.5 * iconDef.size);
    } else {
        y = Math.floor(0.5 * horizontalLines[iconDef.y1] + 0.5 * horizontalLines[iconDef.y2] - 0.5 * iconDef.size);
    }

    // read icon file
    Jimp.read(config.iconPrefix + iconDef.iconName, function (err, iconImage) {
        if (err) {
            console.log(err);
            throw err;
        }
        // console.log('read icon image : ' + iconPrefix + iconDef.iconName);

        // resize icon to defined size
        iconImage.resize(iconDef.size, Jimp.AUTO, function (err, iconImage) {
            if (err) {
                console.log(err);
                throw err;
            }
            // console.log('resized icon image : ' + iconPrefix + iconDef.iconName);

            // add to image
            img.composite(iconImage, x, y, function (err, newimage) {
                // pridaj dalsiu ikonu
                addIcon2Image(imageDef, newimage, ++iconIndex, verticalLines, horizontalLines);
            });
        });
    });
}

function identifyLines(img, horizontal) {
    var lines = [];

    var dim1 = 0;
    var dim2 = 0;
    if (horizontal) {
        dim1 = img.bitmap.height;
        dim2 = img.bitmap.width;
    } else {
        dim1 = img.bitmap.width;
        dim2 = img.bitmap.height;
    }

    for (let i1 = 0; i1 < dim1; i1++) {
        var i2 = 0;
        while (i2 < dim2) {
            // najdi bielu ciaru
            while ((i2 < dim2) && !testBlack(i1, i2, horizontal, img)) {
                i2++;
            }
            var istart = i2;
            // najdi ciernu ciaru
            while ((i2 < dim2) && testBlack(i1, i2, horizontal, img)) {
                i2++;
            }
            if ((i2 - istart) > config.treshold) {
                // dostatocne dlha cierna ciara
                lines.push(i1);
                // hrubka ciary, toto by bolo to iste
                i1 += config.delta;
                // uz som ciaru nasiel, viac ma to nezaujima
                i2 = dim2;
            }
        }
    }

    return lines;
}

function addRedLinesToImage(img, lines, horizontal) {
    const redColor = Jimp.rgbaToInt(255, 0, 0, 255);
    lines.forEach(i => {
        if (horizontal) {
        for (let idelta = 0; idelta < img.bitmap.width; idelta++) {
                img.setPixelColor(redColor, idelta, i);
            }
        } else {
            for (let idelta = 0; idelta < img.bitmap.height; idelta++) {
                img.setPixelColor(redColor, i, idelta);
            }
        }
    });

    return img;
}

function testBlackXY(x, y, img) {
    var c = Jimp.intToRGBA(img.getPixelColor(x, y));
    return (c.r == 0 && c.g == 0 && c.b == 0 && c.a == 255);
}

function testBlack(i1, i2, horizontal, img) {
    if (horizontal) {
        return testBlackXY(i2, i1, img);
    } else {
        return testBlackXY(i1, i2, img);
    }
}

