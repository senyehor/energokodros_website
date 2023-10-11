$(document).ready(() => {
    add_box_identifier_format_info();
})

const BOX_IDENTIFIER_FORMAT_INFO = `Ідентифікатор складається із наступних частин,
 розділених дефісом, літери латинські: 2 літери код міста, 2 літери код закладу,
  2 цифри номер закладу, 3 цифри порядковий номер ящику, 2 цифри дійсна кількість сенсорів, 
  наприклад su-LL-11-222-10`

function add_box_identifier_format_info() {
    __add_muted_text_after_div_label(
        $('#div_id_box-identifier'),
        BOX_IDENTIFIER_FORMAT_INFO
    )
}