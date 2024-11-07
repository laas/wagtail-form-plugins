// [label, char, widgets, processing function]
const OPERATORS = {
    'eq': ['=', 'senu', (a, b) => a.value === b],
    'neq': ['≠', 'senu', (a, b) => a.value !== b],

    'is': ['=', 'lrd', (a, b) => a === b],
    'nis': ['≠', 'lrd', (a, b) => a !== b],

    'lt': ['<', 'n', (a, b) => a < parseFloat(b)],
    'lte': ['≤', 'n', (a, b) => a <= parseFloat(b)],

    'ut': ['>', 'n', (a, b) => a > parseFloat(b)],
    'ute': ['≥', 'n', (a, b) => a >= parseFloat(b)],

    'bt': ['<', 'dt', (a, b) => a < Date.parse(b)],
    'bte': ['≤', 'd', (a, b) => a <= Date.parse(b)],

    'at': ['>', 'dt', (a, b) => a > Date.parse(b)],
    'ate': ['≥', 'd', (a, b) => a >= Date.parse(b)],

    'ct': ['∋', 'mCL', (a, b) => a.includes(b)],
    'nct': ['∌', 'mCL', (a, b) => ! a.includes(b)],

    'c': ['✔', 'c', (a, b) => a],
    'nc': ['✖', 'c', (a, b) => !a],
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
            'type': Array.from(dom_block.querySelector('.formbuilder-field-block').classList)
                .find((classname) => classname.startsWith('formbuilder-field-block-'))
                .split('-')[3]
        }
    ]));
}

function get_value_choices(selected_field) {
    return Array.from(selected_field.dom_block.querySelectorAll(
        '.formbuilder-field-block .formbuilder-choices > div > div:not([aria-hidden])'
    ))
        .map((dom_block) => dom_block.querySelector('.struct-block .formbuilder-choice-label input'))
        .map((dom_label, index) => [`c${index + 1}`, dom_label.value])
}

function get_field_choices(fields, field_index) {
    return [
        ['', 'Fields:', true],
        ...Object.values(fields)
            .filter((f) => field_index > f.index)
            .filter((f) => f.type !== 'hidden')
            .map(f => [f.contentpath, f.label, false]),
        ['', 'Expression:', true],
        ['or', 'one of...', false],
        ['and', 'all of...', false],
    ]
}

function on_rule_subject_selected(dom_dropdown) {
    const dom_beb = dom_dropdown.closest('.formbuilder-beb')

    const dom_input_field_id = dom_beb.querySelector('.formbuilder-beb-field > div > input')
    dom_input_field_id.value = dom_dropdown.value

    const dom_operator = dom_beb.querySelector('div:has(> div > .formbuilder-beb-operator)');
    const dom_val_char = dom_beb.querySelector('div:has(> div > .formbuilder-beb-val-char)');
    const dom_val_num = dom_beb.querySelector('div:has(> div > .formbuilder-beb-val-num)');
    const dom_val_list = dom_beb.querySelector('div:has(> div > .formbuilder-beb-val-list)');
    const dom_val_date = dom_beb.querySelector('div:has(> div > .formbuilder-beb-val-date)');
    const dom_rules = dom_beb.querySelector('div:has(> .formbuilder-beb-rules)');

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

        const operators = Object.entries(OPERATORS)
            .filter(([i, [c, opr_widgets, f]]) => opr_widgets.includes(field_type_id))
            .map(([opr_id, cwf]) => opr_id)

        for (dom_option of dom_operator.querySelectorAll('select > option')) {
            dom_option.classList.toggle('formbuilder-hide', ! operators.includes(dom_option.value))
        }

        if (widget_type === 'dropdown') {
            const dom_val_list_input = dom_val_list.querySelector('input')
            const dom_dropdown = build_virtual_dropdown(dom_val_list_input, get_value_choices(selected_field))
            dom_val_list_input.value = dom_dropdown.value
        }
    }

    if (dom_operator.querySelector('select option:not(.formbuilder-hide):checked') === null) {
        dom_operator.querySelector('select option:not(.formbuilder-hide)').selected = true
    }
}

function build_virtual_dropdown(dom_input, choices) {
    let dom_dropdown = dom_input.parentNode.querySelector('select')
    const selection = dom_input.value || choices.find(([k, s, disabled]) => ! disabled)[0]

    if (dom_dropdown === null) {
        dom_dropdown = document.createElement('select');
        dom_dropdown.addEventListener('change', (event) => dom_input.value = event.target.value)
        dom_input.parentNode.insertBefore(dom_dropdown, dom_input);
    } else {
        dom_dropdown.innerHTML = ""
    }

    for (const [choice_key, choice_label, disabled] of choices) {
        const dom_option = document.createElement('option');
        dom_option.value = choice_key;
        dom_option.text = choice_label;
        dom_option.disabled = disabled;
        dom_option.selected = selection === undefined ? false : (choice_key === selection);
        dom_dropdown.appendChild(dom_option);
    }

    // console.log(dom_dropdown)
    return dom_dropdown
}

class BEBBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);

        const dom_beb = block.container[0];
        const dom_field_block_container = dom_beb.closest('.formbuilder-field-block').parentNode.parentNode.parentNode;

        const fields = get_fields()
        const field_index = fields[dom_field_block_container.getAttribute('data-contentpath')].index;

        if (field_index === 0) {
            return block
        }

        // console.log('yay')
        const dom_rules = build_virtual_dropdown(
            dom_beb.querySelector('.formbuilder-beb-field input'),
            get_field_choices(fields, field_index),
        )
        dom_rules.addEventListener('change', (event) => on_rule_subject_selected(event.target))
        on_rule_subject_selected(dom_rules)

        return block;
    }
}
window.telepath.register('forms.blocks.BooleanExpressionBuilderBlock', BEBBlockDefinition);
