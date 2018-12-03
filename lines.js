var fs = require('fs');
var Jimp = require("jimp");
var projectDir = process.argv[2];
var exportDir = projectDir;
if (process.argv.length > 3) exportDir = process.argv[3];
var config = require(projectDir + '/Architecture_src/model/config');
// var config = require('config/config');

var imagesCount = 0;
var processedImages = 0;

console.log(config.imagesFile);

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

function processImage(imageDef, img) {
    // identify lines and rectangles
    var imgGray = img.clone();
    imgGray = imgGray.grayscale();
    var verticalLines = identifyLines(imgGray, false);
    var horizontalLines = identifyLines(imgGray, true);
    var rectangles = identifyRectangles(horizontalLines, verticalLines);

    // produce helper files
    addGrayLinesToImage(img, imageDef, horizontalLines, verticalLines);
    addGreenRectangles(img, imageDef, rectangles);

    // generate composition
    addIcon2Image(img, imageDef, 0, verticalLines, horizontalLines, rectangles);
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
    };

    const iconDef = imageDef.icons[iconIndex];
    // set coordinates
    var x = 0;
    var y = 0;

	try{
		if (iconDef.rec) {
			// defined by rectangle
			var rec = rectangles[iconDef.rec - 1];
			if (iconDef.x == "left") {
				x = rec[0] + config.offset;
			} else if (iconDef.x == "right") {
				x = rec[2] - config.offset - iconDef.size;
			} else if (iconDef.x == "center") {
				x = (rec[2] + rec[0] - iconDef.size) / 2;
			} else {
				x = Math.floor((1 - iconDef.x) * rec[0] + iconDef.x * rec[2] - 0.5 * iconDef.size);
			}
			if (iconDef.y == "top") {
				y = rec[1] + config.offset;
			} else if (iconDef.y == "bottom") {
				y = rec[3] - config.offset - iconDef.size;
			} else if (iconDef.y == "center") {
				y = (rec[3] + rec[1] - iconDef.size) / 2;
			} else {
				y = Math.floor((1 - iconDef.y) * rec[1] + iconDef.y * rec[3] - 0.5 * iconDef.size);
			}
		} else {
			// defined by lines
			if (iconDef.coefx) {
				x = Math.floor((1 - iconDef.coefx) * verticalLines[iconDef.x1] + iconDef.coefx * verticalLines[iconDef.x2] - 0.5 * iconDef.size);
			} else {
				x = Math.floor(0.5 * verticalLines[iconDef.x1] + 0.5 * verticalLines[iconDef.x2] - 0.5 * iconDef.size);
			}
			if (iconDef.coefy) {
				y = Math.floor((1 - iconDef.coefy) * horizontalLines[iconDef.y1] + iconDef.coefy * horizontalLines[iconDef.y2] - 0.5 * iconDef.size);
			} else {
				y = Math.floor(0.5 * horizontalLines[iconDef.y1] + 0.5 * horizontalLines[iconDef.y2] - 0.5 * iconDef.size);
			}
		}		
	} catch (ex) {
		console.log("!!!! Problem processing file: " + imageDef.fileName + "  icon: " + iconDef.iconName);
		console.log(ex);
		throw ex;
	}

    // read icon file
    Jimp.read(projectDir + '/resources/icons/' + iconDef.iconName, function (err, iconImage) {
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
                addIcon2Image(newimage, imageDef, ++iconIndex, verticalLines, horizontalLines, rectangles);
            });
        });
    });
}

function identifyLines(img, horizontal) {
    var lines = [];
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
            if ((i2 - istart) > config.minLength) {
                // dostatocne dlha ciara
                lines.push(i1);
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

    // return lines;
    return segments;
}

function identifyRectangles(hLines, vLines) {
    var rectangles = [];
    for (let hli1 = 0; hli1 < hLines.length; hli1++) {
        const hl1 = hLines[hli1];
        for (let hli2 = hli1 + 1; hli2 < hLines.length; hli2++) {
            const hl2 = hLines[hli2];
            if ((Math.abs(hl1[0] - hl2[0]) < config.squareDelta) && (Math.abs(hl1[2] - hl2[2]) < config.squareDelta)) {
                // tieto horizontalne usecky su nad sebou
                var x1 = (hl1[0] + hl2[0]) / 2;
                var y1 = hl1[1];
                var x2 = (hl1[2] + hl2[2]) / 2;
                var y2 = hl2[1];

                var bocneHrany = 0;

                // najdi lavu hranu
                var vli = 0;
                while ((vli < vLines.length) && (vLines[vli][0] < (x1 - config.squareDelta))) {
                    vli++;
                }
                while ((vli < vLines.length) && (vLines[vli][0] < (x1 + config.squareDelta))) {
                    if ((Math.abs(y1 - vLines[vli][1]) < config.squareDelta) &&
                        (Math.abs(y2 - vLines[vli][3]) < config.squareDelta)) {
                        // nasiel som bocnu hranu 
                        bocneHrany++;
                        x1 = Math.min(x1, vLines[vli][0]);
                        break;
                    } else {
                        vli++;
                    }
                }
                if (bocneHrany < 1) {
                    // nie je hrana  
                    continue;
                }
                while ((vli < vLines.length) && (vLines[vli][2] < (x2 - config.squareDelta))) {
                    vli++;
                }
                while ((vli < vLines.length) && (vLines[vli][2] < (x2 + config.squareDelta))) {
                    if ((Math.abs(y1 - vLines[vli][1]) < config.squareDelta) &&
                        (Math.abs(y2 - vLines[vli][3]) < config.squareDelta)) {
                        // nasiel som bocnu hranu 
                        bocneHrany++;
                        x2 = Math.max(x2, vLines[vli][2]);
                        break;
                    } else {
                        vli++;
                    }
                }
                if (bocneHrany >= 2) {
                    // mam obdlznik
                    rectangles.push([x1, y1, x2, y2]);
                    break;
                }
            }
        }
    }
    return rectangles;
}

function addGrayLinesToImage(img, imageDef, horizontalLines, verticalLines) {
    var imgLines = img.clone();
    const grayColor = Jimp.rgbaToInt(50, 50, 50, 255);

    horizontalLines.forEach(line => {
        for (let idelta = 0; idelta < img.bitmap.width; idelta += 2) {
            imgLines.setPixelColor(grayColor, idelta, line[1]);
        }
    });
    verticalLines.forEach(line => {
        for (let idelta = 0; idelta < img.bitmap.height; idelta += 2) {
            imgLines.setPixelColor(grayColor, line[0], idelta);
        }
    });

    imgLines.write(projectDir + '/Architecture_temp/lines/' + imageDef.fileName + "_lines.png");
}

// function addRedSegmentsToImage(img, segments) {
//     const redColor = Jimp.rgbaToInt(255, 0, 0, 255);
//     segments.forEach(segment => {
//         if (segment[1] == segment[3]) {
//             for (let x = segment[0]; x < segment[2]; x++) {
//                 img.setPixelColor(redColor, x, segment[1]);
//             }
//         } else {
//             for (let y = segment[1]; y < segment[3]; y++) {
//                 img.setPixelColor(redColor, segment[0], y);
//             }
//         }
//     });

//     return img;
// }

function addGreenRectangles(img, imageDef, rectangles) {
    var imgRec = img.clone();
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
            recCounter++;
        });
        imgRec.write(projectDir + '/Architecture_temp/lines/' + imageDef.fileName + "_rec.png");
    });
}

function testLineXY(x, y, img) {
    var c = Jimp.intToRGBA(img.getPixelColor(x, y));
    var intensity = c.r * c.r + c.g * c.g + c.b * c.b;
    return ((c.a == 255) && (intensity < 50000));
    // return ((c.r == 0 && c.g == 0 && c.b == 0 && c.a == 255) || (c.r == 102 && c.g == 102 && c.b == 102 && c.a == 255));
}

function isLine(i1, i2, horizontal, img) {
    if (horizontal) {
        return testLineXY(i2, i1, img);
    } else {
        return testLineXY(i1, i2, img);
    }
}

