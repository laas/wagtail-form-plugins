// [label, char, widgets, processing function]
const OPERATORS = {
    'eq': ['is equal to', '=', 'senu', (dom_input, value) => dom_input.value === value],
    'neq': ['is not equal to', '≠', 'senu', (dom_input, value) => dom_input.value !== value],

    'is': ['is', '=', 'lrd', (dom_input, value) => dom_input.value === value],
    'nis': ['is not', '≠', 'lrd', (dom_input, value) => dom_input.value !== value],

    'lt': ['is lower than', '<', 'n', (dom_input, value) => parseFloat(dom_input.value) < parseFloat(value)],
    'lte': ['is lower or equal to', '≤', 'n', (dom_input, value) => parseFloat(dom_input.value) <= parseFloat(value)],

    'ut': ['is upper than', '>', 'n', (dom_input, value) => parseFloat(dom_input.value) > parseFloat(value)],
    'ute': ['is upper or equal to', '≥', 'n', (dom_input, value) => parseFloat(dom_input.value) >= parseFloat(value)],

    'bt': ['is before than', '<', 'dt', (dom_input, value) => Date.parse(dom_input.value) < Date.parse(value)],
    'bte': ['is before or equal to', '≤', 'd', (dom_input, value) => Date.parse(dom_input.value) <= Date.parse(value)],

    'at': ['is after than', '>', 'dt', (dom_input, value) => Date.parse(dom_input.value) > Date.parse(value)],
    'ate': ['is after or equal to', '≥', 'd', (dom_input, value) => Date.parse(dom_input.value) >= Date.parse(value)],

    'ct': ['contains', '∋', 'mCL', (dom_input, value) => dom_input.value.includes(value)],
    'nct': ['does not contain', '∌', 'mCL', (dom_input, value) => ! dom_input.value.includes(value)],

    'c': ['is checked', '✔', 'c', (dom_input, value) => dom_input.checked],
    'nc': ['is not checked', '✖', 'c', (dom_input, value) => !dom_input.checked],
}

// [field type identifier, widget type]
const FIELD_CUSTOMIZATION = {
    'singleline': ['s', 'char'],
    'multiline': ['m', 'char'],
    'email': ['e', 'char'],
    'number': ['n', 'number'],
    'url': ['u', 'char'],
    'checkbox': ['c', 'none'],
    'checkboxes': ['C', 'dropdown'],
    'dropdown': ['l', 'dropdown'],
    'multiselect': ['L', 'dropdown'],
    'radio': ['r', 'dropdown'],
    'date': ['d', 'date'],
    'datetime': ['t', 'date'],
    'hidden': ['h', 'char'],
}


function get_fields() {
    const dom_form_fields = document.querySelector('.formbuilder-fields-block > div')
    const dom_block_fields = dom_form_fields.querySelectorAll(':scope > [data-contentpath]:not([aria-hidden])');

    return Object.fromEntries(Array.from(dom_block_fields).map((dom_block, index) => [
        dom_block.getAttribute('data-contentpath'),
        {
            'index': index,
            'contentpath': dom_block.getAttribute('data-contentpath'),
            'label': dom_block.querySelector('.formbuilder-field-block-label input').value || `field n°${ index + 1}`,
            'dom_block': dom_block,
            'type': dom_block.querySelector('.formbuilder-field-block').className.replace('formbuilder-field-block', '').split('-')[1]
        }
    ]));
}

function fill_dropdown(dom_dropdown, choices) {
    dom_dropdown.innerHTML = "";

    for (const [choice_key, choice_label, disabled] of choices) {
        const option = document.createElement('option');
        option.value = choice_key;
        option.text = choice_label;
        option.disabled = disabled;
        dom_dropdown.appendChild(option);    
    }
}

function on_rule_subject_selected(dom_dropdown) {
    const dom_beb = dom_dropdown.closest('.formbuilder-beb')
    const dom_field_block = dom_beb.parentNode.parentNode.parentNode
    const get_field_block = (class_name) => dom_field_block.getElementsByClassName(class_name)[0]?.parentNode;

    const dom_operator = get_field_block('formbuilder-beb-operator').parentNode;
    const dom_val_char = get_field_block('formbuilder-beb-val-char').parentNode;
    const dom_val_num = get_field_block('formbuilder-beb-val-num').parentNode;
    const dom_val_list = get_field_block('formbuilder-beb-val-list').parentNode;
    const dom_val_date = get_field_block('formbuilder-beb-val-date').parentNode;
    const dom_rules = get_field_block('formbuilder-beb-rules');

    if (['and', 'or'].includes(dom_dropdown.value)) {
        dom_operator.classList.toggle('formbuilder-hide', true);
        dom_val_char.classList.toggle('formbuilder-hide', true);
        dom_val_num.classList.toggle('formbuilder-hide', true);
        dom_val_list.classList.toggle('formbuilder-hide', true);
        dom_val_date.classList.toggle('formbuilder-hide', true);
        dom_rules.classList.toggle('formbuilder-hide', false);
    } else {
        const selected_field = get_fields()[dom_dropdown.value]
        const [field_type_id, widget_type] = FIELD_CUSTOMIZATION[selected_field.type];

        dom_operator.classList.toggle('formbuilder-hide', false);
        dom_val_char.classList.toggle('formbuilder-hide', widget_type !== 'char');
        dom_val_num.classList.toggle('formbuilder-hide', widget_type !== 'number');
        dom_val_list.classList.toggle('formbuilder-hide', widget_type !== 'dropdown');
        dom_val_date.classList.toggle('formbuilder-hide', widget_type !== 'date');
        if (dom_rules !== undefined) {
            dom_rules.classList.toggle('formbuilder-hide', true);
        }

        const dom_operator_select = dom_operator.querySelector('select')
        const operator_choices = Object.entries(OPERATORS)
            .filter(([opr_id, [s, c, opr_widgets, f]]) => opr_widgets.includes(field_type_id))
            .map(([opr_id, [opr_str, c, w, f]]) => [opr_id, opr_str, false])
        fill_dropdown(dom_operator_select, operator_choices)

        if (widget_type === 'dropdown') {
            const dom_select = dom_val_list.querySelector('div > div > .w-field__input > select')
            const dom_choices = selected_field.dom_block.querySelectorAll(
                '.formbuilder-field-block .formbuilder-choices > div > div:not([aria-hidden])'
            )
            const value_choices = Array.from(dom_choices)
                .map((dom_block) => dom_block.querySelector('.struct-block .formbuilder-choice-label input'))
                .map((dom_label) => [dom_label.value, dom_label.value])
            fill_dropdown(dom_select, value_choices)
        }

    }
}

function update_rule_subjects_dropdown(dom_beb, fields, field_index) {
    if (field_index === 0) {
        return
    }

    const dom_rule_subject_dropdown = dom_beb.querySelector('.formbuilder-beb-field select')
    const fields_choices = Object.values(fields)
        .filter((f) => field_index > f.index)
        .filter((f) => f.type !== 'hidden')
        .map(f => [f.contentpath, f.label, false])

    fill_dropdown(dom_rule_subject_dropdown, [
        ['', 'Fields:', true],
        ...fields_choices,
        ['', 'Expression:', true],
        ['or', 'one of...', false],
        ['and', 'all of...', false],
    ])

    dom_rule_subject_dropdown.addEventListener('change', (event) => on_rule_subject_selected(event.target))
    on_rule_subject_selected(dom_rule_subject_dropdown)
}


class BEBBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);

        const dom_beb = block.container[0];
        const dom_field_block_container = dom_beb.closest('.formbuilder-field-block').parentNode.parentNode.parentNode;

        const fields = get_fields()
        const current_field = fields[dom_field_block_container.getAttribute('data-contentpath')];

        update_rule_subjects_dropdown(dom_beb, fields, current_field.index);

        return block;
    }
}
window.telepath.register('forms.blocks.BooleanExpressionBuilderBlock', BEBBlockDefinition);
