import sys

import utilities as util

pulitzer_nonfiction = {
    "url": "https://en.wikipedia.org/wiki/Pulitzer_Prize_for_General_Nonfiction",
    "tag_order": ["table", "tr", "th", "td"],
    "table": {
        "attr": "class",
        "attr_select": "sortable",
        "attr_remove": None,
        "optional_attr": None,
        "scrape_text_children": 0
    },
    "tr": {
        "attr": "style",
        "attr_select": "background:#fff7c9",
        "attr_remove": None,
        "optional_attr": None,
        "scrape_text_children": 2
    },
    "th": {
        "attr": "scope",
        "attr_select": "row",
        "attr_remove": None,
        "optional_attr": "rowspan",
        "optional_reason": "depth",
        "scrape_text_children": 0,
        "count": 1
    },
    "td": {
        "attr": None,
        "attr_select": None,
        "attr_remove": None,
        "optional_attr": None,
        "scrape_text_children": 0,
        "count": 3
    },
}

def main(argv):
    controller = pulitzer_nonfiction
    url = controller["url"]
    levels = len(controller["tag_order"])
    i = 0

    soup = util.get_soup(url)

    while i < levels:
        cur_tag = controller["tag_order"][i]
        cur_dict = controller[cur_tag]

        if cur_dict["attr"]:
            cur_level = util.soup_find_all_one_attr(soup, cur_tag, cur_dict["attr_select"], cur_dict["attr"])
        else:
            cur_level = util.soup_find_all(soup, cur_tag)

        if cur_dict["attr_remove"]:
            cur_level = util.remove_components_with_header(cur_level, cur_dict["attr_remove"], cur_dict["attr"])


        for n in range(1, cur_dict["scrape_text_children"] + 1):
            temp_count = i + n
            child_tag = controller["tag_order"][temp_count]
            child_dict = controller[child_tag]

            if child_dict["attr"]:
                child_level = util.soup_find_all_one_attr(soup, child_tag, child_dict["attr_select"], child_dict["attr"])
            else:
                child_level = util.soup_find_all(soup, child_tag)

            if child_dict["attr_remove"]:
                child_level = util.remove_components_with_header(child_tag, child_dict["attr_remove"], child_dict["attr"])

            if child_dict["count"] == 1:




        i += 1




main(sys.argv)



