const OPERATORS = {
    'eq': ['is equal to', '=', ['char', 'number', 'dropdown', 'date'], (a, b) => a === b],
    'neq': ['is not equal to', '≠', ['char', 'number', 'dropdown', 'date'], (a, b) => a !== b],

    'lt': ['is lower than', '<', ['number'], (a, b) => parseFloat(a) < parseFloat(b)],
    'lte': ['is lower or equat to', '≤', ['number'], (a, b) => parseFloat(a) <= parseFloat(b)],

    'ut': ['is upper than', '>', ['number'], (a, b) => parseFloat(a) > parseFloat(b)],
    'ute': ['is upper or equal to', '≥', ['number'], (a, b) => parseFloat(a) >= parseFloat(b)],

    'in': ['is in', '∈', ['dropdown'], (a, b) => b.includes(a)],
    'nin': ['is not in', '∉', ['dropdown'], (a, b) => ! b.includes(a)],

    'ct': ['contains', '∋', ['char', 'dropdown'], (a, b) => a.includes(b)],
    'nct': ['does not contain', '∌', ['char', 'dropdown'], (a, b) => ! a.includes(b)],

    'c': ['is', '✔', [], (a, b) => a],
    'nc': ['is not', '✖', [], (a, b) => !a],
}

const FIELD_CUSTOMIZATION = {
    'singleline': ['char'],
    'multiline': ['char'],
    'email': ['char'],
    'number': ['number'],
    'url': ['char'],
    'checkbox': ['none'],
    'checkboxes': ['dropdown'],
    'dropdown': ['dropdown'],
    'multiselect': ['dropdown'],
    'radio': ['dropdown'],
    'date': ['date'],
    'datetime': ['date'],
    'hidden': ['char'],
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
        const [value_type] = FIELD_CUSTOMIZATION[selected_field.type];

        dom_operator.classList.toggle('formbuilder-hide', value_type === 'none');
        dom_val_char.classList.toggle('formbuilder-hide', value_type !== 'char');
        dom_val_num.classList.toggle('formbuilder-hide', value_type !== 'number');
        dom_val_list.classList.toggle('formbuilder-hide', value_type !== 'dropdown');
        dom_val_date.classList.toggle('formbuilder-hide', value_type !== 'date');
        if (dom_rules !== undefined) {
            dom_rules.classList.toggle('formbuilder-hide', true);
        }

        if (dom_operator.style.display !== 'none') {
            const dom_operator_select = dom_operator.querySelector('select')
            const operator_choices = Object.entries(OPERATORS)
                .filter(([k, v]) => v[2].includes(value_type))
                .map(([k, v]) => [k, v[0], false])
            fill_dropdown(dom_operator_select, operator_choices)
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
