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
    const dom_form_fields = document.querySelector('.formbuilder-fields-block > div[data-streamfield-stream-container]')
    const dom_block_fields = dom_form_fields.querySelectorAll(':scope > [data-contentpath]:not([aria-hidden])');

    return Object.fromEntries(Array.from(dom_block_fields).map((dom_block, index) => [
        dom_block.getAttribute('data-contentpath'),
        {
            'index': index,
            'contentpath': dom_block.getAttribute('data-contentpath'),
            'label': dom_block.querySelector('.formbuilder-field-block-label input').value || `field n°${ index + 1}`,
            'dom_block': dom_block,
            'type': dom_block.getElementsByClassName('formbuilder-field-block')[0].className.replace('formbuilder-field-block', '').split('-')[1]
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
    const get_field_block = (class_name) => dom_field_block.getElementsByClassName(class_name)[0].parentNode;

    const dom_operator = get_field_block('formbuilder-beb-operator').parentNode;
    const dom_val_char = get_field_block('formbuilder-beb-val-char').parentNode;
    const dom_val_num = get_field_block('formbuilder-beb-val-num').parentNode;
    const dom_val_list = get_field_block('formbuilder-beb-val-list').parentNode;
    const dom_val_date = get_field_block('formbuilder-beb-val-date').parentNode;
    const dom_rules = get_field_block('formbuilder-beb-rules');

    if (['and', 'or'].includes(dom_dropdown.value)) {
        dom_beb.classList.toggle('formbuilder-beb-inline', false);

        dom_operator.style.display = 'none';
        dom_val_char.style.display = 'none';
        dom_val_num.style.display = 'none';
        dom_val_list.style.display = 'none';
        dom_val_date.style.display = 'none';
        dom_rules.style.display = '';
    } else {
        dom_beb.classList.toggle('formbuilder-beb-inline', true);

        const selected_field = get_fields()[dom_dropdown.value]
        const [value_type] = FIELD_CUSTOMIZATION[selected_field.type];

        dom_operator.style.display = value_type === 'none' ? 'none' : '';
        dom_val_char.style.display = value_type === 'char' ? '' : 'none';
        dom_val_num.style.display = value_type === 'number' ? '' : 'none';
        dom_val_list.style.display = value_type === 'dropdown' ? '' : 'none';
        dom_val_date.style.display = value_type === 'date' ? '' : 'none';
        dom_rules.style.display = 'none';

        if (dom_operator.style.display !== 'none') {
            const dom_operator_select = dom_operator.querySelector('select')
            const operator_choices = Object.entries(OPERATORS)
                .filter(([k, v]) => v[2].includes(value_type))
                .map(([k, v]) => [k, v[0], false])
            fill_dropdown(dom_operator_select, operator_choices)
        }
    }
}


class BEBBlockDefinition extends window.wagtailStreamField.blocks.StructBlockDefinition {
    get_rule_subjects_choices() {
        const fields_choices = Object.values(this.fields)
            .filter((f) => this.current_field.index > f.index)
            .map(f => [f.contentpath, f.label, false])

        return [
            ['', 'Fields:', true],
            ...fields_choices,
            ['', 'Expression:', true],
            ['or', 'one of...', false],
            ['and', 'all of...', false],
        ]
    }

    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(placeholder, prefix, initialState, initialError);
        this.dom_struct_block = block.container[0];

        if (this.dom_struct_block.closest('[data-contentpath="rules"] > div.formbuilder-block-hidden') !== null) {
            return block
        }

        this.dom_rule_block = block.container[0].closest('[data-contentpath="rule"]')
        this.dom_field_block = this.dom_rule_block.closest('.formbuilder-field-block');
        this.dom_field_block_container = this.dom_field_block.parentNode.parentNode.parentNode;

        this.fields = get_fields()
        this.current_field = this.fields[this.dom_field_block_container.getAttribute('data-contentpath')];

        if (this.current_field.index === 0) {
            this.dom_rule_block.style.display = 'none'
            return block;
        }

        const dom_rule_subject_dropdown = this.dom_rule_block.querySelector('[data-contentpath="field"] select')
        fill_dropdown(dom_rule_subject_dropdown, this.get_rule_subjects_choices())

        dom_rule_subject_dropdown.addEventListener('change', (event) => on_rule_subject_selected(event.target))
        on_rule_subject_selected(dom_rule_subject_dropdown)

        return block;
    }
}
window.telepath.register('forms.blocks.BooleanExpressionBuilderBlock', BEBBlockDefinition);
