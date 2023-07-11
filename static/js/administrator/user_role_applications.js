import {bg_light_on_hover} from "../common/common.js";

$(document).ready(function () {
        $('#applications > div').each(
            function () {
                bg_light_on_hover($(this));
            }
        )
    }
)