/**
 * Created by rasmusmunk on 27/09/2017.
 */
/*jshint esversion: 6 */
"use strict";

function removeChildren(obj) {
    while (obj.firstChild) {
        obj.removeChild(obj.firstChild);
    }
}

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

function setupThumbnailHoverEffect(thumbnail, static_color, hover_color) {
    thumbnail.onmouseover = function () {
        this.style.borderColor = hover_color;
        this.style.borderWidth = "6px";
    };
    thumbnail.onmouseout = function () {
        this.style.borderColor = static_color;
        this.style.borderWidth = "2px";
    };

    thumbnail.onclick = function () {
        this.style.borderColor = static_color;
        this.style.borderWidth = "2px";
    };
}

function setupOverview(static_color, hover_color) {
    let thumbnails = document.getElementsByClassName('thumbnail');
    for (let thumbnail in thumbnails) {
        if (thumbnails.hasOwnProperty(thumbnail)) {
            setupThumbnailHoverEffect(thumbnails[thumbnail], static_color, hover_color);
        }
    }
}

function errorRender(error) {
    let flashes = document.getElementById('flashes');
    removeChildren(flashes);
    let json_response = error.responseJSON.data;
    for (let key in json_response) {
        if (json_response.hasOwnProperty(key)) {
            let messageContainer = document.createElement('div');
            messageContainer.setAttribute('class', "alert alert-" + key);
            messageContainer.setAttribute('role', 'alert');
            messageContainer.innerText = json_response[key];
            flashes.append(messageContainer);
        }
    }
}


function setupTagSearch(createTileCallback, static_color, hover_color) {
    let typingTimer;                //timer identifier
    let doneTypingInterval = 500;  //time in ms, 2 seconds
    let $input = $('#tag');
    let form = $('#form-search');

    //disable enter submit
    form.on('submit', function () {
        return false;
    });

    //on keyup, start the countdown
    $input.on('keyup', function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(tagReady, doneTypingInterval);
    });

    //on keydown, clear the countdown
    $input.on('keydown', function () {
        clearTimeout(typingTimer);
    });

    function tagReady() {
        $('.loading-spinner').show();
        let _data = {
            'tag': $input.val(),
            'csrf_token': $('#csrf_token').val()
        };
        $.ajax({
            url: '/search',
            data: _data,
            type: 'POST',
            success: function (response) {
                let gridItems = document.getElementById('grid-items');
                removeChildren(gridItems);
                for (let results in response) {
                    if (response.hasOwnProperty(results)) {
                        for (let result in response[results]) {
                            if (response[results].hasOwnProperty(result)) {
                                let tile = createTileCallback(response[results][result]);
                                // Access thumbnail child element -> attach hover effect
                                setupThumbnailHoverEffect(tile.getElementsByClassName('thumbnail')[0], static_color, hover_color);
                                gridItems.appendChild(tile);
                            }
                        }
                    }
                }
                $('.loading-spinner').hide();
            },
            error: function (error) {
                $('.loading-spinner').hide();
                errorRender(error);
            }
        });
    }
}

function createGridTile(obj) {
    var newHeader = document.createElement('h3');
    newHeader.className = "card-title";
    newHeader.innerText = obj.name;

    var newBody = document.createElement('p');
    newBody.className = "card-text";
    newBody.innerText = obj.description;

    var newCaption = document.createElement('div');
    newCaption.className = "caption";
    newCaption.appendChild(newHeader);
    newCaption.appendChild(newBody);

    var newImage = document.createElement('img');
    newImage.src = "/images/" + obj.image;
    newImage.alt = "Project";

    var newThumb = document.createElement('div');
    newThumb.className = "thumbnail mb-4";
    newThumb.appendChild(newImage);
    newThumb.appendChild(newCaption);

    var newLink = document.createElement('a');
    newLink.className = "d-block mb-4";
    newLink.href = "/show/" + obj._id;
    newLink.appendChild(newThumb);

    var newDiv = document.createElement('div');
    newDiv.className = "col-sm-6 col-md-4 col-lg-3";
    newDiv.appendChild(newLink);
    return newDiv;
}


function populateGrid(objects, static_color, hover_color) {
    let gridItems = document.getElementById('grid-items');
    removeChildren(gridItems);
    for (let objs in objects) {
        if (objects.hasOwnProperty(objs)) {
            let obj = objects[objs];
            let tile = createGridTile(obj);
            // Access thumbnail child element -> attach hover effect
            setupThumbnailHoverEffect(tile.getElementsByClassName('thumbnail')[0], static_color, hover_color);
            gridItems.appendChild(tile);
        }
    }
}

$(document).ready(function () {
    setupOverview("#8fd182", "#46743c");
});
