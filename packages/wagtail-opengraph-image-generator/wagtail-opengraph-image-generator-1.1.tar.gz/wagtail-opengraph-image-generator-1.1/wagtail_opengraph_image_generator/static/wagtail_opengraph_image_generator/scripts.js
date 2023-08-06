$(document).ready(() => {
    const previewBtn = $('#btnCreateOGPreview')
    const defaultBtnText = previewBtn.text()
    previewBtn.on('click', (e) => {
        e.preventDefault()
        previewBtn.text(`${defaultBtnText} ...`).attr('disabled', true)

        let url
        if (location.href.indexOf('/pages/add/') !== -1) {
            // Are we creating a new page?
            url = `/admin/wagtail_opengraph_image_generator/preview/0/`
        } else if (location.href.indexOf('/edit/')) {
            // or are we editing an existing page?
            url = `/admin/wagtail_opengraph_image_generator/preview/${
                location.pathname.split('/')[3]
            }/`
        }

        $.post(
            url,
            {
                title: $(`#id_${OG_FIELD_TITLE}`)
                    .parent()
                    .find('.public-DraftEditor-content')
                    .html(),
                default_title: $('#id_title').val(),
                subtitle: $(`#id_${OG_FIELD_SUBTITLE}`)
                    .parent()
                    .find('.public-DraftEditor-content')
                    .html(),
                background_image: $(`#id_${OG_FIELD_BACKGROUND_IMAGE}`).val(),
                logo: $(`#id_${OG_FIELD_LOGO}`).val(),
                variant: $('#id_og_dark_variant').is(':checked')
                    ? 'dark'
                    : 'light',
            },
            (data) => {
                $('img.og-preview, div.og-preview-placeholder').remove()
                $('label.og-field:last-of-type').show()
                $(
                    `<img class="og-preview" src='data:image/png;base64,${data}'>`
                ).insertAfter(previewBtn)
                previewBtn.text(defaultBtnText).attr('disabled', false)
            }
        ).fail((error) => {
            previewBtn
                .text('Something went wrong. Try again.')
                .attr('disabled', false)
        })
    })
})
