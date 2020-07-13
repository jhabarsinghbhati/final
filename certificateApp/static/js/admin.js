window.onload = () => {
    let val = window.location.search.substring(1).split('=')
    let a = val[0], b = val[1]
    console.log(a, b)
    if (a == 'first_name' && b) {
        $('#filter>strong').text(`Filtered intern by first name = ${b}`)
        // console.log('filter by f name')
    } else if (a == 'last_name' && b) {
        // console.log('filter by last name')
        $('#filter>strong').text(`Filtered intern by last name = ${b}`)
    } else if (a == 'reg_number' && b) {
        $('#filter>strong').text(`Filtered intern by registration number = ${b}`)
        // console.log('filter by reg number')
    } else if (a == 'days_from_now' && b) {
        $('#filter>strong').text(`Filtered intern by internship ending within days from now = ${b}`)
        // console.log('filter by days from now')
    } else if (a == "update_request" && b) {
        $('#filter>strong').text(`Filtered interns by detail update request`)
        // console.log('filter by update request')
    }
    // else console.log('all')
}
function selectType() {
    var option = document.getElementById('select')
    var searchfield = document.getElementById('searchfield')
    searchfield.name = option.value
    if (option.value == 'days_from_now') {
        searchfield.type = 'number'
        searchfield.placeholder = 'days'
    }
    else {
        searchfield.type = 'text'
        searchfield.placeholder = option.options[option.selectedIndex].text
    }
    if (option.value == '1') {
        searchfield.disabled = true
        searchfield.placeholder = 'All'
    }
    else searchfield.disabled = false
    if (option.value == 'update_request') {
        searchfield.value = "True"
    }
}
function changestatus(event, id) {
    event.preventDefault()
    $(`#status-btn${id}`).children('span').show()
    form = $(`#status-form${id}`)
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        success: (data) => {
            $(`#status-btn${id}`).children('span').hide()
            res = data['message']
            message = $(`<div class="px-4 mx-5 p-1 alert alert-info alert-dismissible fade show" role="alert">
                            ${res}
                            <button type="button" class="p-1 close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>`)
            message.insertBefore(`#report${id}`).show('normal')

            status = data['status']
            // console.log(status,id)
            if (status == "P") {
                $(`#page-status${id}`).text('Pending')
                $(`#current-status${id}`).text('Pending')
            } else if (status == "A") {
                $(`#page-status${id}`).text('Approved')
                $(`#current-status${id}`).text('Approved')
            } else {
                $(`#page-status${id}`).text('Rejected')
                $(`#current-status${id}`).text('Rejected')
            }
        },
        error: (data) => {
            $(`#status-btn${id}`).children('span').hide()
            try {
                message = data['responseJSON']['message']
            }
            catch (err) {
                message = 'Something went wrong please contact developer.'
            }
            message = $(`<div class="px-4 mx-5 p-1 alert alert-danger alert-dismissible fade show" role="alert">
                            ${message}
                            <button type="button" class="p-1 close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>`)
            message.insertBefore(`#report${id}`).show('normal')
        }
    })
}

// var test
function generatecertificate(self, url, id) {
    if ($(`#current-status${id}`).text().trim() != 'Approved') {
        alert('Please approve the status of report first to generate certificate')
    } else {
        self = $(self)
        self.children('span').show()
        $.ajax({
            url: url,
            success: (data) => {
                self.children('span').hide()
                self.hide('normal')
                // console.log(data)
                pdfurl = data['pdfurl']
                pngurl = data['pngurl']
                delurl = data['delurl']

                ckt = `<a href="${pdfurl}" target="=_blank">PDF</a>
                    <a href="${pngurl}" download target="=_blank">PNG</a>
                    <button onclick="deleteCertificate(this,${id},'${delurl}')" class="ml-2 btn btn-sm btn-dark">
                        <span class="spinner-border spinner-border-sm mr-1" role="status" aria-hidden="true"
                        style="display: none;"></span>Delete</button>`
                $(`#certificate-div${id}`).html(ckt)

                cktno = data['cktno']
                $(`#certificate-generated${id}`).text('Yes')
                $(`#certificate-number${id}`).html(`<a href="${pdfurl}" target="_blank">${cktno}</a>`)
                // $('#report').append(ckt.show('normal'))
            },
            error: (data) => {
                // test = data
                self.children('span').hide()
                try {
                    message = data['responseJSON']['message']
                }
                catch (err) {
                    message = 'Something went wrong please contact developer.'
                }
                message = $(`<div class="px-4 mx-5 p-1 alert alert-danger alert-dismissible fade show" role="alert">
                                ${message}
                                <button type="button" class="p-1 close" data-dismiss="alert" aria-label="Close">
                                    <span aria-hidden="true">&times;</span>
                                </button>
                            </div>`)
                message.insertBefore(`#report${id}`).show('normal')
            }
        })
    }
}

function deleteCertificate(self, id, url) {
    self = $(self)
    test = self
    console.log(self)
    self.children('span').show()
    $.ajax({
        url: url,
        success: (data) => {
            // self.children('span').hide()
            self.hide()
            creurl = data['creurl']
            upurl = data['upurl']
            btn = `<button onclick="generatecertificate(this,'${creurl}',${id})" class="mr-2 btn btn-sm btn-dark">
                <span class="spinner-border spinner-border-sm mr-1" role="status" aria-hidden="true"
                style="display: none;"></span>Generate</button>or<button class="mx-2 btn btn-sm btn-danger"
                onClick="upload('${upurl}','popup')">Upload</button>`
            self.parent().html(btn)

            // Alert messages of reponse
            message = data['message']
            message = $(`<div class="px-4 mx-5 p-1 alert alert-success alert-dismissible fade show" role="alert">
                            ${message}
                            <button type="button" class="p-1 close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>`)
            message.insertBefore(`#report${id}`).show('normal')

            $(`#certificate-generated${id}`).text('No')
            $(`#certificate-number${id}`).html('-')
        },
        error: (data) => {
            self.children('span').hide()
            try {
                message = data['responseJSON']['message']
            }
            catch (err) {
                message = 'Something went wrong please contact developer.'
            }
            message = $(`<div class="px-4 mx-5 p-1 alert alert-danger alert-dismissible fade show" role="alert">
                            ${message}
                            <button type="button" class="p-1 close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>`)
            message.insertBefore(`#report${id}`).show('normal')
        }
    })
}


function approvestatus(self, id, url, div, status) {
    self = $(self)
    div = $(`#${div}`)
    self.children('span').show()
    $.ajax({
        url: url,
        success: (data) => {
            self.parent().parent().hide('normal')
            div.text(status)
        },
        error: (data) => {
            self.children('span').hide()
            try {
                message = data['responseJSON']['message']
            }
            catch (err) {
                message = 'Something went wrong please contact developer.'
            }
            message = $(`<div class="px-4 mx-5 p-1 alert alert-danger alert-dismissible fade show" role="alert">
                            ${message}
                            <button type="button" class="p-1 close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                            </button>
                        </div>`)
            message.insertBefore(`#report${id}`).show('normal')
        }
    })
}

function upload(href, name) {
    var win = window.open(href, name, 'height=500,width=800,resizable=yes,scrollbars=yes');
    win.focus();
    return false;
}
function closePopup(win, id, delurl, pdfurl, pngurl, cktno) {
    ckt = `<a href="${pdfurl}" target="=_blank">PDF</a>
                    <a href="${pngurl}" download target="=_blank">PNG</a>
                    <button onclick="deleteCertificate(this,${id},'${delurl}')" class="ml-2 btn btn-sm btn-dark">
                        <span class="spinner-border spinner-border-sm mr-1" role="status" aria-hidden="true"
                        style="display: none;"></span>Delete</button>`
    $(`#certificate-div${id}`).html(ckt)

    $(`#certificate-generated${id}`).text('Yes')
    $(`#certificate-number${id}`).html(`<a href="${pdfurl}" target="_blank">${cktno}</a>`)
    win.close();
}