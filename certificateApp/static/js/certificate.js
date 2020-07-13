// ===========================================================
function readURL(input, tg) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            tg.attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#ckt").change(function () {
    readURL(this, $('#ckt-img'));
});
$("#logo").change(function () {
    readURL(this, $('.internship-logo'));
});
$("#sign").change(function () {
    readURL(this, $('.signature-logo'));
});

function post(path, params, method = 'post', form) {

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    form.method = method;
    form.action = path;
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.style.position = 'absolute';
            hiddenField.name = key;
            hiddenField.value = params[key];

            form.appendChild(hiddenField);
        }
    }

    form.submit();
}

btn = $('#submit-btn')
btn.click(() => {
    console.log('hello')

    data = {
        logox:$('.logo-btn .x-coordinate-badge').text().trim() * 1.6,
        logoy:$('.logo-btn .y-coordinate-badge').text().trim() * 1.6,
        logol:$('#logo-img').height() * 1.6,
        logow:$('#logo-img').width() * 1.6,
        signx:$('.sign-logo-btn .x-coordinate-badge').text().trim() *1.6,
        signy:$('.sign-logo-btn .y-coordinate-badge').text().trim() *1.6,
        signl:$('#sign-img').height() *1.6,
        signw:$('#sign-img').width() *1.6,



        renox: $('.ref-no-control .x-coordinate-badge').text().trim() * 1.6,
        renoy: $('.ref-no-control .y-coordinate-badge').text().trim() * 1.6,
        renos: $('.ref-no-control .font-size-badge').text().trim() * 1.6,

        internamex: $('.name-control .x-coordinate-badge').text().trim() * 1.6,
        internamey: $('.name-control .y-coordinate-badge').text().trim() * 1.6,
        internames: $('.name-control .font-size-badge').text().trim() * 1.6,

        interntypex: $('.internship-control .x-coordinate-badge').text().trim() * 1.6,
        interntypey: $('.internship-control .y-coordinate-badge').text().trim() * 1.6,
        interntypes: $('.internship-control .font-size-badge').text().trim() * 1.6,

        d1x: $('.from-control .x-coordinate-badge').text().trim() * 1.6,
        d1y: $('.from-control .y-coordinate-badge').text().trim() * 1.6,
        d1s: $('.from-control .font-size-badge').text().trim() * 1.6,

        d2x: $('.to-control .x-coordinate-badge').text().trim() * 1.6,
        d2y: $('.to-control .y-coordinate-badge').text().trim() * 1.6,
        d2s: $('.to-control .font-size-badge').text().trim() * 1.6,

        datex: $('.date-control .x-coordinate-badge').text().trim() * 1.6,
        datey: $('.date-control .y-coordinate-badge').text().trim() * 1.6,
        dates: $('.date-control .font-size-badge').text().trim() * 1.6,

        profilex: $('.post-control .x-coordinate-badge').text().trim() * 1.6,
        profiley: $('.post-control .y-coordinate-badge').text().trim() * 1.6,
        profiles: $('.post-control .font-size-badge').text().trim() * 1.6
    }

    if ($('#exampleCheckitOut:checked').val()) {
        post('/certificate/mentor/certificateconfig',data,'POST',$('#ckt-form')[0])
    }
    else{
        alert('Check The Button')
    }

    
    // var formData = new FormData();
    // for(key in data){
    //     formData.append(key,data[key])
    // }
    // formData.append('file', $('#ckt')[0].files[0]);
    // console.log(formData)
    // $.ajax({
    //     url: '/certificate/mentor/certificateconfig',
    //     data: formData,
    //     enctype: 'multipart/form-data',
    //     type: 'POST',
    //     cache : false,
    //     processData: false,
    //     success: (data) => {
    //         console.log(data)
    //     },
    //     error: (data) => {
    //         console.log(data)
    //     }
    // })
})




// $('#form').submit(function(e){
//     e.preventDefault();
//     $form = $(this)
//     var formData = new FormData(this);
//     $.ajax({
//         url: window.location.pathname,
//         type: 'POST',
//         data: formData,
//         success: function (response) {
//             console.log(response)
//         },
//         cache: false,
//         contentType: false,
//         processData: false
//     });
// });






// ==========================================================
$('.create-ref-no').click(() => {
    const value = $('[placeholder="Ref No"]').val()
    var element = document.createElement("span")
    element.setAttribute('class', 'ref-no')
    element.innerText = value
    document.querySelector('.appender').appendChild(element)
    console.log(element)
    $('.ref-no').css({
        position: 'absolute',
        top: '100px',
        left: '600px',
        zIndex: '5',
    })

    $('.ref-no').draggable({
        drag: (event, ui) => {
            pos = ui.position
            $('.ref-no-control .y-coordinate-badge').text(pos.top)
            $('.ref-no-control .x-coordinate-badge').text(pos.left)
        }
    });

})



$('.ref-no-control .increase-size').click(() => {
    var prevFontSize = $('.ref-no').css('fontSize');
    console.log(prevFontSize)
    $('.ref-no').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) + 2) + 'px'
    })
    prevFontSize = $('.ref-no').css('fontSize');
    $('.ref-no-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})

$('.ref-no-control .decrease-size').click(() => {
    var prevFontSize = $('.ref-no').css('fontSize');
    console.log(prevFontSize)
    $('.ref-no').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) - 2) + 'px'
    })
    prevFontSize = $('.ref-no').css('fontSize');
    $('.ref-no-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})



$('.ref-no-control .up').click(() => {
    var yCoordicate = $('.ref-no').css('top');

    $('.ref-no').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.ref-no').css('top');
    $('.ref-no-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.ref-no-control .down').click(() => {
    var yCoordicate = $('.ref-no').css('top');

    $('.ref-no').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.ref-no').css('top');
    $(' .ref-no-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.ref-no-control .left').click(() => {
    var xCoordicate = $('.ref-no').css('left');

    $('.ref-no').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.ref-no').css('left');
    $('.ref-no-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.ref-no-control .right').click(() => {
    var xCoordicate = $('.ref-no').css('left');

    $('.ref-no').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.ref-no').css('left');
    $('.ref-no-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})



///// Intern Name

$('.create-intern-name').click(() => {
    const value = $('[placeholder="Intern Name"]').val()
    var element = document.createElement("span")
    element.setAttribute('class', 'intern-name')
    element.innerText = value
    document.querySelector('.appender').appendChild(element)
    console.log(element)
    $('.intern-name').css({
        position: 'absolute',
        top: '350px',
        left: '300px',
        zIndex: '5',
    })

    $('.intern-name').draggable({
        drag: (event, ui) => {
            var pos = ui.position
            $('.name-control .x-coordinate-badge').text(pos.left)
            $('.name-control .y-coordinate-badge').text(pos.top)
        }
    });
    // var yCoordicate = $('.intern-name').css('top');
    // var xCoordicate = $('.intern-name').css('left');


})
$('.name-control .increase-size').click(() => {
    var prevFontSize = $('.intern-name').css('fontSize');
    console.log(prevFontSize)
    $('.intern-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) + 2) + 'px'
    })
    prevFontSize = $('.intern-name').css('fontSize');
    $('.name-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})

$('.name-control .decrease-size').click(() => {
    var prevFontSize = $('.intern-name').css('fontSize');
    console.log(prevFontSize)
    $('.intern-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) - 2) + 'px'
    })
    prevFontSize = $('.intern-name').css('fontSize');
    $('.name-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})



$('.name-control .up').click(() => {
    var yCoordicate = $('.intern-name').css('top');

    $('.intern-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.intern-name').css('top');
    $('.name-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.name-control .down').click(() => {
    var yCoordicate = $('.intern-name').css('top');

    $('.intern-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.intern-name').css('top');
    $(' .name-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.name-control .left').click(() => {
    var xCoordicate = $('.intern-name').css('left');

    $('.intern-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.intern-name').css('left');
    $('.name-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.name-control .right').click(() => {
    var xCoordicate = $('.intern-name').css('left');

    $('.intern-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.intern-name').css('left');
    $('.name-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})



// internship name


$('.create-internship-name').click(() => {
    const value = $('[placeholder="Internship Name"]').val()
    var element = document.createElement("span")
    element.setAttribute('class', 'internship-name')
    element.innerText = value
    document.querySelector('.appender').appendChild(element)
    console.log(element)
    $('.internship-name').css({
        position: 'absolute',
        top: '350px',
        left: '350px',
        zIndex: '5',
    })
    $('.internship-name').draggable({
        drag: (event, ui) => {
            var pos = ui.position
            $('.internship-control .x-coordinate-badge').text(pos.left)
            $('.internship-control .y-coordinate-badge').text(pos.top)
        }
    });

})
$('.internship-control .increase-size').click(() => {
    var prevFontSize = $('.internship-name').css('fontSize');
    console.log(prevFontSize)
    $('.internship-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) + 2) + 'px'
    })
    prevFontSize = $('.internship-name').css('fontSize');
    $('.internship-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})

$('.internship-control .decrease-size').click(() => {
    var prevFontSize = $('.internship-name').css('fontSize');
    console.log(prevFontSize)
    $('.internship-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) - 2) + 'px'
    })
    prevFontSize = $('.internship-name').css('fontSize');
    $('.internship-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})



$('.internship-control .up').click(() => {
    var yCoordicate = $('.internship-name').css('top');

    $('.internship-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.internship-name').css('top');
    $('.internship-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.internship-control .down').click(() => {
    var yCoordicate = $('.internship-name').css('top');

    $('.internship-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.internship-name').css('top');
    $(' .internship-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.internship-control .left').click(() => {
    var xCoordicate = $('.internship-name').css('left');

    $('.internship-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.internship-name').css('left');
    $('.internship-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.internship-control .right').click(() => {
    var xCoordicate = $('.internship-name').css('left');

    $('.internship-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.internship-name').css('left');
    $('.internship-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})



//////////// from 

$('.create-from').click(() => {
    const value = $('[placeholder="Starting Date"]').val()
    var element = document.createElement("span")
    element.setAttribute('class', 'from-name')
    element.innerText = value
    document.querySelector('.appender').appendChild(element)
    console.log(element)
    $('.from-name').css({
        position: 'absolute',
        top: '390px',
        left: '350px',
        zIndex: '5',
    })

    $('.from-name').draggable({
        drag: (event, ui) => {
            var pos = ui.position
            $('.from-control .x-coordinate-badge').text(pos.left)
            $('.from-control .y-coordinate-badge').text(pos.top)
        }
    });

})
$('.from-control .increase-size').click(() => {
    var prevFontSize = $('.from-name').css('fontSize');
    console.log(prevFontSize)
    $('.from-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) + 2) + 'px'
    })
    prevFontSize = $('.from-name').css('fontSize');
    $('.from-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})

$('.from-control .decrease-size').click(() => {
    var prevFontSize = $('.from-name').css('fontSize');
    console.log(prevFontSize)
    $('.from-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) - 2) + 'px'
    })
    prevFontSize = $('.from-name').css('fontSize');
    $('.from-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})



$('.from-control .up').click(() => {
    var yCoordicate = $('.from-name').css('top');

    $('.from-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.from-name').css('top');
    $('.from-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.from-control .down').click(() => {
    var yCoordicate = $('.from-name').css('top');

    $('.from-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.from-name').css('top');
    $(' .from-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.from-control .left').click(() => {
    var xCoordicate = $('.from-name').css('left');

    $('.from-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.from-name').css('left');
    $('.from-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.from-control .right').click(() => {
    var xCoordicate = $('.from-name').css('left');

    $('.from-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.from-name').css('left');
    $('.from-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})



///to//






$('.create-to').click(() => {
    const value = $('[placeholder="Ending Date"]').val()
    var element = document.createElement("span")
    element.setAttribute('class', 'to-name')
    element.innerText = value
    document.querySelector('.appender').appendChild(element)
    console.log(element)
    $('.to-name').css({
        position: 'absolute',
        top: '390px',
        left: '450px',
        zIndex: '5',
    })

    $('.to-name').draggable({
        drag: (event, ui) => {
            var pos = ui.position
            $('.to-control .x-coordinate-badge').text(pos.left)
            $('.to-control .y-coordinate-badge').text(pos.top)
        }
    });

})
$('.to-control .increase-size').click(() => {
    var prevFontSize = $('.to-name').css('fontSize');
    console.log(prevFontSize)
    $('.to-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) + 2) + 'px'
    })
    prevFontSize = $('.to-name').css('fontSize');
    $('.to-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})

$('.to-control .decrease-size').click(() => {
    var prevFontSize = $('.to-name').css('fontSize');
    console.log(prevFontSize)
    $('.to-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) - 2) + 'px'
    })
    prevFontSize = $('.to-name').css('fontSize');
    $('.to-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})



$('.to-control .up').click(() => {
    var yCoordicate = $('.to-name').css('top');

    $('.to-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.to-name').css('top');
    $('.to-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.to-control .down').click(() => {
    var yCoordicate = $('.to-name').css('top');

    $('.to-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.to-name').css('top');
    $(' .to-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.to-control .left').click(() => {
    var xCoordicate = $('.to-name').css('left');

    $('.to-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.to-name').css('left');
    $('.to-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.to-control .right').click(() => {
    var xCoordicate = $('.to-name').css('left');

    $('.to-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.to-name').css('left');
    $('.to-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})




//// post


$('.create-post').click(() => {
    const value = $('[placeholder="Designation"]').val()
    var element = document.createElement("span")
    element.setAttribute('class', 'post-name')
    element.innerText = value
    document.querySelector('.appender').appendChild(element)
    console.log(element)
    $('.post-name').css({
        position: 'absolute',
        top: '420px',
        left: '280px',
        zIndex: '5',
    })

    $('.post-name').draggable({
        drag: (event, ui) => {
            var pos = ui.position
            $('.post-control .x-coordinate-badge').text(pos.left)
            $('.post-control .y-coordinate-badge').text(pos.top)
        }
    });
})
$('.post-control .increase-size').click(() => {
    var prevFontSize = $('.post-name').css('fontSize');
    console.log(prevFontSize)
    $('.post-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) + 2) + 'px'
    })
    prevFontSize = $('.post-name').css('fontSize');
    $('.post-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})

$('.post-control .decrease-size').click(() => {
    var prevFontSize = $('.post-name').css('fontSize');
    console.log(prevFontSize)
    $('.post-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) - 2) + 'px'
    })
    prevFontSize = $('.post-name').css('fontSize');
    $('.post-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})



$('.post-control .up').click(() => {
    var yCoordicate = $('.post-name').css('top');

    $('.post-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.post-name').css('top');
    $('.post-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.post-control .down').click(() => {
    var yCoordicate = $('.post-name').css('top');

    $('.post-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.post-name').css('top');
    $(' .post-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.post-control .left').click(() => {
    var xCoordicate = $('.post-name').css('left');

    $('.post-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.post-name').css('left');
    $('.post-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.post-control .right').click(() => {
    var xCoordicate = $('.post-name').css('left');

    $('.post-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.post-name').css('left');
    $('.post-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})





//// date




$('.create-date').click(() => {
    const value = $('[placeholder="Date"]').val()
    var element = document.createElement("span")
    element.setAttribute('class', 'date-name')
    element.innerText = value
    document.querySelector('.appender').appendChild(element)
    console.log(element)
    $('.date-name').css({
        position: 'absolute',
        top: '330px',
        left: '100px',
        zIndex: '5',
    })

    $('.date-name').draggable({
        drag: (event, ui) => {
            var pos = ui.position
            $('.date-control .x-coordinate-badge').text(pos.left)
            $('.date-control .y-coordinate-badge').text(pos.top)
        }
    });
})
$('.date-control .increase-size').click(() => {
    var prevFontSize = $('.date-name').css('fontSize');
    console.log(prevFontSize)
    $('.date-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) + 2) + 'px'
    })
    prevFontSize = $('.date-name').css('fontSize');
    $('.date-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})

$('.date-control .decrease-size').click(() => {
    var prevFontSize = $('.date-name').css('fontSize');
    console.log(prevFontSize)
    $('.date-name').css({
        fontSize: (+prevFontSize.slice(0, prevFontSize.length - 2) - 2) + 'px'
    })
    prevFontSize = $('.date-name').css('fontSize');
    $('.date-control .font-size-badge').text(+prevFontSize.slice(0, prevFontSize.length - 2))
})



$('.date-control .up').click(() => {
    var yCoordicate = $('.date-name').css('top');

    $('.date-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.date-name').css('top');
    $('.date-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.date-control .down').click(() => {
    var yCoordicate = $('.date-name').css('top');

    $('.date-name').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.date-name').css('top');
    $(' .date-control .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.date-control .left').click(() => {
    var xCoordicate = $('.date-name').css('left');

    $('.date-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.date-name').css('left');
    $('.date-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.date-control .right').click(() => {
    var xCoordicate = $('.date-name').css('left');

    $('.date-name').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.date-name').css('left');
    $('.date-control .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})




// $('.upload-logo').click(() => {
//     var element = document.createElement('img')
//     element.setAttribute('class', 'internship-logo')
//     element.setAttribute('src', 'logo.png')
//     document.querySelector('.appender').appendChild(element)
//     console.log(element)
//     $('.internship-logo').css({
//         position: 'absolute',
//         top: '520px',
//         left: '600px',
//         zIndex: '7',
//         width: '100px'
//     })
//     $('.logo-invisibles').removeClass('invisible')



// })


//////logo 




$('.internship-logo').draggable({
    drag: (event, ui) => {
        var pos = ui.position
        $('.logo-btn .x-coordinate-badge').text(pos.left)
        $('.logo-btn .y-coordinate-badge').text(pos.top)
    }
});
$('.logo-btn .increase-size').click(() => {
    console.log($('.internship-logo'))
    var preWidth = $('.internship-logo').css('width');
    console.log(preWidth)
    $('.internship-logo').css({
        width: (+preWidth.slice(0, preWidth.length - 2) + 2) + 'px'
    })
    preWidth = $('.internship-logo').css('width');
    $('.logo-btn .font-size-badge').text(+preWidth.slice(0, preWidth.length - 2))
})

$('.logo-btn .decrease-size').click(() => {
    var preWidth = $('.internship-logo').css('width');
    console.log(preWidth)
    $('.internship-logo').css({
        width: (+preWidth.slice(0, preWidth.length - 2) - 2) + 'px'
    })
    preWidth = $('.internship-logo').css('width');
    $('.logo-btn .font-size-badge').text(+preWidth.slice(0, preWidth.length - 2))
})



$('.logo-btn .up').click(() => {
    var yCoordicate = $('.internship-logo').css('top');

    $('.internship-logo').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.internship-logo').css('top');
    $('.logo-btn .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.logo-btn .down').click(() => {
    var yCoordicate = $('.internship-logo').css('top');

    $('.internship-logo').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.internship-logo').css('top');
    $('.logo-btn .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.logo-btn .left').click(() => {
    var xCoordicate = $('.internship-logo').css('left');

    $('.internship-logo').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.internship-logo').css('left');
    $('.logo-btn .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.logo-btn .right').click(() => {
    var xCoordicate = $('.internship-logo').css('left');

    $('.internship-logo').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.internship-logo').css('left');
    $('.logo-btn .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})



// signature 


// $('.upload-signature').click(() => {
//     var element = document.createElement('img')
//     element.setAttribute('class', 'signature-logo')
//     element.setAttribute('src', 'signature.png')
//     document.querySelector('.appender').appendChild(element)
//     console.log(element)
//     $('.signature-logo').css({
//         position: 'absolute',
//         top: '300px',
//         left: '600px',
//         zIndex: '7',
//         width: '100px'
//     })
//     $('.sign-logo-invisibles').removeClass('invisible')

// })



//////sign - logo 




$('.signature-logo').draggable({
    drag: (event, ui) => {
        var pos = ui.position
        $('.sign-logo-btn .x-coordinate-badge').text(pos.left)
        $('.sign-logo-btn .y-coordinate-badge').text(pos.top)
    }
});
$('.sign-logo-btn .increase-size').click(() => {
    console.log($('.signature-logo'))
    var preWidth = $('.signature-logo').css('width');
    console.log(preWidth)
    $('.signature-logo').css({
        width: (+preWidth.slice(0, preWidth.length - 2) + 2) + 'px'
    })
    preWidth = $('.signature-logo').css('width');
    $('.sign-logo-btn .font-size-badge').text(+preWidth.slice(0, preWidth.length - 2))
})

$('.sign-logo-btn .decrease-size').click(() => {
    var preWidth = $('.signature-logo').css('width');
    console.log(preWidth)
    $('.signature-logo').css({
        width: (+preWidth.slice(0, preWidth.length - 2) - 2) + 'px'
    })
    preWidth = $('.signature-logo').css('width');
    $('.sign-logo-btn .font-size-badge').text(+preWidth.slice(0, preWidth.length - 2))
})



$('.sign-logo-btn .up').click(() => {
    var yCoordicate = $('.signature-logo').css('top');

    $('.signature-logo').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) - 2) + 'px'
    })
    yCoordicate = $('.signature-logo').css('top');
    $('.sign-logo-btn .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.sign-logo-btn .down').click(() => {
    var yCoordicate = $('.signature-logo').css('top');

    $('.signature-logo').css({
        top: (+yCoordicate.slice(0, yCoordicate.length - 2) + 2) + 'px'
    })
    yCoordicate = $('.signature-logo').css('top');
    $('.sign-logo-btn .y-coordinate-badge').text(+yCoordicate.slice(0, yCoordicate.length - 2))
})

$('.sign-logo-btn .left').click(() => {
    var xCoordicate = $('.signature-logo').css('left');

    $('.signature-logo').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) - 2) + 'px'
    })
    xCoordicate = $('.signature-logo').css('left');
    $('.sign-logo-btn .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})

$('.sign-logo-btn .right').click(() => {
    var xCoordicate = $('.signature-logo').css('left');

    $('.signature-logo').css({
        left: (+xCoordicate.slice(0, xCoordicate.length - 2) + 2) + 'px'
    })
    xCoordicate = $('.signature-logo').css('left');
    $('.sign-logo-btn .x-coordinate-badge').text(+xCoordicate.slice(0, xCoordicate.length - 2))
})
