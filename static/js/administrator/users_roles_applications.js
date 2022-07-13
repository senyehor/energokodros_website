import {bg_light_on_hover} from "../common/common.js";

$(document).ready(function () {
        // set applications change bg on hover
        $('#applications > div').each(
            function () {
                bg_light_on_hover($(this));
            }
        )
    }
);

