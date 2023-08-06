"""
Helper module for reportng
"""
import dominate.tags as tag
from dominate.util import raw
import logging
from random import choice


def check_keys(keys: list, check_dict: dict):
    for k in keys:
        if not check_dict.get(k):
            raise TypeError("{} key not found".format(k))
    return True


class JSCSS:
    """
    This class controls constants that can be modified by the user and can be
    pointed to local files to host them locally. Can be used with
    ``DownloadAssets(download_path, rel_path)`` class to save all files locally and point them
    correctly
    """

    #: bootswatch theme
    bootswatch = "https://bootswatch.com/4/lux/bootstrap.min.css"
    #: jquery: Constant that handles jqery.min.js
    jquery = "https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"
    #: bs4_js: Constant that handles bootstrap.min.js
    bs4_js = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
    # highlight_custom: Constant that handles the custom js that aids in highlighting
    # comment highlight_custom = "https://cdn.rawgit.com/securisec/reportng/master/js/highlight.js"
    #: font_awesome: Constant that handles font awesomes all.min.js
    font_awesome = "https://use.fontawesome.com/releases/v5.0.6/css/all.css"
    #: asciinema_css: Constant that handles asciinema-player.min.js
    asciinema_css = "https://cdnjs.cloudflare.com/ajax/libs/asciinema-player/2.4.1/asciinema-player.min.css"
    #: asciinema_js: Constant that handles asciinema-player.min.js
    asciinema_js = "https://cdnjs.cloudflare.com/ajax/libs/asciinema-player/2.4.1/asciinema-player.min.js"
    #: highlighjs_css: Constant that handles highlight.js default.min.js
    highlightjs_css = "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/default.min.css"
    #: highlight_js: Constant that handles highlight.min.js
    highlightjs_js = (
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/highlight.min.js"
    )
    #: progressbar: Constant that handles progressbar.js
    progressbar_js = (
        "https://cdn.rawgit.com/securisec/reportng/master/js/progressbar.js"
    )
    #: mark_js: Constant that handles mark.js
    mark_js = "https://cdnjs.cloudflare.com/ajax/libs/mark.js/8.11.1/jquery.mark.min.js"
    #: popper_js = Constant that handles popper.js
    popper_js = (
        "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"
    )


class CSSControl:
    """
    CSS control
    """

    #: css_overflow: This value can be modified globally so that all containers are the same size similar to the output report_code_section. Can be modified directly, or using overflow option in report_section
    css_overflow = "max-height: 70%; overflow: auto; margin-bottom: 20"
    #: jumbotron_style: Style attribute values of jumbotron
    jumbotron_style = "padding-bottom:3; padding-top:40"
    #: sticky_section_css: Controls if section should sticky with preceeding section
    sticky_section_css = "padding:0; margin-top:-2rem;"
    #: not_stick_section: Controls if the section is not a sticky
    not_sticky_section = "padding-bottom:3; padding-top:40;"


class JSCustom:
    """
    Class that handles all the custom JS code. It is best not to modify any of this code.
    """

    tooltip_js = """
                $(function () {
                    $('[data-toggle="tooltip"]').tooltip()
                })
                """

    highlight_js = """
                function clickHighlight() {
                    document.getElementById("performbutton").click();
                }
                """

    populate_navbar_onload = """
                function populateDropdown() {
                    var headings = $('h1')
                    var select = document.getElementById("ddmenu");
                    for (var i = 0; i < headings.length; i++){
                        var a = document.createElement("a")
                        a.setAttribute("class", "dropdown-item " + headings[i].className);
                        a.setAttribute("href", "#" + headings[i].id)
                        a.innerHTML = headings[i].innerText;
                        select.appendChild(a);
                    }
                }
                window.onload = populateDropdown
                """

    smoothscroll_navbar_pad = """
                $(document).on('click', 'a[href^="#"]', function (event) {
                    event.preventDefault();
                    $('html, body').animate({
                        scrollTop: $($.attr(this, 'href')).offset().top-150
                    }, 500);
                });
                """

    dropdown_filter = """
                $(document).ready(function(){
                $("#ddfilter").on("keyup", function() {
                    var value = $(this).val().toLowerCase();
                    $(".dropdown-menu a").filter(function() {
                    $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
                    });
                });
                });
                """

    progress_bar = """
                $(function() {
                $("body").prognroll({
                    height: 7
                });
                });
                """

    markjs_script = """
                $(function () {
                    var $input = $("input[type='search']"),
                        $clearBtn = $("button[data-search='clear']"),
                        $prevBtn = $("button[data-search='prev']"),
                        $nextBtn = $("button[data-search='next']"),
                        $content = $(".context"),
                        $results,
                        currentClass = "current",
                        offsetTop = 150,
                        currentIndex = 0;
                    function jumpTo() {
                        if ($results.length) {
                            var position,
                                $current = $results.eq(currentIndex);
                            $results.removeClass(currentClass);
                            if ($current.length) {
                                $current.addClass(currentClass);
                                position = $current.offset().top - offsetTop;
                                window.scrollTo(0, position);
                            }
                        }
                    }
                    $input.on("input", function () {
                        var searchVal = this.value;
                        $content.unmark({
                            done: function () {
                                $content.markRegExp(RegExp(searchVal), {
                                    separateWordSearch: false,
                                    done: function () {
                                        $results = $content.find("mark");
                                        currentIndex = 0;
                                        var c = document.getElementById('searchcount');
                                        c.innerHTML = $results.length;
                                        jumpTo();
                                    }
                                });
                            }
                        });
                    });
                    $nextBtn.add($prevBtn).on("click", function () {
                        if ($results.length) {
                            currentIndex += $(this).is($prevBtn) ? -1 : 1;
                            if (currentIndex < 0) {
                                currentIndex = $results.length - 1;
                            }
                            if (currentIndex > $results.length - 1) {
                                currentIndex = 0;
                            }
                            jumpTo();
                        }
                    });
                });
                    """

    themes_preview = """
            $('.ddtheme').click(function(e){
            themes = {
                'Default' : 'https://bootswatch.com/_vendor/bootstrap/dist/css/bootstrap.min.css',
                'Cerulean' : 'https://bootswatch.com/4/cerulean/bootstrap.min.css',
                'Cosmo' : 'https://bootswatch.com/4/cosmo/bootstrap.min.css',
                'Cyborg' : 'https://bootswatch.com/4/cyborg/bootstrap.min.css',
                'Darkly' : 'https://bootswatch.com/4/darkly/bootstrap.min.css',
                'Flatly' : 'https://bootswatch.com/4/flatly/bootstrap.min.css',
                'Journal' : 'https://bootswatch.com/4/journal/bootstrap.min.css',
                'Litera' : 'https://bootswatch.com/4/litera/bootstrap.min.css',
                'Lumen' : 'https://bootswatch.com/4/lumen/bootstrap.min.css',
                'Lux' : 'https://bootswatch.com/4/lux/bootstrap.min.css',
                'Materia' : 'https://bootswatch.com/4/materia/bootstrap.min.css',
                'Minty' : 'https://bootswatch.com/4/minty/bootstrap.min.css',
                'Pulse' : 'https://bootswatch.com/4/pulse/bootstrap.min.css',
                'Sandstone' : 'https://bootswatch.com/4/sandstone/bootstrap.min.css',
                'Simplex' : 'https://bootswatch.com/4/simplex/bootstrap.min.css',
                'Sketchy' : 'https://bootswatch.com/4/sketchy/bootstrap.min.css',
                'Slate' : 'https://bootswatch.com/4/slate/bootstrap.min.css',
                'Solar' : 'https://bootswatch.com/4/solar/bootstrap.min.css',
                'Spacelab' : 'https://bootswatch.com/4/spacelab/bootstrap.min.css',
                'Superhero' : 'https://bootswatch.com/4/superhero/bootstrap.min.css',
                'United' : 'https://bootswatch.com/4/united/bootstrap.min.css',
                'Yeti' : 'https://bootswatch.com/4/yeti/bootstrap.min.css',
        }
        var choice = $('#dropdownId');
        console.log(choice)
        choice.text(this.innerHTML);
        if (choice[0].innerHTML in themes){
            $('#bootswatch').attr('href', themes[choice[0].innerHTML])
        }
        
    });
                """


class CustomHTML:
    """
    Some custom HTML to help with element creation
    """

    themes_preview = """
    <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
        <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="javascript:void(0)" id="dropdownId" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Themes</a>
            <div class="dropdown-menu" aria-labelledby="dropdownId">
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Default</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Cerulean</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Cosmo</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Cyborg</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Darkly</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Flatly</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Journal</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Litera</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Lumen</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Lux</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Materia</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Minty</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Pulse</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Sandstone</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Simplex</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Sketchy</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Slate</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Solar</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Spacelab</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Superhero</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">United</a>
            <a class="dropdown-item ddtheme" href="javascript:void(0)">Yeti</a>
            </div>
        </li>
    </ul>
    """


class NotValidTag(Exception):
    """
    Exception to handle invalid tag for background color control
    """

    pass


class ObjectNotInitiated(Exception):
    """
    Exception when a method is called but not initiated
    """

    pass


class TooManyValues(Exception):
    """
    Exception when too many args are passed
    """

    pass


class TableError(Exception):
    """
    Exception when there are problems with creating a table
    """

    pass


class HelperFunctions:
    """
    Some helper functions that does not impact how enduser uses reportng
    """

    #: Valid options for colors/cards etc
    valid_tags = [
        "primary",
        "secondary",
        "success",
        "danger",
        "warning",
        "info",
        "light",
        "dark",
        "default",
        "red",
        "green",
        "blue",
        "yellow",
        "light",
    ]

    @staticmethod
    def id_with_random(length, title):
        random_string = "".join(
            [choice("abcdefghijklmnopqrstuvwxyz") for _ in range(length)]
        )
        return "".join(e for e in title if e.isalnum()) + random_string

    @staticmethod
    def color_to_tag(s):
        """
        Maps colors to their appropriate tags
        """
        if s == "red":
            s = "danger"
        elif s == "green":
            s = "success"
        elif s == "yellow":
            s = "warning"
        elif s == "blue":
            s = "info"
        elif s == "light":
            s = "secondary"
        elif s == "primary":
            s = "primary"
        else:
            s = s
        return s

    @staticmethod
    def convert_to_string(s):
        """
        Converts an object to string
        """
        return "%s" % s

    @staticmethod
    # Function that creates to ol tags and populates with il tags for
    # carousel count indicator
    def slide_indicator(num):
        """
        Helper function that controls how image slide count works
        """
        with tag.ol(_class="carousel-indicators") as o:
            for cnt in range(num):
                if cnt == 0:
                    tag.li(
                        data_target="#carousel_controls",
                        data_slide_to="0",
                        _class="active",
                    )
                else:
                    tag.li(
                        data_target="#carousel_controls", data_slide_to="%s" % str(cnt)
                    )
        return o

    @staticmethod
    # Function to create the cards
    def make_cards(b_only, k, h, v):
        """
        Helper function that helps making cards
        """
        if k not in HelperFunctions.valid_tags:
            raise NotValidTag(
                "\n\n%s is not a valid tag. \nChoose one of the following: \n%s"
                % (k, "\n".join([x for x in HelperFunctions.valid_tags]))
            )
        # checks bool and determines styling
        if b_only:
            style = "border"
            text = "text-primary"
        else:
            style = "bg"
            text = "text-white"
        with tag.div(
            _class="card %s %s-%s m-3" % (text, style, HelperFunctions.color_to_tag(k)),
            style="width: 20rem;",
        ) as m:
            tag.div(h, _class="card-header")
            with tag.div(_class="card-body"):
                tag.p(v, _class="card-text")
        return m

    @staticmethod
    # Function to create alerts in sections
    def make_alert(data):
        """
        Helper function that creates dismissable alerts
        """
        color = data.get("color") or "primary"
        message = data.get("message")
        with tag.div(
            message,
            _class="reportng-alert-message-class alert alert-dismissible alert-%s"
            % HelperFunctions.color_to_tag(color),
        ) as a:
            raw(
                '<button type="button" class="close" data-dismiss="alert">&times;</button>'
            )
        return a

    @staticmethod
    def ref_button(data):
        """
        Places a button with href on it.
        """
        if isinstance(data, dict):
            color = data.get("color") or "primary"
            link = data.get("link")
            b = tag.a(
                "Reference",
                _class="reportng-ref-button-class btn btn-outline-%s btn-sm float-right"
                % HelperFunctions.color_to_tag(color),
                href=link,
                role="button",
                target="_blank",
            )
            return b

    @staticmethod
    def create_badges(b):
        """
        Creates badges at the bottom of a section
        """
        total = ""
        if not isinstance(b, list):
            raise NotValidTag("Use a list of dictionaries to create badges")
        for i in range(len(b)):
            color = b[i].get("color") or "primary"
            message = b[i].get("message")
            assert message, "No messages passed"
            assert color in HelperFunctions.valid_tags, NotValidTag(
                "Choose a valid tag color from\n%s"
                % " ".join(HelperFunctions.valid_tags)
            )
            total += str(
                tag.span(
                    message,
                    _class="reportng-badge-class badge badge-%s float-right"
                    % HelperFunctions.color_to_tag(color),
                )
            )
        return total

    @staticmethod
    def make_modals(section, info):
        if not "button" in info:
            button = "Info"
        else:
            button = info["button"]
        for k in ["title", "message"]:
            if not k in info:
                raise NotValidTag("Make sure to use both title and content keys")
        modal_title = info["title"].replace(" ", "")
        modal_content = info["message"]
        tag.button(
            button,
            type="button",
            _class="btn btn-primary btn-md reportng-button-class",
            data_toggle="modal",
            data_target="#%s" % modal_title,
        )
        with tag.div(
            _class="modal fade",
            id="%s" % modal_title,
            tabindex="-1",
            role="dialog",
            aria_labelledby="model%s" % modal_title,
            aria_hidden="true",
        ):
            with tag.div(_class="modal-dialog", role="document"):
                with tag.div(_class="modal-content reportng-modal-content-class"):
                    with tag.div(_class="modal-header reportng-modal-header-class"):
                        tag.h4(
                            modal_title,
                            _class="modal-title reportng-modal-title-class",
                            id="model%s" % modal_title,
                        )
                    with tag.div(_class="modal-body reportng-modal-body-class"):
                        tag.div(
                            modal_content,
                            _class="container-fluid",
                            style="word-wrap: break-word;",
                        )
                    with tag.div(_class="modal-footer reportng-modal-footer-class"):
                        tag.button(
                            "Close",
                            type="button",
                            _class="btn btn-sm btn-secondary",
                            data_dismiss="modal",
                        )

    @staticmethod
    def accordian_collapse(color, title, content, pre, raw_html, **kwargs):
        """
        Creates a collapsible accordian
        """
        title_random = HelperFunctions.id_with_random(5, title)
        with tag.div(
            _class="jumbotron container reportng-section-collapsible-class"
        ) as h:
            # with tag.div(id="accordian"):
            with tag.div(_class="card"):
                with tag.div(
                    _class="card-header %s reportng-collapse-card-header-class" % color,
                    id="headingOne%s" % title_random,
                ):
                    tag.h1(
                        title,
                        _class=color,
                        data_toggle="collapse",
                        data_target="#collapse%s" % title_random,
                        aria_expanded="true",
                        aria_controls="collapse%s" % title_random,
                        id=title_random,
                    )
                with tag.div(
                    id="collapse%s" % title_random,
                    _class="collapse",
                    aria_labelledby="headingOne%s" % title_random,
                    data_parent="#accordion",
                ):
                    with tag.div(
                        _class="card-body context reportng-collapse-card-body-class"
                    ):
                        if raw_html != "":
                            raw(raw_html)
                        elif pre:
                            tag.pre(content)
                        else:
                            tag.p(content)
                if "alert" in kwargs:
                    HelperFunctions.make_alert(kwargs.get("alert"))
                if "badge" in kwargs:
                    HelperFunctions.create_badges(kwargs.get("badge"))
        return HelperFunctions.convert_to_string(h)
