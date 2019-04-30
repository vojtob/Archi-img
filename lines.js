var fs = require('fs');
var Jimp = require("jimp");
var projectDir = process.argv[2];
var exportDir = projectDir;
if (process.argv.length > 3) exportDir = process.argv[3];
var config = require(projectDir + '/Architecture_src/model/config');
var resolution = require("screen-resolution");

var imagesCount = 0;
var processedImages = 0;

// setup resolution, line width, scale, ... 
// calibration based on standard image Calibration.png
Jimp.read(projectDir + '/Architecture_temp/exported/Calibration.png', function (err, img) {
    if (err) throw err;

    // temporary config for calibration
    console.log('Calibration (setup scale). Calibration image size: ' + img.bitmap.width + " x " + img.bitmap.height);
    config.minLength = img.bitmap.height / 3;
    config.delta = img.bitmap.height / 5;
    // console.log(config);
    
    var imgGray = img.clone();
    imgGray = imgGray.grayscale();
    var verticalLines = identifyLines(imgGray, false);
    var horizontalLines = identifyLines(imgGray, true);
    var rectangles = identifyRectangles(horizontalLines, verticalLines);
    if(rectangles.length != 1) {
        console.log("Not calibrated, rectangles size: " + rectangles.length);
    } else {
        // konstanty odvodim od vysky standardneho elementu
        var h = rectangles[0][3]-rectangles[0][1];
        config.minLength = Math.floor(h/2);
        config.delta = Math.floor(h/3);
        // velkost ikony nastavim tak, aby 64 zodpovedalo stvrtine vysky standardneho elementu
        config.iconSize = h;
        config.offset = Math.floor(h/10);
        console.log("Calibrated");
        console.log(config);
        // process other images
        readFiles();
    }
});

function readFiles() {
    console.log("Processing images from: " + config.imagesFile);
    
    fs.readFile(projectDir + '/Architecture_src/model/' + config.imagesFile, 'utf8', function (err, data) {
        if (err) throw err;
        var imageDefs = JSON.parse(data);
        imagesCount = imageDefs.length;
        
        imageDefs.forEach(imageDef => {
            console.log('start processing image ' + imageDef.fileName);
            Jimp.read(projectDir + '/Architecture_temp/exported/' + imageDef.fileName + ".png", function (err, img) {
                if (err) throw err;
                // console.log(img);
                
                processImage(imageDef, img);
            });
        });
    });
}

function processImage(imageDef, img) {
    console.log("Analyze image " + imageDef.fileName);
    if(imageDef.icons.length > 0) {
        // identify lines and rectangles
        var imgGray = img.clone();
        imgGray = imgGray.grayscale();
        var verticalLines = identifyLines(imgGray, false);
        // console.log(verticalLines);
        var horizontalLines = identifyLines(imgGray, true);
        // console.log(horizontalLines);
        var rectangles = identifyRectangles(horizontalLines, verticalLines);
        // console.log(rectangles);

        // produce helper files
        addGrayLinesToImage(img, imageDef, horizontalLines, verticalLines);
        addGreenRectangles(img, imageDef, rectangles);
    }

    // generate composition
    console.log("Add icons to image " + imageDef.fileName);
    if(config.addIcons) {
        addIcon2Image(img, imageDef, 0, verticalLines, horizontalLines, rectangles);
    } else {
	}
}

function addIcon2Image(img, imageDef, iconIndex, verticalLines, horizontalLines, rectangles) {
    if (iconIndex == imageDef.icons.length) {
        // vsetky pridane, uloz obrazok
        img.write(exportDir + '/Architecture/' + imageDef.fileName + ".png", function (err, img) {
            if(err) {
                console.log("Problem with image " + imageDef.fileName);
                console.log(err);
            }
            console.log((++processedImages) + '/' + imagesCount + "  DONE image " + exportDir + '/Architecture/' + imageDef.fileName);
            if (processedImages == imagesCount) {
                console.log("ALL IMAGES PROCESSED, DONE")
            }
        });
        return;
    }


    var iconDef = imageDef.icons[iconIndex];
    // read icon file
    Jimp.read(projectDir + '/resources/icons/' + iconDef.iconName, function (err, iconImage) {
        if (err) {
            console.log(err);
            throw err;
        }
        // console.log('read icon image : ' x+ iconDef.iconName);
        // console.log(iconImage);
        // console.log("orig icon size: " + iconImage.bitmap.width + " x " + iconImage.bitmap.height);

        // resize icon to defined size
        iconImage.resize(h = Math.floor(iconDef.size*config.iconSize/64), Jimp.AUTO, function (err, iconImage) {
            if (err) {
                console.log(err);
                throw err;
            }
            // console.log("resized icon size: " + iconImage.bitmap.width + " x " + iconImage.bitmap.height);

            // set coordinates
            var x = 0;
            var y = 0;
        
            try{
                // defined by rectangle
                var rec = rectangles[iconDef.rec - 1];
                if (iconDef.x == "left") {
                    x = rec[0] + config.offset;
                } else if (iconDef.x == "right") {
                    x = rec[2] - config.offset - iconImage.bitmap.width;
                } else if (iconDef.x == "center") {
                    x = (rec[2] + rec[0] - iconImage.bitmap.width) / 2;
                } else {
                    x = Math.floor((1 - iconDef.x) * rec[0] + iconDef.x * rec[2] - 0.5 * iconImage.bitmap.width);
                }
                if (iconDef.y == "top") {
                    y = rec[1] + config.offset;
                } else if (iconDef.y == "bottom") {
                    y = rec[3] - config.offset - iconImage.bitmap.height;
                } else if (iconDef.y == "center") {
                    y = (rec[3] + rec[1] - iconImage.bitmap.height) / 2;
                } else {
                    y = Math.floor((1 - iconDef.y) * rec[1] + iconDef.y * rec[3] - 0.5 * iconImage.bitmap.height);
                }
            } catch (ex) {
                console.log("!!!! Problem processing file: " + imageDef.fileName + "  icon: " + iconDef.iconName);
                console.log(ex);
                throw ex;
            }      

            // add to image
            img.composite(iconImage, x, y, function (err, newimage) {
                // pridaj dalsiu ikonu
                addIcon2Image(newimage, imageDef, ++iconIndex, verticalLines, horizontalLines, rectangles);
            });
        });
    });

}

function identifyLines(img, horizontal) {
    // var lines = [];
    var segments = [];

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
            // preskoc medzeru
            while ((i2 < dim2) && !isLine(i1, i2, horizontal, img)) {
                i2++;
            }
            var istart = i2;
            var density = 0;
            // nasleduj ciaru
            while ((i2 < dim2) && isLine(i1, i2, horizontal, img)) {
                i2++;
            }
            // console.log("min length: " + config.minLength);
            if ((i2 - istart) > config.minLength) {
                // dostatocne dlha ciara
                // hrubka ciary, toto by bolo to iste
                // i1 += config.delta;
                // uz som ciaru nasiel, viac ma to nezaujima
                if (horizontal) {
                    segments.push([istart, i1, i2, i1]);
                } else {
                    segments.push([i1, istart, i1, i2]);
                    // i2 = dim2;
                }
            }
        }
    }

    return segments;
}

function identifyRectangles(hLines, vLines) {
    // console.log('hlines', hLines);
    // console.log('vlines', vLines);
    var rectangles = [];
    for (let hli1 = 0; hli1 < hLines.length; hli1++) {
        const hl1 = hLines[hli1];
        for (let hli2 = hli1 + 1; hli2 < hLines.length; hli2++) {
            const hl2 = hLines[hli2];
            if ((Math.abs(hl1[0] - hl2[0]) < config.delta) && 
                (Math.abs(hl1[2] - hl2[2]) < config.delta) && 
                (Math.abs(hl1[1] - hl2[1]) > config.minLength)) {
                // tieto horizontalne usecky su nad sebou, ale nie su prilis blizko seba
                var x1 = (hl1[0] + hl2[0]) / 2;
                var y1 = hl1[1];
                var x2 = (hl1[2] + hl2[2]) / 2;
                var y2 = hl2[1];

                // najdi lavu hranu
                var vli = 0;
                while (vli < vLines.length) {
                    var vll = vLines[vli];
                    if(vll[0] < (x1 - config.delta)) {
                        // tato ciara je prilis vlavo, hladam dalej
                        vli += 1;
                        continue;
                    }
                    if(vll[0] > (x1 + config.delta)) {
                        // tato ciara je prilis vpravo, uz nic nenajdem
                        break;
                    }
                    if(Math.abs(y1 - vll[1]) > config.delta) {
                        // tato ciare zacina v inej vyske, hladam dalej
                        vli += 1;
                        continue;
                    }
                    if(Math.abs(y2 - vll[3]) > config.delta) {
                        // tato ciare konci v inej vyske, hladam dalej
                        vli += 1;
                        continue;
                    }
                    // tato ciara je fajn lava hrana
                    vli += 1;

                    // idem hladat pravu hranu
                    vlir = vli;
                    while (vlir < vLines.length) {
                        vlr = vLines[vlir];
                        if(vlr[0] < (x2 - config.delta)) {
                            // tato ciara je prilis vlavo, hladam dalej
                            vlir += 1;
                            continue;
                        }
                        if(vlr[0] > (x2 + config.delta)) {
                            // tato ciara je prilis vpravo, uz nic nenajdem
                            break;
                        }
                        if(Math.abs(y1 - vlr[1]) > config.delta) {
                            // tato ciare zacina v inej vyske, hladam dalej
                            vlir += 1;
                            continue;
                        }
                        if(Math.abs(y2 - vlr[3]) > config.delta) {
                            // tato ciare konci v inej vyske, hladam dalej
                            vlir += 1;
                            continue;
                        }
                        // tato ciara je fajn prava hrana

                        // este overim, ci ide o obdlznik s oblymi rohami alebo hranaty, ci to nie je nejaky fault
                        sx1 = Math.min(x1, vll[0]);
                        sx2 = Math.max(x2, vlr[2]);
                        if( ((hl1[0]-sx1) > (config.delta/3)) &&
                            ((sx2-hl1[2]) > (config.delta/3)) &&
                            ((vll[1]-y1) > (config.delta/3)) &&
                            ((y2-vll[3]) > (config.delta/3))) {
                                // mam round rectangle
                                // console.log("round rect " + rectangles.length);
                                rectangles.push([sx1, y1, sx2, y2]);
                                hli2 = hLines.length;
                                vli = vLines.length;
                                break;
                        } else if( (Math.abs(hl1[0]-sx1) < (config.delta/6)) &&
                                    (Math.abs(sx2-hl1[2]) < (config.delta/6)) &&
                                    (Math.abs(vll[1]-y1) < (config.delta/6)) &&
                                    (Math.abs(y2-vll[3]) < (config.delta/6))) {
                                // mam normal rectangle
                                // console.log("normal rect " + rectangles.length);
                                // if(rectangles.length == 7) {
                                //     console.log([x1, y1, x2, y2]);
                                //     console.log(hl1);
                                //     console.log(vll);
                                // }
                                rectangles.push([sx1, y1, sx2, y2]);
                                hli2 = hLines.length;
                                vli = vLines.length;
                                break;
                        } else {
                            // nie je obdlznik
                            vlir += 1;
                        }
                    }
                }
            }
        }
    }
    return rectangles;
}

function addGrayLinesToImage(img, imageDef, horizontalLines, verticalLines) {
    var imgLines = img.clone();
    // const grayColor = Jimp.rgbaToInt(50, 50, 50, 255);
    const grayColor = Jimp.rgbaToInt(255, 0, 0, 255);

    horizontalLines.forEach(line => {
        for (let idelta = line[0]; idelta < line[2]; idelta += 1) {
            imgLines.setPixelColor(grayColor, idelta, line[1]);
        }
    });
    verticalLines.forEach(line => {
        for (let idelta = line[1]; idelta < line[3]; idelta += 1) {
            imgLines.setPixelColor(grayColor, line[0], idelta);
        }
    });

    imgLines.write(projectDir + '/Architecture_temp/lines/' + imageDef.fileName + "_lines.png");
}

function addGreenRectangles(img, imageDef, rectangles) {
    var imgRec = img.clone();
    // console.log("rec for " + imageDef.fileName);
    // console.log(rectangles);
    // imgRec = addRedSegmentsToImage(imgRec, horizontalLines);
    // imgRec = addRedSegmentsToImage(imgRec, verticalLines);

    const greenColor = Jimp.rgbaToInt(0, 255, 0, 255);
    var recCounter = 1;

    Jimp.loadFont(Jimp.FONT_SANS_16_BLACK).then(function (font) {
        rectangles.forEach(rectangle => {
            for (let x = rectangle[0]; x < rectangle[2]; x++) {
                imgRec.setPixelColor(greenColor, x, rectangle[1]);
                imgRec.setPixelColor(greenColor, x, rectangle[3]);

            }
            for (let y = rectangle[1]; y < rectangle[3]; y++) {
                imgRec.setPixelColor(greenColor, rectangle[0], y);
                imgRec.setPixelColor(greenColor, rectangle[2], y);
            }
            imgRec.print(font, rectangle[0] + config.offset, rectangle[1] + config.offset, recCounter.toString());
            // console.log("green rectangle " + recCounter.toString());
            recCounter++;
        });
        imgRec.write(projectDir + '/Architecture_temp/lines/' + imageDef.fileName + "_rec.png");
    });
}

// overi, ci je tu tmavy bod
function testLineXY(x, y, img) {
    var c = Jimp.intToRGBA(img.getPixelColor(x, y));
    var intensity = c.r * c.r + c.g * c.g + c.b * c.b;
    return ((c.a == 255) && (intensity < 50000));
    // return ((c.r == 0 && c.g == 0 && c.b == 0 && c.a == 255) || (c.r == 102 && c.g == 102 && c.b == 102 && c.a == 255));
}

// odpovie, ci je na tomto bode ciara
function isLine(i1, i2, horizontal, img) {
    if (horizontal) {
        return testLineXY(i2, i1, img);
    } else {
        return testLineXY(i1, i2, img);
    }
}

